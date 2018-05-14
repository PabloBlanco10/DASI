import apiai
import json

CLIENT_ACCESS_TOKEN = '0cec20af732f499ea4532ee576c35fcc'

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

def checkMessage(message):
    request = ai.text_request()
    request.lang = 'es'

    request.query = message

    response = json.loads(request.getresponse().read())

    result = response['result']
    action = result.get('action')
    metadata = result.get('metadata')
    intent = metadata.get('intentName')
    entities = result.get('parameters')

    print(intent, entities)


    return intent, entities