from . import db

class Datos(db.Model):
    __tablename__ = 'datos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Datos {self.nombre}>'
