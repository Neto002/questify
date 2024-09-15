import os
from flask import Flask, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from secret import postgreURL

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("test.html", profilePic="https://imgs.search.brave.com/bxepz6yw_TXK-bBWpEPOD2GVYZqLSCs61buNCTprRaY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTQy/MDA5ODI0L3B0L2Zv/dG8vc2lsaG91ZXR0/ZS1vZi15b3VuZy13/b21hbi5qcGc_cz02/MTJ4NjEyJnc9MCZr/PTIwJmM9akN3WkNM/aU9KdDBaQUZWd2RO/eEtSQmZKSzMxWFZC/Vm9ZSDdPSlVTeHV5/dz0")

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
