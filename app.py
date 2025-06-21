import os
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# Cargar configuración
if 'WEBSITE_HOSTNAME' not in os.environ:
    print("Loading development config")
    app.config.from_object('azureproject.development')
else:
    print("Loading production config")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importar el modelo aquí después de crear db
from models import PixelCount

@app.route("/", methods=["GET"])
def index():
    pixel_counts = PixelCount.query.order_by(PixelCount.timestamp.desc()).all()
    return render_template("index.html", pixel_counts=pixel_counts)

@app.route("/add_pixel", methods=["POST"])
@csrf.exempt
def add_pixel():
    if not request.is_json:
        return {"error": "El cuerpo debe ser JSON"}, 400

    data = request.get_json()
    usuario = data.get("usuario")
    timestamp = data.get("timestamp")
    fichero = data.get("fichero")
    pixeles = data.get("pixeles")

    if not usuario or not timestamp or not fichero or not pixeles:
        return {"error": "Faltan campos"}, 400

    nuevo = PixelCount(
        usuario=usuario,
        timestamp=datetime.fromisoformat(timestamp),
        fichero=fichero,
        pixeles=pixeles
    )
    db.session.add(nuevo)
    db.session.commit()
    return {"id": nuevo.id}, 201

@app.route("/pixelcounts", methods=["GET"])
def index():
    try:
        pixel_counts = PixelCount.query.order_by(PixelCount.timestamp.desc()).all()
    except Exception as e:
        return f"<h1>❌ Error en index:</h1><pre>{str(e)}</pre>", 500
    return render_template("index.html", pixel_counts=pixel_counts)
def get_pixelcounts():
    registros = PixelCount.query.order_by(PixelCount.timestamp.desc()).all()
    return {
        "resultados": [
            {
                "id": p.id,
                "usuario": p.usuario,
                "timestamp": p.timestamp.isoformat(),
                "fichero": p.fichero,
                "pixeles": p.pixeles
            } for p in registros
        ]
    }

@app.route("/eliminar/<int:id>", methods=["POST"])
@csrf.exempt
def eliminar_pixelcount(id):
    registro = PixelCount.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()
