from flask import Blueprint, jsonify, request
from .controllers import get_all_users, get_user_by_id, create_user, update_user, \
delete_user, get_all_tipo_inventario, get_all_tipo_dato, get_usuario_by_id, get_registro_inventario_by_id, \
get_all_registro_inventario_campos, get_tipo_inventario_by_id, create_registro_inventario, \
create_registro_inventario_campo, update_registro_inventario, delete_registro_inventario

main = Blueprint('main', __name__)

@main.route('/tipo_inventario', methods=['GET'])
def get_tipos_inventario():
    return jsonify(get_all_tipo_inventario())

@main.route('/tipo_inventario/<int:id_tipo_inv>', methods=['GET'])
def get_tipo_inventario(id_tipo_inv):
    return jsonify(get_tipo_inventario_by_id(id_tipo_inv))

@main.route('/tipo_dato', methods=['GET'])
def get_tipo_dato():
    return jsonify(get_all_tipo_dato())

@main.route('/usuarios/<int:id_user>', methods=['GET'])
def get_usuario(id_user):
    return jsonify(get_usuario_by_id(id_user))

@main.route('/registro_inventario/<int:id_registro>', methods=['GET'])
def get_registro_inventario(id_registro):
    return jsonify(get_registro_inventario_by_id(id_registro))

@main.route('/registro_inventario', methods=['POST'])
def add_registro_inventario():
    data = request.get_json()
    return jsonify(create_registro_inventario(data)), 201

@main.route('/registro_inventario/<int:id_registro>', methods=['PUT'])
def edit_registro_inventario(id_registro):
    data = request.get_json()
    return jsonify(update_registro_inventario(id_registro, data)), 200

@main.route('/registro_inventario_campos', methods=['GET'])
def get_registro_inventario_campos():
    return jsonify(get_all_registro_inventario_campos())

@main.route('/registro_inventario_campos', methods=['POST'])
def add_registro_inventario_campos():
    data = request.get_json()
    return jsonify(create_registro_inventario_campo(data, 5)), 201

@main.route('/registro_inventario/<int:id_registro>', methods=['DELETE'])
def eliminate_registro_inventario(id_registro):
    return jsonify(delete_registro_inventario(id_registro)), 204

