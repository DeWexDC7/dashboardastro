from flask import Blueprint, jsonify, request
from .controllers import get_all_users, get_user_by_id, create_user, update_user, delete_user

main = Blueprint('main', __name__)

@main.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify(sorted(users, key=lambda user: user['id']))

@main.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = get_user_by_id(id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@main.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or not all(key in data for key in ('nombre', 'direccion', 'telefono')):
        return jsonify({'error': 'Invalid data'}), 400
    new_user = create_user(data)
    return jsonify(new_user), 201

@main.route('/users/<int:id>', methods=['PUT'])
def modify_user(id):
    data = request.get_json()
    updated_user = update_user(id, data)
    if updated_user:
        return jsonify(updated_user)
    return jsonify({'error': 'User not found'}), 404

@main.route('/users/<int:id>', methods=['DELETE'])
def remove_user(id):
    success = delete_user(id)
    if success:
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404
