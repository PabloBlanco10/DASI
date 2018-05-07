from pyknow import *


class eatBotRules(KnowledgeEngine):

    # @Rule(Light(color='green'))
    # def green_light(self):
    #     print("Walk")
    #
    # @Rule(Light(color='red'))
    # def red_light(self):
    #     print("Don't walk")
    #
    # @Rule(AS.light << Light(color=L('yellow') | L('blinking-yellow')))
    # def cautious(self, light):
    #     print("Be cautious because light is", light["color"])


    def __init__(self):
        print('iniciando reglas')
