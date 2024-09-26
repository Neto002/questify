import os
from flask import Flask, send_file, render_template, request, redirect, url_for
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

class Projetos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    integrantes = db.Column(db.String(255))
    tarefas = db.Column(db.String(255))

    def __repr__(self):
        return f'Projetos {self.nome}>'

with app.app_context():
    db.create_all()

def createUser(nome, email, senha):
    usuario = Usuarios(nome=nome, email=email, senha=senha, xp=0, nivel=1, pontos=0)
    db.session.add(usuario)
    db.session.commit()

def createProject(nome):
    projeto = Projetos(nome=nome, integrantes='', tarefas='')
    db.session.add(projeto)
    db.session.commit()

def allProjects():
    projetos = Projetos.query.all()
    return projetos

def table_exists(table_name):
    try:
        db.metadata.reflect(bind=db.engine)
        db.metadata.tables[table_name]
        return True
    except KeyError:
        return False

@app.route("/")
def index():
    #return f'{Projects()[0].nome}
    projetos = allProjects()
    for i in projetos:
        if i.tarefas == '':
            i.tarefas = 0
        else:
            i.tarefas = i.tarefas.split(', ')
            i.tarefas = len(i.tarefas)
    return render_template(
        "index.html",
        todo=[["Tarefa 1",50,"Questify Front",1],["Tarefa 2",30,"Questify Front",2],["Tarefa 3",50,"Questify Back",3],["Tarefa 4",30,"Questify Back",4]],
        projects=projetos
        )

@app.route("/missions")
def missions():
    return render_template("missions.html")

@app.route("/rewards")
def rewards():
    return render_template("rewards.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def signup():
    return render_template("signup.html")

@app.route("/add_project", methods=["POST"])
def add_project():
    project_name = request.form.get("projectName")
    createProject(project_name)
    return redirect(url_for("index"))

def main():
    app.run(port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    main()
