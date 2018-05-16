import apiai
import json


class EatBotConversation:

    def __init__(self):
        CLIENT_ACCESS_TOKEN = '0cec20af732f499ea4532ee576c35fcc'
        self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
        self.context = None


    def checkMessage(self, message):
        request = self.ai.text_request()
        request.lang = 'es'

        if self.context != None:
            request.resetContexts = False
            request.contexts = [self.context]
        else:
            request.resetContexts = True

        request.query = message

        response = json.loads(request.getresponse().read())

        result = response['result']
        action = result.get('action')
        metadata = result.get('metadata')
        intent = metadata.get('intentName')
        entities = result.get('parameters')

        print(intent)
        print(entities)

        if intent != 'Default Fallback Intent':
            self.context = None

        return intent, entities


    def addContext(self, context):
        self.context = context