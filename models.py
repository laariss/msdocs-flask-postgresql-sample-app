from sqlalchemy import Column, Integer, String, DateTime
from app import db  # Importa db desde app.py

class PixelCount(db.Model):
    __tablename__ = 'pixel_counts'
    id = Column(Integer, primary_key=True)
    usuario = Column(String(128), nullable=False)
    timestamp = Column(DateTime)
    fichero = Column(String(256), nullable=False)
    pixeles = Column(db.JSON)

    def __repr__(self):
        return f"<PixelCount usuario={self.usuario}, fichero={self.fichero}, timestamp={self.timestamp}, pixeles={self.pixeles}>"
