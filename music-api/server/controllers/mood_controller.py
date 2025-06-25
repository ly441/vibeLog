from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.mood import Mood
from server import db

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/moods', methods=['GET'])
@jwt_required()
def get_moods():
    user_id = get_jwt_identity()
    moods = Mood.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'intensity': m.intensity,
        'description': m.description,
        'created_at': m.created_at.isoformat(),
        'song_count': len(m.songs)
    } for m in moods]), 200

@mood_bp.route('/moods', methods=['POST'])
@jwt_required()
def create_mood():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    mood = Mood(
        user_id=user_id,
        name=data['name'],
        intensity=data['intensity'],
        description=data.get('description', '')
    )
    db.session.add(mood)
    db.session.commit()
    
    return jsonify({
        'id': mood.id,
        'name': mood.name,
        'message': 'Mood created successfully'
    }), 201