from __future__ import annotations
from openai import OpenAI
from time import sleep
import os

class Bot:
  def __init__(self, role, model='gpt-4o-mini'):
    self.role = role
    self.model = model
    self.chat = OpenAI().chat

  def reply(self, conversation: Conversation):
    
    completion = self.chat.completions.create(
        model=self.model,
        messages=conversation.list(),
    )

    reply = Message(self.role, completion.choices[0].message.content)
    conversation.add_message(reply)
    return reply


class Message:
  def __init__(self, role, content):
    self.role: str = role
    self.content: str = content

  def __str__(self):
    return f'{self.role.upper()}: {self.content}'
  
  def write(self, speed=0.02):
    print(f'{self.role.upper()}:')
    msg = ''
    for char in str(self.content):
      columns, _ = os.get_terminal_size()
      if char.isspace(): char = ' '
      if len(msg) >= columns: print(); msg = ''
      msg += char
      print(f"\r{msg}", end='', flush=True)
      sleep(speed)
  
class Conversation:
  def __init__(self, messages: list[Message]):
    self.messages = messages

  def add_message(self, message: Message):
    self.messages.append(message)

  def last(self) -> Message:
    return self.messages[-1]
  
  def list(self):
    return [{'role': message.role if self.last().role == 'user' else Conversation.notRole(message.role), 'content': message.content} for message in self.messages]
  
  def __getitem__(self, index) -> Message:
    return self.messages[index]
  
  @staticmethod
  def notRole(role):
    return 'system' if role == 'user' else 'user'
  