from doctest import debug
from HastagAPI import app,db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

#Espero bastante que gostem do projeto, infelizmente só obtive tempo 
#neste domingo para fazer, então o visual (css e js) não será dos melhores masssssss
#espero que gostem
# Sou Fãnzão do Lira, ele com certeza foi uma das principais 
#inspirações para que eu  estudasse e trabalhase com tecnologia