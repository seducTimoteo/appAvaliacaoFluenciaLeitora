from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models.models import User
from app.extensions import db
from app.services.transcription_service import process_audio_and_transcribe

bp = Blueprint('api', __name__)

@bp.route('/login', methods=['POST'])
def login():
    print("Headers Received:", request.headers)  # Debugging output
    print("Content-Type:", request.content_type)  # Specific debug for Content-Type

    if not request.content_type or 'application/json' not in request.content_type:
        return jsonify({'error': 'Unsupported Media Type', 'message': 'Content-Type must be application/json'}), 415

    data = request.get_json(force=True)  # Using force=True to ignore Content-Type header
    if not data:
        return jsonify({'error': 'Bad Request', 'message': 'No JSON data provided'}), 400

    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=True)
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@bp.route('/transcribe', methods=['POST'])
@login_required
def transcribe_audio_api():
    response, status_code = process_audio_and_transcribe(request)
    return response, status_code

@bp.route('/')
def index():
    return jsonify({
        'message': 'Welcome to the Fluency Assessment API',
        'usage': {
            'transcribe_audio': {
                'method': 'POST',
                'endpoint': '/transcribe',
                'description': 'Submit an audio file for transcription.',
                'required_fields': ['audio_file', 'reference_text', 'id_avaliacao'],
            }
        },
        'note': 'Please refer to the API documentation for more details.'
    })

@bp.route('/alunos', methods=['GET'])
@login_required
def list_alunos():
    alunos = User.query.all()
    return jsonify([{'id': aluno.id, 'nome': aluno.nome, 'cpf': aluno.cpf} for aluno in alunos])
