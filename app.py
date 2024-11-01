import os
import random
import datetime
from crypt import methods

from flask import Flask, send_file, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import nullsfirst

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

session = None

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    nascimento = db.Column(db.Date, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    pontos = db.Column(db.Integer, nullable=False)
    profilePic = db.Column(db.String(255))
    saveCodes = db.Column(db.String(255))

    def __repr__(self):
        return f'Usuarios {self.nome}'

class Projetos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    integrantes = db.Column(db.String(255))
    tarefas = db.Column(db.String(255))

    def __repr__(self):
        return f'Projetos {self.nome}'

class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    projeto = db.Column(db.String(255), nullable=False)
    concluida = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Tarefas {self.nome}'

with app.app_context():
    db.create_all()

def createUser(nome, sobrenome, cargo, email, senha, nascimento):
    usuario = Usuarios(nome=nome, sobrenome=sobrenome, cargo=cargo, email=email, nascimento=nascimento, senha=senha, xp=0, nivel=1, pontos=0)
    db.session.add(usuario)
    db.session.commit()

def createProject(nome):
    projeto = Projetos(nome=nome, integrantes='', tarefas='')
    db.session.add(projeto)
    db.session.commit()

def createTask(nome, xp, projeto, concluida):
    task = Tarefas(nome=nome, xp=xp, projeto=projeto, concluida=concluida)
    db.session.add(task)
    db.session.commit()

def allTasks():
    return Tarefas.query.all()

def loginUser(email):
    usuario = Usuarios.query.filter_by(email=email).first()
    if usuario:
        return usuario
    else:
        return False

def allProjects():
    projetos = Projetos.query.all()
    return projetos

def deleteProject(id):
    projeto = Projetos.query.filter_by(id=id).first()
    db.session.delete(projeto)
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
    global session
    if not session:
        return redirect(url_for("login"))
    else:
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
            projects=projetos,
            user=session,
            profilePic = session.profilePic
            )

@app.route("/missions")
def missions():
    global session
    if not session:
        return redirect(url_for("login"))
    else:
        return render_template("missions.html")

@app.route("/rewards")
def rewards():
    global session
    if not session:
        return redirect(url_for("login"))
    else:
        return render_template("rewards.html")

@app.route("/profile")
def profile():
    global session
    if not session:
        return redirect(url_for("login"))
    else:
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

@app.route("/cadastro", methods=["POST"])
def cadastro():
    createUser(request.form.get("nome"), request.form.get("sobrenome"), request.form.get("cargo"), request.form.get("email"), request.form.get("senha"), request.form.get("nascimento"))
    return redirect(url_for("login"))

@app.route("/login_user", methods=["POST"])
def login_user():
    global session
    email = request.form.get("email")
    user = loginUser(email)
    if user:
        session = loginUser(user.email)
        return redirect(url_for("index"))
    else:
        return redirect("/login?error=login_error")

@app.route("/logout")
def logout():
    global session
    session = None
    return redirect(url_for("login"))

@app.route("/delete_project", methods=["POST"])
def delete_project():
    project_id = request.form.get("project_id")
    deleteProject(project_id)
    return redirect(url_for("index"))


@app.route("/update_task_status", methods=["POST"])
def update_task_status():
    task_id = request.json.get("task_id")
    status = request.json.get("status")
    tarefa = Tarefas.query.get(task_id)

    if tarefa:
        tarefa.concluida = status
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Tarefa não encontrada"}), 404

def main():
    app.run(port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    main()
