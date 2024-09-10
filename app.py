import os

from flask import Flask, send_file, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("tasks.html")

def main():
    app.run(port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    main()
