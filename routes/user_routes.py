from flask import Blueprint, request, jsonify
from config import Config
from models import User
from app import db
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/create-secure', methods=['POST'])
def create_user():
    data = request.json
    if db.session.query(db.exists().where(User.username == data['username'])).scalar():
        return jsonify({'message': 'Username taken'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        name=data['name'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# Create a new user
@user_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    if db.session.query(db.exists().where(User.username == data['username'])).scalar():
        return jsonify({'message': 'Username taken'}), 409
    new_user = User(username=data['username'], name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/all', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "username": user.username,
        "name": user.name,
        "email": user.email
    } for user in users]), 200

# Get a user by username
@user_bp.route('/<string:username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'username': user.username, 'name': user.name, 'email': user.email, 'password': user.password, 'api-key': Config.API_KEY})

# Update email
@user_bp.route('/email/<string:username>', methods=['PUT'])
def update_email(username):
    data = request.get_json()
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'Email updated successfully'}), 200

# Update password
@user_bp.route('/password/<string:username>', methods=['PUT'])
def update_password(username):
    data = request.get_json()
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    user.password = data['password']
    db.session.commit()
    return jsonify({'message': 'Password updated successfully'}), 200

# Check if username is taken
@user_bp.route('/username/count/<string:username>', methods=['GET'])
def username_count(username):
    username_count = db.session.query(User).filter_by(username=username).count()
    if username_count == 0:
        return jsonify({'message': 'Username not taken'}), 200
    return jsonify({'message': 'Username is taken'}), 409

# Delete a user
@user_bp.route('/delete/<string:username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
