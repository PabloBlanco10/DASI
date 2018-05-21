from pyknow import *


class EatBotRules(KnowledgeEngine):
    bot = None

    def setBot(self, bot):
        self.bot = bot


    @Rule(Fact(intent='Default Fallback Intent'))
    def ruleNotUnderstood(self):
        # no te entiendo
        self.bot.responseNotUnderstood()

    @Rule(Fact(intent='greet'))
    def ruleGreet(self):
        # saludar al usuario
        name = self.bot.message['from']['first_name']
        self.bot.responseGreet(name)

    @Rule(Fact(intent = 'chooseFoodType'),
          NOT(Fact(foodType=W())))
    def ruleFoodTypeWithoutFoodType(self):
    #mostrar al usuario los tipos de comida
        self.bot.responseFoodTypeWithoutFoodType()



    @Rule(Fact(intent='chooseFoodType'),
          Fact(foodType=MATCH.foodType))
    def ruleFoodTypeWithFoodType(self, foodType):
        # el usuario ya ha elegido el tipo de comida
        self.bot.responseFoodTypeWithFoodType(foodType)


    @Rule(Fact(intent='selectFoodType'),
          Fact(foodType=MATCH.foodType))
    def ruleFoodTypeSelectFoodType(self, foodType):
        # el usuario ya ha elegido el tipo de comida
        self.bot.responseFoodTypeWithFoodType(foodType)


    @Rule(Fact(intent='chooseRestaurant'),
          NOT(Fact(restaurant=W())))
    def ruleChooseRestaurantWithoutRestaurant(self):
        # mostrar al usuario los restaurantes
        self.bot.responseChooseRestaurantWithoutRestaurant()


    @Rule(Fact(intent='chooseRestaurant'),
          Fact(restaurant=MATCH.restaurant))
    def ruleChooseRestaurantWithRestaurant(self, restaurant):
        # mostrar al usuario el restaurante elegido y los productos que hay
        self.bot.responseChooseRestaurantWithRestaurant(restaurant)


    @Rule(Fact(intent='selectRestaurant'),
          Fact(restaurant=MATCH.restaurant))
    def ruleChooseRestaurantSelectRestaurant(self, restaurant):
        # el usuario ya ha elegido el tipo de comida
        self.bot.responseChooseRestaurantWithRestaurant(restaurant)

    @Rule(Fact(intent='chooseProduct'),
          Fact(product=MATCH.product))
    def ruleChooseProduct(self, product):
        # eleccion de producto
        self.bot.responseChooseProduct(product)

    @Rule(Fact(intent='confirmOrder'))
    def ruleFinishOrder(self):
        # confirmar pedido
        self.bot.responseFinishOrder()

    @Rule(Fact(intent='makeOpinion'))
    def ruleMakeOpinion(self):
        # hacer opinion
        self.bot.responseMakeOpinion()