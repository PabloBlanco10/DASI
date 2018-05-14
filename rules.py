from pyknow import *


class EatBotRules(KnowledgeEngine):
    bot = None

    def get_bot(self, bot):
        self.bot = bot

    @Rule(Fact(intent='Default Fallback Intent'))
    def ruleNotUnderstood(self):
        # no te entiendo
        self.bot.responseNotUnderstood

    @Rule(Fact(intent='chooseFoodType'),
          Fact(foodType=MATCH.foodType))
    def ruleFoodTypeWithFoodType(self, foodType):
        # el usuario ya ha elegido el tipo de comida
        self.bot.responseFoodTypeWithFoodType


    @Rule(Fact(intent = 'chooseFoodType'),
          NOT(Fact(foodType=W())))
    def ruleFoodTypeWithoutFoodType(self):
    #mostrar al usuario los tipos de comida
        self.bot.responseFoodTypeWithoutFoodType


    @Rule(Fact(intent='greet'))
    def ruleGreet(self):
        # mostrar al usuario los tipos de comida
        name = self.bot.message['from']['first_name']
        self.bot.responseGreet(name)


    # @Rule(Fact(intent='chooseRestaurant', entities=None))
    # def ruleChooseRestaurant(self, restaurante):
    #     # mostrar al usuario los tipos de comida
    #     print('Regla de saludo')
    #     self.bot.response('Regla de saludo')
    #
    #
    # @Rule(Fact(intent='chooseRestaurant', entities=MATCH.restaurante))
    # def ruleChooseRestaurant(self, restaurante):
    #     # mostrar al usuario los tipos de comida
    #     print('Regla de saludo')
    #     self.bot.response('Regla de saludo')



