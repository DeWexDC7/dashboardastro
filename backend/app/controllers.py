from .models import Datos
from . import db

def get_all_users():
    users = Datos.query.all()
    return [{'id': user.id, 'nombre': user.nombre, 'direccion': user.direccion, 'telefono': user.telefono} for user in users]

def get_user_by_id(user_id):
    user = Datos.query.get_or_404(user_id)
    return {'id': user.id, 'nombre': user.nombre, 'direccion': user.direccion, 'telefono': user.telefono}

def create_user(data):
    new_user = Datos(nombre=data['nombre'], direccion=data['direccion'], telefono=data['telefono'])
    db.session.add(new_user)
    db.session.commit()
    return {'id': new_user.id, 'nombre': new_user.nombre, 'direccion': new_user.direccion, 'telefono': new_user.telefono}

def update_user(user_id, data):
    user = Datos.query.get_or_404(user_id)
    user.nombre = data['nombre']
    user.direccion = data['direccion']
    user.telefono = data['telefono']
    db.session.commit()
    return {'id': user.id, 'nombre': user.nombre, 'direccion': user.direccion, 'telefono': user.telefono}

def delete_user(user_id):
    user = Datos.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
