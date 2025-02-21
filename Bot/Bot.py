from __future__ import annotations
from openai import OpenAI
from time import sleep
import os

class Bot:
  def __init__(self, role: str, model='gpt-4o-mini', name: str = None, context=None):
    self.role = role
    self.model = model
    self.chat = OpenAI().chat
    self.name = name or role.capitalize()
    self.context = Message(role = 'developer', content = context)
    if self.context:
      self.context.strip('.').strip()
      self.context.append('. Your name is ' + self.name + '.')

  def reply(self, conversation: Conversation):
    completion = self.chat.completions.create(
        model=self.model,
        messages=conversation.appendContext(self.context if self.context else None).relativeList(),
    )

    reply = Message(self.role, completion.choices[0].message.content, sender = self.name)
    conversation.add_message(reply)
    return reply


class Message:
  def __init__(self, role, content, mirror=False, sender=None):
    self.role: str = role
    self.content: str = content
    self.sender = sender or role.capitalize()
    self.mirror = Message('user' if self.role == 'system' else 'system', self.content, mirror=True) if not mirror else None

  def write(self, delay=0.02):
    print(f'{self.sender}:')
    msg = ''
    for char in str(self.content):
      columns, _ = os.get_terminal_size()
      if char.isspace(): char = ' '
      if len(msg) >= columns: print(); msg = ''
      msg += char
      print(f"\r{msg}", end='', flush=True)
      sleep(delay)

  def toDict(self):
    return {'role': self.role, 'content': self.content}
  
  def append(self, content):
    self.content += content

  def strip(self, *args, **kwargs):
    self.content = self.content.strip(*args, **kwargs)
    return self
  
  def __str__(self):
    return f'{self.role.upper()}: {self.content}'
  
  def __repr__(self):
    return f'Message(role={self.role}, content={self.content[:7]+"..." if len(self.content) > 10 else self.content}, sender={self.sender})'

  def __bool__(self):
    return bool(self.content)
  
class Conversation:
  def __init__(self, messages: list[Message]):
    self.messages = messages

  def add_message(self, message: Message):
    self.messages.append(message)

  def last(self) -> Message:
    return self.messages[-1]
  
  def waitFor(self):
    return 'system' if self.last().role == 'user' else 'user'
  
  def list(self):
    return [message.toDict() for message in self.messages]
  
  def mirror(self):
    return Conversation([message.mirror for message in self.messages])
  
  def relativeList(self, role = 'system'):
    return self.list() if self.waitFor() == role else self.mirror().list()

  def appendContext(self, context: Message):
    if not context: return self
    messages = self.messages.copy()
    messages.insert(0, context)
    return Conversation(messages=messages)
  
  def __getitem__(self, index) -> Message:
    return self.messages[index]
  
  def __str__(self):
    return '\n'.join([str(message) for message in self.messages])
  
  