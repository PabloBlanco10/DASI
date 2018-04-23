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
import database
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, CategoriesOptions, RelationsOptions

TOKEN = '511510486:AAEULAaDh8wnpHB5oXydCo149zus3MknZfg'  # @eatbot_bot

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='98851fcb-a08a-4596-babb-f1f734c48af8',
  password='3Hum5Es63rG3',
  version='2018-03-16')

response = natural_language_understanding.analyze(
  text='quiero pedir una pizza bolognesa para cenar',
  clean=False,
  features=Features(
    entities=EntitiesOptions(
      limit=5),
    concepts=ConceptsOptions(
      limit=3),
    categories=CategoriesOptions(),
    relations=RelationsOptions(),
    keywords=KeywordsOptions())
)

print(json.dumps(response, indent=2))

listaProductos = ["Pizza bolognesa", "Pizza margarita", "Pizza Hawaiana", "Pizza Pollo", "Pizza Napolitana", "Pizza cuatro quesos", "Pizza mozzarella", "Pizza prosciutto"]
listaRestaurantes = ["Restaurante1", "Restaurante2", "Restaurante3", "Restaurante4"]


database.borrarBBDD
database.crearTablas
database.cargarProductosBBDD(listaProductos)
database.cargarRestaurantesBBDD(listaRestaurantes)


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
