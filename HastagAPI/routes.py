from flask import render_template,request,session,jsonify
from HastagAPI import app
from requests import get, post

def Enviar_mensagem(MSG):
    token = '6268128320:AAEo1u3Ib1Z5wc2o6MifNbIeP03CxXcuf54'
    url = f'https://api.telegram.org/bot{token}/SendMessage'
    id = 5127620212
    MSG = str(MSG)
    data = {'chat_id':id,'text':MSG}
    post(url,data)

@app.route("/webhooks",methods=["GET","POST"])
def EstacaZero():
    dados = request.json
    print(dados)
    Enviar_mensagem(dados)
    return "Hello"

    

