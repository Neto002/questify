import os
from flask import Flask, send_file, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html", todo=[["Tarefa 1",50,"Questify Front"],["Tarefa 2",30,"Questify Front"],["Tarefa 3",50,"Questify Back"],["Tarefa 4",30,"Questify Back"]])

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
