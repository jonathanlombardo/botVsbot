from Bot import Bot, Conversation, Message
from time import sleep
from dotenv import load_dotenv
import os, sys

def main():

  load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

  print('Creating bots...', end='\r')
  userBot = Bot('user')
  aiBot = Bot('system')
  print('Creating bots... Done!')

  chat: Conversation = Conversation([Message('user', input('Write first input message: '))])
  print()

  timeout = 0
  counter = 0
  while counter <= timeout:
    bot = userBot if chat.last().role == 'system' else aiBot
    bot.reply(chat)

    chat.last().write(speed=0.02)
    print('\n')

    if counter >= timeout:
      answ = input('\rDo you want to continue? (y/n): ').lower()
      while answ not in ['y', 'n']:
        sys.stdout.write("\033[F")
        answ = input('\rDo you want to continue? (y/n): ')
        
      if answ == 'y': counter = -1; sys.stdout.write("\033[F"); print(' ' * os.get_terminal_size().columns, end='\r')
    
    counter += 1
  

if __name__ == '__main__':
  main()
  