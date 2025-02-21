from Bot import Bot, Conversation, Message
from time import sleep
from dotenv import load_dotenv
import os, sys

def readarguments():
  import argparse

  parser = argparse.ArgumentParser(description='Let the AI chat with itself')
  parser.add_argument('--model', '-m', type=str, default='gpt-4o-mini', help='Choose the model to use for the AI chat')
  parser.add_argument('--timeout-count', '-t', type=int, default=1, help='Choose the number of messages before asking to continue', choices=range(1, 101))
  parser.add_argument('--delay', '-d', type=float, default=0.02, help='Choose slowness when AI writing messages')
  parser.add_argument('--user-bot-name', '-ub', type=str, default='User', help='Choose the name of the user bot')
  parser.add_argument('--ai-bot-name', '-ab', type=str, default='AI', help='Choose the name of the AI bot')
  return parser.parse_args()

def main():

  load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
  args = readarguments()

  print('Creating bots:')
  userBot: Bot = Bot('user', args.model, args.user_bot_name, context=input(f'   Write a context for {args.user_bot_name}:'))
  aiBot: Bot = Bot('system', args.model, args.ai_bot_name, context=input(f'   Write a context for {args.ai_bot_name}:'))
  print('   Done!')

  prompt = Message('user', input(f'Write first prompt for {userBot.name}: '), sender=userBot.name)
  chat: Conversation = Conversation([prompt])
  print()

  timeout = args.timeout_count - 1
  counter = 0
  while counter <= timeout:
    bot = userBot if chat.waitFor() == 'user' else aiBot
    bot.reply(chat)

    chat.last().write(delay=args.delay)
    print('\n')

    if counter >= timeout:
      answ = input('\rDo you want to continue? (y/n): ').lower()
      while answ not in ['y', 'n']:
        sys.stdout.write("\033[F")
        answ = input('\rDo you want to continue? (y/n): ')
        
      if answ == 'y': counter = -1; sys.stdout.write("\033[F"); print(' ' * os.get_terminal_size().columns, end='\r')
    
    counter += 1
  
  if len(chat) > 0 and input('Do you want to save the conversation? (y/n): ').lower() == 'y':
    path = input('Write the path to save the conversation: ')
    chat.save(path=path.strip(), bots=[userBot, aiBot])
  
  input('\nPress any key to exit...')

if __name__ == '__main__':
  main()
  