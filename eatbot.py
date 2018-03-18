########################################################
#################### TELEGRAM BOT ######################
################ EATBOT - @eatbot_bot ##################
# UCM - MÁSTER INGENIERÍA INFORMÁTICA - DASI - GRUPO 3 #
########################################################

##################### AUTORES ##########################
############### Pablo Blanco Peris #####################
############# María Castañeda López ####################
########################################################


import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = '511510486:AAEULAaDh8wnpHB5oXydCo149zus3MknZfg'  # @eatbot_bot


#función que gestiona los mensajes recibidos por el chat
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    mensaje = msg['text']
    print(mensaje)

    if mensaje == '/start':
        bot.sendMessage(chat_id, 'Buenas, soy EatBot, ¿te apetece comer algo? 🍕🌭🍔🌮🌯🍱🍩🍰')
    else:
        bot.sendMessage(chat_id, mensaje)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                       [InlineKeyboardButton(text='Tócame', callback_data='press')],
                   ])

        bot.sendMessage(chat_id, 'Prueba con el botón del chat', reply_markup=keyboard)


#función que gestiona los botones inchat
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    # print('Callback Query catch')
    # print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Te he pillado y lo sabes')


bot = telepot.Bot(TOKEN)

MessageLoop(bot, {'chat': on_chat_message,
                  # callback_query es el boton del chat
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)

