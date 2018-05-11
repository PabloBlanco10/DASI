from pyknow import *


class EatBotRules(KnowledgeEngine):

    @Rule(Fact(intent = 'tipoComida', restaurante = W()))
    def reglaTipoComida(self):
    #mostrar al usuario los tipos de comida
        print('Regla de tipo de comida')

    @Rule(Fact(intent='saludo', restaurante = W()))
    def reglaTipoComida(self):
        # mostrar al usuario los tipos de comida
        print('Regla de saludo')


