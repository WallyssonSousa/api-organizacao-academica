from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

home = Blueprint('home', __name__) 

@home.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Welcome to Organização Acadêmica API"}), 200
