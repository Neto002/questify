import os
from flask import Flask, send_file, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    pontos = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Usuarios {self.nome}>'

with app.app_context():
    db.create_all()

def createUser(nome, email, senha):
    usuario = Usuarios(nome=nome, email=email, senha=senha, xp=0, nivel=1, pontos=0)
    db.session.add(usuario)
    db.session.commit()

def table_exists(table_name):
    try:
        db.metadata.reflect(bind=db.engine)
        db.metadata.tables[table_name]
        return True
    except KeyError:
        return False

@app.route("/")
def index():
    return render_template("index.html", todo=[[1,"Tarefa 1",50],[2,"Tarefa 2",30]])

# Suggested code may be subject to a license. Learn more: ~LicenseLog:2678314680.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:1603898920.
@app.route("/test")
def test():

    return f'{table_exists("usuarios")}'

@app.route("/missions")
def missions():
    return render_template("missions.html")

@app.route("/rewards")
def rewards():
    return render_template("rewards.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

def main():
    app.run(port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    main()
