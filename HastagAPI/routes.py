from flask import render_template,request,session,jsonify
from HastagAPI import app
from requests import get, post
import json

def Enviar_mensagem(MSG):
    token = '6268128320:AAEo1u3Ib1Z5wc2o6MifNbIeP03CxXcuf54'
    url = f'https://api.telegram.org/bot{token}/SendMessage'
    id = 5127620212
    MSG = str(MSG)
    data = {'chat_id':id,'text':MSG}
    post(url,data)

@app.route("/EntradaDeWebhooks",methods=["POST"])
def Webhooks():
    # dados = json.dumps(str((request.data))[2:-1])
    dados = request.get_json()
    Enviar_mensagem(dados)
    return "Hello"

    

