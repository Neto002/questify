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

    def __repr__(self):
        return f'Usuarios {self.nome}'

class Projetos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    integrantes = db.Column(db.String(255))
    tarefas = db.Column(db.String(255))
    gerente = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Projetos {self.nome}'

class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    pontos = db.Column(db.Integer, nullable=False)
    usuario = db.Column(db.Integer, nullable=False)
    prazo = db.Column(db.Date, nullable=False)
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

def createProject(nome, usuario):
    projeto = Projetos(nome=nome, integrantes=f"{usuario.id},", tarefas='', gerente=usuario.id)
    db.session.add(projeto)
    db.session.commit()

def createTask(nome, xp, pontos, usuario, prazo, projeto):
    task = Tarefas(nome=nome, xp=xp, pontos=pontos, usuario=usuario, prazo=prazo, projeto=projeto)
    db.session.add(task)
    project = Projetos.query.filter_by(id=projeto).first()
    project.tarefas += f"{task.id},"
    db.session.commit()

def allTasks(user):
    return Tarefas.query.filter_by(usuario=user.id)

def allUsers():
    return Usuarios.query.order_by(Usuarios.xp.desc()).all()

def loginUser(email, senha):
    usuario = Usuarios.query.filter_by(email=email, senha=senha).first()
    if usuario:
        return usuario
    else:
        return False

def updatePic(userID, image):
    user = Usuarios.query.filter_by(id=userID).first()
    user.profilePic = image

def allProjects():
    projetos = projetos.query.all()
    return projetos

def allMyProjects(user):
    projetos = Projetos.query.all()
    myProjects = []
    for i in projetos:
        membros = i.integrantes.split(",")
        for userId in membros:
            if str(user.id) == userId:
                myProjects.append(i)
    return myProjects

def deleteProject(id):
    projeto = Projetos.query.filter_by(id=id).first()
    db.session.delete(projeto)
    db.session.commit()

def deleteTarefa(id):
    task = Tarefas.query.filter_by(id=id).first()
    db.session.delete(task)
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
        tarefas = allTasks(session)
        newTarefas = []
        for tarefa in tarefas:
            projectName = Projetos.query.filter_by(id=tarefa.projeto).first().nome
            tarefa.proj = projectName
            newTarefas.append(tarefa)
        projetos = allMyProjects(session)
        for i in projetos:
            if i.tarefas == '':
                i.tarefas = 0
            else:
                i.tarefas = i.tarefas.split(',')
                count = 0
                for task in i.tarefas:
                    if task != "":
                        count += 1
                i.tarefas = count
        return render_template(
            "index.html",
            todo=newTarefas,
            projects=projetos,
            user=session,
            profilePic = session.profilePic,
            players = allUsers()
            )

@app.route("/rewards")
def rewards():
    global session
    if not session:
        return redirect(url_for("login"))
    else:
        return render_template("rewards.html", user=session)

@app.route("/profile")
def profile():
    global session
    if not session:
        return redirect(url_for("login"))
    else:
        return render_template("profile.html", user=session)

@app.route("/login")
def login():
    return render_template("login.html", user=session)

@app.route("/register")
def signup():
    return render_template("signup.html", user=session)

@app.route("/add_project", methods=["POST"])
def add_project():
    global session
    project_name = request.form.get("projectName")
    createProject(project_name, session)
    return redirect(url_for("index"))

@app.route("/edit_project", methods=["POST"])
def edit_project():
    global session
    id = request.form.get("id")
    print(id)
    nome = request.form.get("nome")
    project = Projetos.query.filter_by(id=id).first()
    project.nome = nome
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add_task", methods=["POST"])
def add_task():
    nome = request.form.get("titulo")
    xp = request.form.get("xp")
    pontos = request.form.get("pontos")
    usuario = request.form.get("usuario")
    prazo = request.form.get("prazo")
    projeto = request.form.get("projeto")
    createTask(nome, xp, pontos, usuario, prazo, projeto)
    return redirect("/")

@app.route("/cadastro", methods=["POST"])
def cadastro():
    createUser(request.form.get("nome"), request.form.get("sobrenome"), request.form.get("cargo"), request.form.get("email"), request.form.get("senha"), request.form.get("nascimento"))
    return redirect(url_for("login"))

@app.route("/login_user", methods=["POST"])
def login_user():
    global session
    email = request.form.get("email")
    senha = request.form.get("password")
    user = loginUser(email, senha)
    if user:
        session = user
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
    project = Projetos.query.filter_by(id=project_id).first()
    tasks = project.tarefas
    tasks = tasks.split(",")
    tasks.pop()
    for i in tasks:
        task = Tarefas.query.filter_by(id=int(i)).first()
        deleteTarefa(task.id)
    deleteProject(project_id)
    return redirect(url_for("index"))

@app.route("/profileUp", methods=["POST"])
def update_profile():
    global session
    user = loginUser(session.email, session.senha)
    if 'img' in request.files:
        img = request.files["img"]
        session.profilePic = f"{session.id}.profile.jpg"
        updatePic(session.id,session.profilePic)
        img.save(f"static/media/{session.id}.profile.jpg")
        db.session.commit()
        return redirect("/profile")
    else:
        return "Error: 400"

@app.route("/task_toggle/<taskId>")
def task_toggle(taskId):
    tarefa = Tarefas.query.filter_by(id=int(taskId)).first()
    user = Usuarios.query.filter_by(id=session.id).first()
    if tarefa.concluida:
        tarefa.concluida = False
        user.xp -= tarefa.xp
        user.pontos -= tarefa.pontos
    else:
        tarefa.concluida = True
        user.xp += tarefa.xp
        user.pontos += tarefa.pontos
    db.session.commit()
    return redirect("/")

def main():
    app.run(port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    main()
