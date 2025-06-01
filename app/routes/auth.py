from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User
from app import db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_data()
    if not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Username and password are required"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 409
    
    hashed_password = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_data()
    if not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Username and password are required"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['username']):
        return jsonify({"msg": "Invalid username or password"}), 401
    
    token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=1))
    return jsonify({"msg": "Login successful", "token": token}), 200