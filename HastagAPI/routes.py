from flask import redirect, render_template,request,session, url_for,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Nullable
from HastagAPI import app,db 
import json
from datetime import datetime
from time import sleep
from functools import wraps
 
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
    Dados = db.Column(db.String(250),nullable=False)
    Usuario = db.Column(db.String(25),nullable=False)


def Logado(funcao_original):
    @wraps(funcao_original)
    def wrapper(*args, **kwargs):
        try:
            a = session["usuario"]
        except:
            a = ""
        if a:
            resultado = funcao_original(*args, **kwargs)
        else:
            return redirect(url_for("Login"))
        return resultado
    return wrapper


@app.route("/EntradaDeWebhooks",methods=["POST"])
def Webhook():
    try:
        Dados = json.loads(request.data)
    except:
        Dados = None

    if Dados == None:
        return None
    else:
        Nome,Email,Status,Usuario= Dados["nome"],Dados["email"],Dados["status"],Dados["nome"]
        match Status:
            case 'aprovado':
                log = Webhooks()
                log.Evento=f"Sistema Liberou o acesso do cliente {Nome} que possui o email:{Email}!"
                log.Dados=str(Dados).replace("{","").replace("}","")
                log.Usuario = Usuario
                print("Seja bem vindo Impressionador(a)!")
            case 'recusado':
                log = Webhooks()
                log.Evento=f"Sistema Recusou o acesso do cliente {Nome} que possui o email:{Email}!"
                log.Dados=str(Dados).replace("{","").replace("}","")
                log.Usuario = Usuario
                print("Pagamento recusado.")
            case 'reembolsado':
                log = Webhooks()
                log.Evento=f"Sistema Retirou o acesso do cliente {Nome} que possui o email:{Email}!"
                log.Dados=str(Dados).replace("{","").replace("}","")
                Acesso = None
                log.Usuario = Usuario
            case _:
                log = Webhooks()
                log.Evento=f"Falha na tratativa"
                log.Dados=str(Dados).replace("{","").replace("}","")
                log.Usuario = Usuario
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
        try:
            email = (User.query.filter_by(email=(str(request.form["email"]).lower())).first()).email
        except:
            email = ""
        if Token != "uhdfaAADF123":
            return "Acesso Negado"
        elif "@" in email:
            return render_template("CadastroUsuario.html",Informacao = "Email já cadastrado!")
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
                return render_template("LoginUsuario.html",Informacao = "Senha Incorreta")
            elif str(senha) == str(usuarioDB.senha) and str(
                usuarioForm).lower().replace(" ","") == str(usuarioDB.email).lower().replace(" ",""):
                session["usuario"] = usuarioForm
                return redirect(url_for("BancoDeDados"))
        else:
            return render_template("LoginUsuario.html",Informacao = "Usuario Não Cadastrado")

@app.route("/BancoDeDados",methods=["POST","GET"])
@Logado
def BancoDeDados():
    if request.method == "GET":
        Logs = []
        for i in Webhooks.query.all():
            Logs.append((i.Usuario,i.Evento,i.Dados,str(i.Tempo)[:-7],i.id) )
        return render_template("TelaDB.html",Logs=Logs)
    else:
        usuario = request.form["Usuario"]
        Logs = []
        for i in Webhooks.query.filter_by(Usuario=usuario).all():
            Logs.append((i.Usuario,i.Evento,i.Dados,str(i.Tempo)[:-7],i.id) )
        return render_template("TelaDB.html",Logs=Logs)



    

