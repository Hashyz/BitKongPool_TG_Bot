# Import necessary libraries
#pip install pyTelegramBotAPI, telebot

import os
import telebot
from BitKong import BitKongAPI  # Assuming BitKongAPI is a custom module
import datetime
from telebot import types

# Retrieve the API key from environment variables
API_KEY = os.getenv("API-KEY")
bot = telebot.TeleBot(API_KEY)

try:
  # Define a command handler for the "/start" command
  @bot.message_handler(commands=["start"])
  def start(message):
      # Create a custom keyboard markup
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      button_Pool = types.InlineKeyboardButton('/pool', callback_data='/pool')
      button_Leader = types.InlineKeyboardButton('/leader', callback_data='/leader')
  
      markup.add(button_Pool)
      markup.add(button_Leader)
  
      # Send a welcome message with the custom keyboard
      bot.send_message(message.chat.id, text='Hello Konger!!', reply_markup=markup)
  
  # Define a command handler for the "/pool" command
  @bot.message_handler(commands=["pool"])
  def pool(message):
      # Parse the user's request
      request = message.text.split()
      
      if len(request) > 1:
          if request[1].lower() == "p":
              if len(request) > 2:
                  # Check if the request specifies a past pool
                  need = int(request[2]) if request[2].isdigit() else 0
                  jsn = BitKongAPI().getData(request, need)
  
                  respondInjsn = jsn['respondInjsn']
                  totalPool = respondInjsn['amount']
                  currency = respondInjsn['currency']['id']
  
                  if need > 0:
                      bot.reply_to(
                          message,
                          f"🤑 Total Pool Past {need} hour: \"{totalPool} {currency}\"!",
                          parse_mode="Markdown")
                  else:
                      bot.reply_to(
                          message,
                          f"🤑 Total Current Pool : \"{totalPool} {currency}\"!\n{BitKongAPI().timeLeft()}",
                          parse_mode="Markdown")
          else:
              bot.reply_to(message, "😕 Do you mean 'p'? (Past Tour number)")
      else:
          # Retrieve and display the current pool information
          res1 = BitKongAPI().req()
          respondInjsn = res1.json()['data']['leaderboard']
          totalPool = respondInjsn['amount']
          currency = respondInjsn['currency']['id']
          bot.reply_to(
              message,
              f"🤑 Now Total \"{totalPool} {currency}\" pool !\n{BitKongAPI().timeLeft()}",
              parse_mode="Markdown")
  
  # Define a command handler for the "/leader" command
  @bot.message_handler(commands=["leader"])
  def leader(message):
      # Parse the user's request
      request = message.text.split()
      boo = True
      jsn = {}
      pastHour = 0
  
      if len(request) > 1:
          if request[1].lower() == "t":
              if len(request) > 2:
                  totalPeo = int(request[2]) if request[2].isdigit() else 0
                  
                  if len(request) > 3:
                      if request[3].lower() == "p":
                          if len(request) > 4:
                              pastHour = int(request[4]) if request[4].isdigit() else 0
                          else:
                              pastHour = 0
                          jsn = BitKongAPI().getData(request, need=pastHour, take=totalPeo if totalPeo < 50 else 50)
                          boo = False
                      else:
                          boo = True
                  else:
                      pass
                  
                  if boo:
                      jsn = BitKongAPI().getData(request, need=0, take=totalPeo if totalPeo < 50 else 50)
                  
                  res1 = jsn["respond"]
                  respondInjsn = jsn['respondInjsn']
                  totalPool = respondInjsn['amount']
                  currency = respondInjsn['currency']['id']
                  
                  bot.reply_to(
                      message,
                      f"💰 Total Pool in Past {pastHour} Hour : {totalPool} {currency}!\n{BitKongAPI().timeLeft()}\n```{BitKongAPI().TourTable(res1,totalPeo)}```\n",
                      parse_mode="Markdown",
                  )
              else:
                  bot.reply_to(message, "😕 Do you mean 't'? (Total People)")
          else:
              bot.reply_to(message, "😕 Do you mean 't'? (Total People)")
      else:
          # Retrieve and display leaderboard information
          defaultPeo = 10
          jsn = BitKongAPI().getData(request, need=0, take=defaultPeo)
          res1 = jsn["respond"]
          respondInjsn = jsn['respondInjsn']
          totalPool = respondInjsn['amount']
          currency = respondInjsn['currency']['id']
          
          bot.reply_to(
              message,
              f"💰 Total Pool in Current Hour : {totalPool} {currency}!\n{BitKongAPI().timeLeft()}\n```{BitKongAPI().TourTable(res1,defaultPeo)}```\n",
              parse_mode="Markdown",
          )
except Exception as e:
  print(f"An error occurred: {e}")
  
# Start the bot polling
print("* Start Pooling.")
bot.polling()
