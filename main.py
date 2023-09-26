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

    button_Pool = types.InlineKeyboardButton('Current Prize Pool',
                                             callback_data='/pool')
    button_Leader = types.InlineKeyboardButton('Current Leaderboard',
                                               callback_data='/leader')
    button_Leader_Perv = types.InlineKeyboardButton(
        'Previous Leaderboard', callback_data='/leader t 10 p 1')

    markup.add(button_Pool)
    markup.add(button_Leader)
    markup.add(button_Leader_Perv)

    # Send a welcome message with the custom keyboard
    bot.send_message(message.chat.id,
                     text='Hello Konger!!',
                     reply_markup=markup)

  #Inline Buttons
  @bot.message_handler(
      func=lambda message: message.text == 'Current Prize Pool')
  def send_pool(message):
    message.text = "/pool"
    pool(message)

  @bot.message_handler(
      func=lambda message: message.text == 'Current Leaderboard')
  def send_leader(message):
    message.text = "/leader"
    leader(message)

  @bot.message_handler(
      func=lambda message: message.text == 'Previous Leaderboard')
  def send_leader_prev(message):
    message.text = "/leader t 10 p 1"
    leader(message)

  @bot.callback_query_handler(func=lambda call:True)
  def answer(callback):
    if callback.message:
      if callback.data:
        if callback.data.split()[0] == "/leader":
          callback.message.text = callback.data
          leader(callback.message)
        # elif callback.data.split()[0] == "/pool":
        #   pool(callback.message)
        else:pass

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
          jsn = BitKongAPI().getData(request, need)  #respond requests
          respondInjsn = jsn.get('respondInjsn')
          # totalPool = respondInjsn['amount']
          if respondInjsn == None:
            return bot.reply_to(message,
                                "Please Try Again! Server is Refreshing!")
          totalPool = respondInjsn.get("amount")  #['amount']
          if totalPool == None:
            return bot.reply_to(message,
                                "Please Try Again! Server is Refreshing!")

          currency = respondInjsn['currency']['id']

          if need > 0:
            bot.reply_to(
                message,
                f"Previous {need} Hour Pool : \"{totalPool} {currency}\"!",
                parse_mode="Markdown")
          else:
            bot.reply_to(
                message,
                f"Current Price Pool : \"{totalPool} {currency}\"!\n{BitKongAPI().timeLeft()}",
                parse_mode="Markdown")
      else:
        return bot.reply_to(message, "😕 Do you mean 'p'? (Past Tour number)")
    else:
      # Retrieve and display the current pool information
      res1 = BitKongAPI().req()
      # print(res1.json())
      respondInjsn = res1.json().get('data').get("leaderboard")
      # totalPool = respondInjsn['amount']
      if respondInjsn == None:
        return bot.reply_to(message, "Please Try Again! Server is Refreshing!")
      # respondInjsn = respondInjsn1.get('leaderboard')
      totalPool = respondInjsn.get("amount")  #['amount']
      if totalPool == None:
        return bot.reply_to(message, "Please Try Again! Server is Refreshing!")
      currency = respondInjsn['currency']['id']
      return bot.reply_to(
          message,
          f"Current Price Pool : \"{totalPool} {currency}\"!\n{BitKongAPI().timeLeft()}",
          parse_mode="Markdown")

  # Define a command handler for the "/leader" command
  @bot.message_handler(commands=["leader"])
  def leader(message):
    makeup = types.InlineKeyboardMarkup(row_width=5)
    hr1 = types.InlineKeyboardButton("1h", callback_data="/leader t 10 p 1")
    hr2 = types.InlineKeyboardButton("2h", callback_data="/leader t 10 p 2")
    hr3 = types.InlineKeyboardButton("3h", callback_data="/leader t 10 p 3")
    hr4 = types.InlineKeyboardButton("4h", callback_data="/leader t 10 p 4")
    hr5 = types.InlineKeyboardButton("5h", callback_data="/leader t 10 p 5")
    makeup.add(hr1, hr2, hr3, hr4, hr5)

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
              jsn = BitKongAPI().getData(
                  request,
                  need=pastHour,
                  take=totalPeo if totalPeo < 50 else 50)
              boo = False
            else:
              boo = True
          else:
            pass

          if boo:
            jsn = BitKongAPI().getData(request,
                                       need=0,
                                       take=totalPeo if totalPeo < 50 else 50)

          res1 = jsn["respond"]
          respondInjsn = jsn.get('respondInjsn')

          if respondInjsn == None:
            return bot.reply_to(message,
                                "Please Try Again! Server is Refreshing!")
          totalPool = respondInjsn.get("amount")  #['amount']
          if respondInjsn == None:
            return bot.reply_to(message,
                                "Please Try Again! Server is Refreshing!")
          currency = respondInjsn['currency']['id']

          # bot.reply_to(
          #     message,
          #     f"Previous {pastHour} Hour Prize Pool : {totalPool} {currency}\n```{BitKongAPI().TourTable(res1,totalPeo)}```\n",
          #     parse_mode="Markdown",
          # )
          table_image = BitKongAPI.TourTable(res1, totalPeo)
          if pastHour == 0:
            bot.send_photo(
                message.chat.id,
                photo=table_image,
                caption=
                f"Current Price Pool : {totalPool} {currency}!\n{BitKongAPI().timeLeft()}",
                parse_mode="Markdown",
                reply_markup=makeup)
          else:
            bot.send_photo(
                message.chat.id,
                photo=table_image,
                caption=
                f"Previous {pastHour} Hour Pool : {totalPool} {currency}!\n",
                parse_mode="Markdown",
                reply_markup=makeup)
        else:
          bot.reply_to(message, "😕 Do you mean 't'? (Total People)")
      else:
        bot.reply_to(message, "😕 Do you mean 't'? (Total People)")
    else:
      # Retrieve and display leaderboard information
      defaultPeo = 10
      jsn = BitKongAPI().getData(request, need=0, take=defaultPeo)
      res1 = jsn["respond"]
      respondInjsn = jsn.get('respondInjsn')
      if respondInjsn == None:
        return bot.reply_to(message, "Please Try Again! Server is Refreshing!")
      totalPool = respondInjsn.get('amount')
      if totalPool == None:
        return bot.reply_to(message, "Please Try Again! Server is Refreshing!")
      currency = respondInjsn['currency']['id']

      # bot.reply_to(
      #     message,
      #     f"Current Price Pool : {totalPool} {currency}!\n{BitKongAPI().timeLeft()}\n```{BitKongAPI().TourTable(res1,defaultPeo)}```\n",
      #     parse_mode="Markdown",
      # )
      table_image = BitKongAPI.TourTable(res1, defaultPeo)

      bot.send_photo(
          message.chat.id,
          photo=table_image,
          caption=
          f"Current Price Pool : {totalPool} {currency}!\n{BitKongAPI().timeLeft()}",
          parse_mode="Markdown",
      )  #reply_markup=makeup)
      # bot.send_photo(message, photo=table_image, caption=f"Previous 1 Hour Prize Pool : {totalPool} {currency}", parse_mode="Markdown")

  # Start the bot polling
  print("* Start Pooling.")
  bot.polling()
except Exception as e:
  print(f"An error occurred: {e}")
