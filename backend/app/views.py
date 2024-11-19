from flask import Blueprint, jsonify, request
from .controllers import get_all_users, get_user_by_id, create_user, update_user, delete_user

main = Blueprint('main', __name__)

@main.route('/users', methods=['GET'])
def get_users():
    return jsonify(get_all_users())

@main.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(get_user_by_id(id))

@main.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    return jsonify(create_user(data)), 201

@main.route('/users/<int:id>', methods=['PUT'])
def modify_user(id):
    data = request.get_json()
    return jsonify(update_user(id, data))

@main.route('/users/<int:id>', methods=['DELETE'])
def remove_user(id):
    return delete_user(id)
