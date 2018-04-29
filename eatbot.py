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
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telepot.delegate import pave_event_space, per_chat_id, create_open, per_callback_query_origin
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, CategoriesOptions, RelationsOptions, SemanticRolesOptions, SentimentOptions, MetadataOptions, EmotionOptions
from watson_developer_cloud import LanguageTranslatorV2



TOKEN = '511510486:AAEULAaDh8wnpHB5oXydCo149zus3MknZfg'  # @eatbot_bot

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='98851fcb-a08a-4596-babb-f1f734c48af8',
  password='3Hum5Es63rG3',
  version='2018-03-16')


language_translator = LanguageTranslatorV2(
    username='175989d2-d33d-4a62-8374-453c799047a8',
    password='xWwfNrCRQr2H',
)

texto = 'hola, qué tipo de comida tenéis?'
translation = language_translator.translate(
    text=texto,
    model_id='es-en')
# print(json.dumps(translation, indent=2, ensure_ascii=False))

for key, value in translation.items():
    if 'translations' in key:
        translate = value[0].get('translation')

print(translate)


response = natural_language_understanding.analyze(
  text=translate,
  clean=False,
  features=Features(
    entities=EntitiesOptions(),
    concepts=ConceptsOptions(),
    categories=CategoriesOptions(),
    relations=RelationsOptions(),
    keywords=KeywordsOptions(),
    semantic_roles= SemanticRolesOptions(),
    sentiment= SentimentOptions()))
    # metadata= MetadataOptions(),
    # emotion= EmotionOptions())
print(json.dumps(response, indent=2))

print('__________________________________________')

respuesta = natural_language_understanding.analyze(
  text=texto,
  clean=False,
  features=Features(
    entities=EntitiesOptions(),
    concepts=ConceptsOptions(),
    categories=CategoriesOptions(),
    relations=RelationsOptions(),
    keywords=KeywordsOptions(),
    semantic_roles= SemanticRolesOptions()))
    # sentiment= SentimentOptions()))
    # metadata= MetadataOptions(),
    # emotion= EmotionOptions())
print(json.dumps(respuesta, indent=2))

listaProductos = ["Pizza bolognesa", "Pizza margarita", "Pizza Hawaiana", "Pizza Pollo", "Pizza Napolitana", "Pizza cuatro quesos", "Pizza mozzarella", "Pizza prosciutto"]
listaRestaurantes = [["Restaurante Asiatico","chino"], ["Pizzeria Luigi","italiano"],
                     ["La mafia","italiano"], ["Durum Doner","turco"], ["Durum kebab","turco"],
                     ["Korean Style","coreano"], ["Nyu Jao","japones"], ["Burger","americano"],
                     ["Casa Jose", "español"], ["Mcdonals","americano"], ["American Grill","americano"]]


database.borrarBBDD()
database.crearTablas()
database.cargarProductosBBDD(listaProductos)
database.cargarRestaurantesBBDD(listaRestaurantes)
database.buscarTiposRestaurante()

lista = database.buscarRestaurantesDelTipo('chino')

class UserHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print (content_type, chat_type, chat_id)

        mensaje = msg['text']
        print(mensaje)
        listaDeSaludos = ['hola', 'buenas', 'hey']

        if any(saludo in mensaje for saludo in listaDeSaludos):
            bot.sendMessage(chat_id, 'Holaaa, te apetece comer algo? Sólo tienes que decir el tipo de comida que buscas !')
            bot.sendPhoto(chat_id, 'http://elestimulo.com/bienmesabe/wp-content/uploads/sites/7/2016/04/detective.jpg')

        if mensaje == '/start':

            tiposDeRestaurante = database.buscarTiposRestaurante()
            str1 = ', '.join(tiposDeRestaurante)

            bot.sendMessage(chat_id, 'Qué tipo de comida te apetece? Tenemos' + str1)



        elif mensaje == '/help':

            bot.sendMessage(chat_id, 'Comandos:'
                                     '\n /buscarCine - Usa este comando para ver la cartelera del cine que quieras.'
                                     '\n /buscarPelicula - Usa este comando seguido del nombre de una pelicula para buscar los cines mas cercanos en los que se proyecta la pelicula.'
                                     '\n /cineCercano - Busca los cines mas cercanos basandose en tu ubicacion.'
                                     '\n /sugerirPelicula - Envia la informacion sobre una pelicula estrenada recientemente al azar.')


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, UserHandler, timeout=3600
    ),

    # pave_event_space()(
    #     per_callback_query_origin(), create_open, ButtonHandler, timeout=3600)
    # ,
])

#answerer = telepot.helper.Answerer(bot)

bot.message_loop(run_forever='Listening ...')


#función que gestiona los mensajes recibidos por el chat
# def on_chat_message(msg):
#     content_type, chat_type, chat_id = telepot.glance(msg)
#     mensaje = msg['text']
#     print(mensaje)
#
#     if mensaje == '/start':
#         bot.sendMessage(chat_id, 'Buenas, soy EatBot, ¿te apetece comer algo? 🍕🌭🍔🌮🌯🍱🍩🍰')
#     else:
#         bot.sendMessage(chat_id, mensaje)
#         keyboard = InlineKeyboardMarkup(inline_keyboard=[
#                        [InlineKeyboardButton(text='Tócame', callback_data='press')],
#                    ])
#
#         bot.sendMessage(chat_id, 'Prueba con el botón del chat', reply_markup=keyboard)
#
#
# #función que gestiona los botones inchat
# def on_callback_query(msg):
#     query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
#     # print('Callback Query catch')
#     # print('Callback Query:', query_id, from_id, query_data)
#
#     bot.answerCallbackQuery(query_id, text='Te he pillado y lo sabes')


# bot = telepot.Bot(TOKEN)
#
# MessageLoop(bot, {'chat': on_chat_message,
#                   # callback_query es el boton del chat
#                   'callback_query': on_callback_query}).run_as_thread()
# print('Listening ...')