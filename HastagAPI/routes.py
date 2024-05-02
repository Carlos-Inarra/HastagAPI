from flask import redirect, render_template,request,session,jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from HastagAPI import app,db 
from requests import get, post
import json
from datetime import datetime
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Usuario = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(15),nullable=False)

class Webhooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Evento = db.Column(db.String(50), nullable=False)
    Tempo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    Dados = db.Column(db.String(250))

@app.route("/EntradaDeWebhooks",methods=["POST"])
def Webhooks():
    Dados = json.loads(request.data)
    Nome,Email,Status = Dados["nome"],Dados["email"],Dados["status"]
    match Status:
        case 'aprovado':
            log = Webhooks(Evento=f"Sistema Liberou o acesso do cliente {Nome} que possui o email:{Email}!",Dados=Dados)
            print("Seja bem vindo Impressionador(a)!")
        case 'recusado':
            log = Webhooks(Evento=f"Sistema Recusou o acesso do cliente {Nome} que possui o email:{Email}!",Dados=Dados)
            print("Pagamento recusado.")
        case 'reembolsado':
            log = Webhooks(Evento=f"Sistema Retirou o acesso do cliente {Nome} que possui o email:{Email}!",Dados=Dados)
            Acesso = None
        case _:
            log = Webhooks(Evento=f"Falha na tratativa",Dados=Dados)
            print(f"Status do pagamento desconhecido: {Status}")
    db.session.add(log)
    db.session.commit()

@app.route("/Cadastro",methods=["POST","GET"])
def Cadastro():
    if request.method == "GET":
        return render_template("CadastroUsuario.html")
    else:
        Token = str(request.form["token"])
        if Token != "uhdfaAADF123":
            log = Webhooks(Evento=f"Sistema negou o cadastro de um usuario que utilizou um token diferente do permitido!",dados=f"Token utilizado{Token}")
            db.session.add(log)
            db.session.commit()
            return "Acesso Negado"
        else:
            Usuario = str( request.form["usuario"])
            Senha = hash(request.form["Senha"])
            Email = str(request.form["email"])
            user = User(Usuario=Usuario, email=Email, senha=Senha,token = Token)
            db.session.add(user)
            db.session.commit()
            log = Webhooks(Evento=f"Usuario cadastrado com sucesso!",dados=f"Usuario:{Usuario},Email:{Email}")
            db.session.add(log)
            db.session.commit()
            redirect(url_for("Login"))

@app.route("/Login",methods=["POST","GET"])
def Login():
    if request.method == "GET":
        return render_template("LoginUsuario.html")
    else:
        usuarioForm = request.form["email_ou_usuario"]
        try:
            usuarioDB = User.query.filter_by(email=usuarioForm).first()
        except:
            usuarioDB = User.query.filter_by(Usuario=usuarioForm).first()
        if str(usuarioForm).lower().replace(" ","") != str(usuarioDB).lower().replace(" ",""):
            log = Webhooks(Evento=f"Tentativa de login sem suceso!",dados=f"{usuarioForm}")
            db.session.add(log)
            db.session.commit()
            return render_template("LoginUsuario.html",Informacao = "Usuario Não Cadastrado")
        elif hash(request.form["senha"]) != hash(User.query.filter_by(senha=usuarioForm).first()):
            log = Webhooks(Evento=f"Tentativa de login sem suceso!",dados=f"{usuarioForm}")
            db.session.add(log)
            db.session.commit()
            return render_template("LoginUsuario.html",Informacao = "Senha Incorreta")
        elif hash(request.form["senha"]) == hash(User.query.filter_by(senha=usuarioForm).first()) and str(
            usuarioForm).lower().replace(" ","") == str(usuarioDB).lower().replace(" ",""):
            log = Webhooks(Evento=f"Usuario logado com suceso!",dados=f"{usuarioForm}")
            db.session.add(log)
            db.session.commit()
            return redirect("BancoDeDados")


@app.route("/BancoDeDados",methods=["POST","GET"])
def BancoDeDados():
    return render_template("TelaDB.html")


    

