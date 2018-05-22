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

# https://github.com/nickoala/telepot
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telepot.delegate import pave_event_space, per_chat_id, create_open, per_callback_query_origin
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent

# https://docs.python.org/2/library/time.html
import time

# https://github.com/buguroo/pyknow
from pyknow import *

class EatBot:
    eatBotRules = None
    chat_id = None
    message = None
    restaurant = None
    productOrder = None
    idLastOrder = None
    restaurantNameSuggestion = None


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

        # guardamos el usuario en la bdd si no está
        user = [[chat_id, msg['from']['first_name']]]
        database.insertUser(user)

        # llamamos a dialogflow
        intent, entities = self.eatBotConversation.checkMessage(self.message['text'])


        # gestionamos el mensaje
        self.eatBotRules.reset()


        # declaramos los hechos para las reglas, los intent y las entities
        if intent != '':
            self.eatBotRules.declare(Fact(intent = intent))

        for k , v in entities.items():
            f = Fact()
            f[k] = v
            if k != '' and v != '':
                self.eatBotRules.declare(f)

        print(self.eatBotRules.facts)

        # ejecutamos el motor de reglas
        self.eatBotRules.run()



    def responseGreet(self, nombre):
        #saludo
        self.bot.sendMessage(self.chat_id, 'Hola ' + nombre +  ' te apetece comer algo? Sólo tienes que decir el tipo de comida que buscas !')

        #miramos si ha hecho algún pedido anteriormente y le sugerimos al usuario elegir un restaurante del mismo tipo
        idRestaurant = database.searchOrderForUser(self.chat_id)
        if idRestaurant != None:
            foodType = database.searchRestaurantForOrder(idRestaurant)
            restaurantName = database.searchRestaurantTypeSimilar(foodType, idRestaurant)
            self.restaurantNameSuggestion = restaurantName
            self.bot.sendMessage(self.chat_id, 'Tu último pedido fue de comida ' + foodType + ' te apetece pedir en el restaurante ' + restaurantName + ' que es del mismo estilo ?')
            self.eatBotConversation.addContext('responseRestaurantSuggestion')



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

        # añadimos contexto para dialogflow
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

        # añadimos contexto para dialogflow
        self.eatBotConversation.addContext('selectRestaurant')


    def responseChooseRestaurantWithRestaurant(self, restaurant):
        #restauarante elegido, mostramos productos
        productList = database.searchProductsFromRestaurant(restaurant)
        self.restaurant = restaurant
        if len(productList) > 0 :
            self.bot.sendMessage(self.chat_id, 'Has elegido el restaurante ' + restaurant)

            # comprobamos si ya ha hecho un pedido anteriormente para mostrarle su opinion
            opinion = database.searchOpinionFromRestaurant(database.searchIDRestaurant(restaurant))
            if len(opinion) > 0:
                self.bot.sendMessage(self.chat_id, 'Tu última opinión de este restaurante fue: ' + str(opinion))

            self.bot.sendMessage(self.chat_id, 'Este restaurante tiene estos productos')

            # mostramos los productos
            i = 0
            for product in productList:
                i += 1
                self.bot.sendMessage(self.chat_id, str(i) + '. ' + product)

            self.bot.sendMessage(self.chat_id, 'Qué te apetece?🤤 Elige cada producto en una linea y avisame cuando termines '+
                                 'por favor😋')

            # añadimos contexto para dialogflow
            self.eatBotConversation.addContext('selectProduct')

            # creamos la lista de productos del pedido
            self.productOrder = []

        else:
            self.responseNotUnderstood()


    def responseChooseProduct(self, product):
        #producto elegido
        productId = database.searchIDProduct(product)
        if productId > -1:
            self.productOrder.append(productId)

        # añadimos contexto para dialogflow
        self.eatBotConversation.addContext('selectProduct')

    def responseFinishOrder(self):
        # pedido finalizado

        # guardamos en la bbdd el pedido
        database.insertOrder((self.chat_id, self.restaurant))

        idOrder = database.searchOrder(self.chat_id, self.restaurant)
        self.idLastOrder = idOrder

        for idProduct in self.productOrder:
             database.insertOrderProduct((idOrder, idProduct))

        self.bot.sendMessage(self.chat_id,'Tu pedido con identificador ' + str(idOrder) + ' se ha realizado con éxito.')
        self.bot.sendMessage(self.chat_id,'¿Qué te ha parecido la comida? Añade un comentario')

        # añadimos contexto para dialogflow
        self.eatBotConversation.addContext('makeOpinion')


    def responseMakeOpinion(self):
        #opinion del usuario
        opinion = self.eatBotConversation.getOpinion()
        database.insertOpinion((self.idLastOrder, opinion))
        self.bot.sendMessage(self.chat_id,'¡Gracias! Hemos guardado tu opinión correctamente.')



    def responseMakeOpinionYes(self):
        # acepta la sugerencia del restaurante
       self.responseChooseRestaurantWithRestaurant(self.restaurantNameSuggestion)


    def responseMakeOpinionNo(self):
        # no acepta la sugerencia del restaurante
        self.bot.sendMessage(self.chat_id, '¡Vaya! qué lástima, otra vez será...')



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


if __name__ == '__main__':

    #creamos instancia del bot
    eatbot = EatBot()