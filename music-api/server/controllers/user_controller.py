from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from server.models.user import User
from server.db.database import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/signup', methods=['POST'])
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
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from server.models.user import User
from server.db.database import db

users_bp = Blueprint('users', __name__)

# CREATE (Signup)
@users_bp.route('/signup', methods=['POST'])
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

# READ (Login)
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not all(field in data for field in ('username', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200

# READ (Get All Users - Admin Only)
@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user.is_admin:
        return jsonify({'message': 'Admin access required'}), 403

    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin
    } for user in users]), 200

# READ (Get Single User)
@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    
    # Users can only view their own profile unless they're admin
    if int(current_user_id) != user_id:
        current_user = User.query.get(current_user_id)
        if not current_user.is_admin:
            return jsonify({'message': 'Unauthorized access'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin
    }), 200

# UPDATE (User Profile)
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    
    # Users can only update their own profile unless they're admin
    if int(current_user_id) != user_id:
        current_user = User.query.get(current_user_id)
        if not current_user.is_admin:
            return jsonify({'message': 'Unauthorized access'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    
    # Update username if provided and not taken
    if 'username' in data:
        if data['username'] != user.username and User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 409
        user.username = data['username']
    
    # Update email if provided and not taken
    if 'email' in data:
        if data['email'] != user.email and User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 409
        user.email = data['email']
    
    # Update password if provided
    if 'password' in data:
        user.set_password(data['password'])
    
    # Admin can update admin status
    if 'is_admin' in data:
        current_user = User.query.get(current_user_id)
        if current_user.is_admin:
            user.is_admin = data['is_admin']
        else:
            return jsonify({'message': 'Admin privileges required'}), 403

    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'message': 'User updated successfully'
    }), 200

# DELETE (User Account)
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Users can only delete their own account unless they're admin
    if int(current_user_id) != user_id and not current_user.is_admin:
        return jsonify({'message': 'Unauthorized access'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200