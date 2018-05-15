from pyknow import *


class EatBotRules(KnowledgeEngine):
    bot = None

    def setBot(self, bot):
        self.bot = bot


    @Rule(Fact(intent='Default Fallback Intent'))
    def ruleNotUnderstood(self):
        # no te entiendo
        self.bot.responseNotUnderstood()



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



    @Rule(Fact(intent='greet'))
    def ruleGreet(self):
        # saludar al usuario
        name = self.bot.message['from']['first_name']
        self.bot.responseGreet(name)



    @Rule(Fact(intent='chooseRestaurant'),
          Fact(restaurant=MATCH.restaurant))
    def ruleChooseRestaurant(self, restaurant):
        # mostrar al usuario el restaurante elegido y los productos que hay
        self.bot.responseChooseRestaurant(restaurant)



    @Rule(Fact(intent='chooseProduct'),
          Fact(product=MATCH.product))
    def ruleChooseProduct(self, product):
        # eleccion de producto
        self.bot.responseChooseProduct(product)

