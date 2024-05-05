from flask import redirect, render_template,request,session,jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from HastagAPI import app,db 
import json
from datetime import datetime
import time
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Usuario = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(15),nullable=False)

class Webhooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Evento = db.Column(db.String(250), nullable=False)
    Tempo = db.Column(db.DateTime, nullable=False, default=datetime.now())
    Dados = db.Column(db.String(250))

@app.route("/EntradaDeWebhooks",methods=["POST"])
def Webhook():
    try:
        Dados = json.loads(request.data)
    except:
        Dados = None

    if Dados == None:
        return None
    else:
        Nome,Email,Status = Dados["nome"],Dados["email"],Dados["status"]
        match Status:
            case 'aprovado':
                log = Webhooks()
                log.Evento=f"Sistema Liberou o acesso do cliente {Nome} que possui o email:{Email}!"
                log.Dados=Dados
                print("Seja bem vindo Impressionador(a)!")
            case 'recusado':
                log = Webhooks()
                log.Evento=f"Sistema Recusou o acesso do cliente {Nome} que possui o email:{Email}!"
                log.Dados=Dados
                print("Pagamento recusado.")
            case 'reembolsado':
                log = Webhooks()
                log.Evento=f"Sistema Retirou o acesso do cliente {Nome} que possui o email:{Email}!"
                log.Dados=Dados
                Acesso = None
            case _:
                log = Webhooks()
                log.Evento=f"Falha na tratativa"
                log.Dados=Dados
                print(f"Status do pagamento desconhecido: {Status}")
        db.session.add(log)
        db.session.commit()
        return "Dados Recebidos"

@app.route("/Cadastro",methods=["POST","GET"])
def Cadastro():
    if request.method == "GET":
        return render_template("CadastroUsuario.html")
    else:
        Token = str(request.form["token"])
        if Token != "uhdfaAADF123":
            log = Webhooks()
            log.Evento=f"Sistema negou o cadastro de um usuario que utilizou um token diferente do permitido!"
            log.dados=f"Token utilizado{Token}"
            db.session.add(log)
            db.session.commit()
            return "Acesso Negado"
        elif User.query.filter_by(email=(str(request.form["email"]).lower())).first() != None:
            log = Webhooks()
            log.Evento=f"Sistema negou o cadastro de um usuario que possuir cadastro!"
            email = request.form["email"]
            log.dados=f"email utilizado:{email}"
            db.session.add(log)
            db.session.commit()
            render_template("CadastroUsuario.html",Informacao = "Email já cadastrado!, você será redirecionado para a tela de login")
            time.sleep(5)
            return redirect(url_for("Login"))
        else:
            Usuario = str( request.form["usuario"])
            Senha = hash(request.form["Senha"])
            Email = str(request.form["email"]).lower()
            user = User()
            user.Usuario=Usuario
            user.email=Email
            user.senha=Senha
            user.token = Token
            db.session.add(user)
            db.session.commit()
            log = Webhooks()
            log.Evento=f"Usuario cadastrado com sucesso!"
            log.dados=f"Usuario:{Usuario},Email:{Email}"
            db.session.add(log)
            db.session.commit()
            return redirect(url_for("Login"))

@app.route("/Login",methods=["POST","GET"])
def Login():
    if request.method == "GET":
        return render_template("LoginUsuario.html")
    else:
        usuarioForm = request.form["email"]
        senha = hash(request.form["senha"])
        usuarioDB = User.query.filter_by(email=(str(usuarioForm).lower())).first()
        if usuarioDB != None:
            if  str(senha) != str(usuarioDB.senha):
                log = Webhooks()
                log.Evento=f"Tentativa de login sem suceso!"
                log.dados=f"{usuarioForm}"
                db.session.add(log)
                db.session.commit()
                return render_template("LoginUsuario.html",Informacao = "Senha Incorreta")
            elif str(senha) == str(usuarioDB.senha) and str(
                usuarioForm).lower().replace(" ","") == str(usuarioDB.email).lower().replace(" ",""):
                log = Webhooks()
                log.Evento=f"Usuario logado com suceso!"
                log.dados=f"{usuarioForm}"
                db.session.add(log)
                db.session.commit()
                return redirect(url_for("BancoDeDados"))
        else:
            log = Webhooks()
            log.Evento=f"Tentativa de login sem suceso!"
            log.dados=f"{usuarioForm}"
            db.session.add(log)
            db.session.commit()
            return render_template("LoginUsuario.html",Informacao = "Usuario Não Cadastrado")


@app.route("/BancoDeDados",methods=["POST","GET"])
def BancoDeDados():
    return render_template("TelaDB.html")


    

