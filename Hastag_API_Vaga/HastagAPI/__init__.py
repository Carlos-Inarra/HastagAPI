from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY']='f3325d12c1df8cd9c8b41d4a'

from HastagAPI import routes