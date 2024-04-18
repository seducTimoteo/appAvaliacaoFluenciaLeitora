from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from app.extensions import db
from app.models.models import User
import logging

# Create the blueprint for authentication
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth_login', methods=['POST'])  # Rename to avoid conflict
def auth_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=True)
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200
