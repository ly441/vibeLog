from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from server.models.user import User
from server.db.database import db

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['POST'])
def signup():
    data = request.get_json()

    if not data or not all(field in data for field in ('username', 'email', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check for existing username or email
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 409

    # Create new user
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email
    }), 201


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not all(field in data for field in ('username', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({'access_token': access_token}), 200
