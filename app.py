from flask import Flask, render_template
from models import db, Imagen  # Asegúrate de tener este modelo configurado

app = Flask(__name__)

@app.route("/")
def index():
    imagenes = Imagen.query.all()
    return render_template("index.html", imagenes=imagenes)

if __name__ == "__main__":
    app.run()
