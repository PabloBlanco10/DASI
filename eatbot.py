########################################################
#################### TELEGRAM BOT ######################
################ EATBOT - @eatbot_bot ##################
# UCM - MÁSTER INGENIERÍA INFORMÁTICA - DASI - GRUPO 3 #
########################################################

##################### AUTORES ##########################
############### Pablo Blanco Peris #####################
############# María Castañeda López ####################
########################################################


import database
import conversation
import rules
from pyknow import *

import telepot
import time
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telepot.delegate import pave_event_space, per_chat_id, create_open, per_callback_query_origin
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
import json



class EatBot:
    eatBotRules = None
    chat_id = None
    message = None
    restaurant = None
    productOrder = None
    idLastOrder = None

    def __init__(self):

        # self.createDatabase()

        # TOKEN = '571166195:AAFEEM3SbBGrSUnsodId-q8TwRQ-yQ3ANOk'  # @eatbotMariabot
        TOKEN = '511510486:AAEULAaDh8wnpHB5oXydCo149zus3MknZfg'  # @eatbot_bot

        self.bot = telepot.Bot(TOKEN)
        MessageLoop(self.bot, self.manageMessage).run_as_thread()
        print('Listening ...')

        self.eatBotRules = rules.EatBotRules()
        self.eatBotRules.setBot(self)
        self.eatBotConversation = conversation.EatBotConversation()

        # Keep the program running.
        while 1:
            time.sleep(10)



    def manageMessage(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.chat_id = chat_id

        # mensaje del usuario
        self.message = msg

        # guardamos el usuario en la bdd
        user = [[chat_id, msg['from']['first_name']]]
        database.insertUser(user)

        # llamamos a dialogflow
        intent, entities = self.eatBotConversation.checkMessage(self.message['text'])


        # gestionamos el mensaje
        self.eatBotRules.reset()

        if intent != '':
            self.eatBotRules.declare(Fact(intent = intent))

        for k , v in entities.items():
            f = Fact()
            f[k] = v
            if k != '' and v != '':
                self.eatBotRules.declare(f)

        print(self.eatBotRules.facts)
        self.eatBotRules.run()



    def responseGreet(self, nombre):
        #saludo
        self.bot.sendMessage(self.chat_id, 'Hola ' + nombre +  ' te apetece comer algo? Sólo tienes que decir el tipo de comida que buscas !')



    def responseNotUnderstood(self):
        #no hemos reconocido nada
        self.bot.sendMessage(self.chat_id, 'Lo siento, no sé a que te refieres... 🤔🤔')



    def responseFoodTypeWithoutFoodType(self):
        #tipo de comida no reconocido, mostramos los tipos de comida
        foodTypeList = database.searchFoodType()
        self.bot.sendMessage(self.chat_id, 'Qué te apetece pedir? Tenemos estos tipos de comida disponibles')

        i = 0
        for foodType in foodTypeList:
            i += 1
            self.bot.sendMessage(self.chat_id, str(i) + '. ' + foodType)

        self.eatBotConversation.addContext('selectFoodType')


    def responseFoodTypeWithFoodType(self, foodType):
        #tipo de comida reconocido, mostramos restaurantes de ese tipo
        restaurantList = database.searchRestaurantType(foodType)
        if len(restaurantList) > 0 :
            self.bot.sendMessage(self.chat_id, 'Tenemos estos resturantes que cuentan con tipo de comida ' + foodType)
            i = 0
            for restaurant in restaurantList:
                i += 1
                self.bot.sendMessage(self.chat_id, str(i) + '. ' + restaurant)

            self.bot.sendMessage(self.chat_id, 'Cuál te apetece? 🍽')
            self.eatBotConversation.addContext('selectRestaurant')

        else:
            self.responseNotUnderstood()

    def responseChooseRestaurantWithoutRestaurant(self):
        #nombre de restaurante no reconocido, mostramos todos los restaurantes
        restaurantList = database.searchRestaurant()
        self.bot.sendMessage(self.chat_id, 'Qué restaurante te apetece? Estos son los restaurantes disponibles')

        i = 0
        for restaurant in restaurantList:
            i += 1
            self.bot.sendMessage(self.chat_id, str(i) + '. ' + restaurant)

        self.eatBotConversation.addContext('selectRestaurant')


    def responseChooseRestaurantWithRestaurant(self, restaurant):
        #restauarante elegido, mostramos productos
        productList = database.searchProductsFromRestaurant(restaurant)
        self.restaurant = restaurant
        if len(productList) > 0 :
            self.bot.sendMessage(self.chat_id, 'Has elegido el restaurante ' + restaurant)
            self.bot.sendMessage(self.chat_id, 'Este restaurante tiene estos productos')
            i = 0
            for product in productList:
                i += 1
                self.bot.sendMessage(self.chat_id, str(i) + '. ' + product)

            self.bot.sendMessage(self.chat_id, 'Qué te apetece?🤤 Elige cada producto en una linea y avisame cuando termines '+
                                 'por favor😋')
            self.eatBotConversation.addContext('selectProduct')
            self.productOrder = []


        else:
            self.responseNotUnderstood()


    def responseChooseProduct(self, product):
        #producto elegido
        productId = database.searchIDProduct(product)
        if productId > -1:
            self.productOrder.append(productId)

        self.eatBotConversation.addContext('selectProduct')

    def responseFinishOrder(self):
        #idRestaurant = database.searchIDRestaurant(self.restaurant)

        database.insertOrder((self.chat_id, self.restaurant))
        idOrder = database.searchOrder(self.chat_id, self.restaurant)
        self.idLastOrder = idOrder

        for idProduct in self.productOrder:

             database.insertOrderProduct((idOrder, idProduct))

        self.bot.sendMessage(self.chat_id,'Tu pedido con identificador ' + str(idOrder) + ' se ha realizado con éxito')
        self.bot.sendMessage(self.chat_id,'¿Qué te ha parecido la comida? Añade un comentario')
        self.eatBotConversation.addContext('makeOpinion')


    def responseMakeOpinion(self):
        opinion = self.eatBotConversation.getOpinion()
        database.insertOpinion((self.idLastOrder, opinion))



    #creacion de la bdd
    def createDatabase(self):
        productsList = ["Pizza bolognesa", "Pizza margarita", "Pizza hawaiana", "Pasta carbonara", "Pizza napolitana",
                          "Pasta alfredo",
                          "Pizza mozzarella", "Pizza prosciutto", "Arroz Tres Delicias", "Gyozas", "Kebab",
                          "Falafel", "Patatas fritas",
                          "Shushi", "Fideos Fritos", "Hamburguesa Queso", "Aros de Cebolla", "Tortilla de Patata",
                          "Costillas"]

        restaurantsList = [["Yhu Yughae", "china"], ["La Tagliatella", "italiana"],
                             ["La mafia", "italiana"], ["Doner Valdebebas", "turca"], ["Doner Bernabeu", "turca"],
                             ["Korean Style", "coreana"], ["Nyu Jao", "japonesa"], ["Fosters", "americana"],
                             ["Casa Jose", "española"], ["Mcdonals", "americana"], ["Grill Texas", "americana"]]

        restaurantProductList = [[1, 9], [1, 10], [2, 2], [2, 4], [3, 2], [3, 5], [4, 11], [4, 12],
                                              [5, 11], [5, 13], [6, 9], [6, 14], [7, 9], [7, 15],
                                              [8, 16], [8, 17], [9, 18], [9, 19], [10, 13], [10, 16],
                                              [11, 17], [11, 19]]

        database.deleteDatabase()
        database.createTables()
        database.insertProducts(productsList)
        database.insertRestaurants(restaurantsList)
        database.insertRestaurantProducts(restaurantProductList)


        # database.searchRestaurantType()
        # listaRestaurantesTipoX = database.searchRestaurantType('chino')
        # listaProductosRestauranteX = database.buscarProductosDelRestaurante('Restaurante Asiatico')



if __name__ == '__main__':

    #creamos instancia del bot
    eatbot = EatBot()





# class UserHandler(telepot.helper.ChatHandler):
#     def __init__(self, *args, **kwargs):
#         super(UserHandler, self).__init__(*args, **kwargs)
#
#     def on_chat_message(self, msg):
#         content_type, chat_type, chat_id = telepot.glance(msg)
#
#         # nombre del usuario
#         nombre = (msg['from']['first_name'])
#
#         # mensaje del usuario
#         mensaje = msg['text']
#
#         # guardamos el usuario en la bdd
#         usuario = [[chat_id, msg['from']['first_name']]]
#         database.insertarUsuario(usuario)
#
#         # llamamos a dialogflow
#         intent, entities = conversation.consultarMensaje(mensaje)
#
#         # gestionamos el mensaje
#
#
#         f = Fact(intent)
#
#         EatBot.gestionarMensaje()

        # if intent == 'Default Fallback Intent':
        #     self.eatBot.sendMessage(chat_id, 'No entiendo a qué te refieres')
        #
        # elif intent == 'saludo':
        #     self.eatBot.sendMessage(chat_id,
        #                     'Hola ' + nombre +  ' te apetece comer algo? Sólo tienes que decir el tipo de comida que buscas !')
        #     # bot.sendPhoto(chat_id, 'http://elestimulo.com/bienmesabe/wp-content/uploads/sites/7/2016/04/detective.jpg')
        #
        #
        # elif intent == 'elegirRestaurante':
        #     bot.sendMessage(chat_id, 'Este restaurante tiene estos productos:')
        #
        #
        # elif intent == 'tiposComida':
        #     tiposDeRestaurante = database.buscarTiposRestaurante()
        #     str1 = ', '.join(tiposDeRestaurante)
        #
        #     bot.sendMessage(chat_id, 'Tenemos diferentes tipos de comida que puedes elegir entre ' + str1)

        # database.insertarPedido([[chat_id, 'Casa Jose']])
        # idPedido = database.buscarPedido(chat_id, 'Casa Jose')
        # database.insertarPedidoProducto([[idPedido, 'Costillas']])# for hasta que termine de introducir todos los productos

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





# from watson_developer_cloud import NaturalLanguageUnderstandingV1
# from watson_developer_cloud.natural_language_understanding_v1 \
#   import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, CategoriesOptions, RelationsOptions, SemanticRolesOptions, SentimentOptions, MetadataOptions, EmotionOptions
# from watson_developer_cloud import LanguageTranslatorV2

#
# natural_language_understanding = NaturalLanguageUnderstandingV1(
#   username='98851fcb-a08a-4596-babb-f1f734c48af8',
#   password='3Hum5Es63rG3',
#   version='2018-03-16')
#
#
# language_translator = LanguageTranslatorV2(
#     username='175989d2-d33d-4a62-8374-453c799047a8',
#     password='xWwfNrCRQr2H',
# )
#
# texto = 'hola, qué tipo de comida tenéis?'
# translation = language_translator.translate(
#     text=texto,
#     model_id='es-en')
# # print(json.dumps(translation, indent=2, ensure_ascii=False))
#
# for key, value in translation.items():
#     if 'translations' in key:
#         translate = value[0].get('translation')
#
# print(translate)
#
#
# response = natural_language_understanding.analyze(
#   text=translate,
#   clean=False,
#   features=Features(
#     entities=EntitiesOptions(),
#     concepts=ConceptsOptions(),
#     categories=CategoriesOptions(),
#     relations=RelationsOptions(),
#     keywords=KeywordsOptions(),
#     semantic_roles= SemanticRolesOptions(),
#     sentiment= SentimentOptions()))
#     # metadata= MetadataOptions(),
#     # emotion= EmotionOptions())
# print(json.dumps(response, indent=2))
#
# print('__________________________________________')
#
# respuesta = natural_language_understanding.analyze(
#   text=texto,
#   clean=False,
#   features=Features(
#     entities=EntitiesOptions(),
#     concepts=ConceptsOptions(),
#     categories=CategoriesOptions(),
#     relations=RelationsOptions(),
#     keywords=KeywordsOptions(),
#     semantic_roles= SemanticRolesOptions()))
#     # sentiment= SentimentOptions()))
#     # metadata= MetadataOptions(),
#     # emotion= EmotionOptions())
# print(json.dumps(respuesta, indent=2))


# bot = telepot.DelegatorBot(TOKEN, [
#     pave_event_space()(
#         per_chat_id(), create_open, UserHandler, timeout=3600
#     ),
# ])
# bot.message_loop(run_forever='Listening ...')



