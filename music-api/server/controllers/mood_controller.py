from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.mood import Mood
from server.db.database import db

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
def toggle_mood():
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


@mood_bp.route('/moods/<int:id>', methods=['GET'])
@jwt_required()
def get_mood(id):
    user_id = get_jwt_identity()
    mood = Mood.query.filter_by(user_id=user_id, id=id).first()
    if not mood:
        return jsonify({'message': 'Mood not found'}), 404
    return jsonify({
        'id': mood.id,
        'name': mood.name,
        'intensity': mood.intensity,
        'description': mood.description,
        'created_at': mood.created_at.isoformat(),
        'song_count': len(mood.songs)
    }), 200

@mood_bp.route('/moods/<int:id>', methods=['PUT'])
@jwt_required()
def update_mood(id):
    user_id = get_jwt_identity()
    mood = Mood.query.filter_by(user_id=user_id, id=id).first()
    if not mood:
        return jsonify({'message': 'Mood not found'}), 404

    data = request.get_json()
    mood.name = data.get('name', mood.name)
    mood.intensity = data.get('intensity', mood.intensity)
    mood.description = data.get('description', mood.description)
    
    db.session.commit()
    return jsonify({'message': 'Mood updated successfully'}), 200

@mood_bp.route('/moods/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_mood(id):
    user_id = get_jwt_identity()
    mood = Mood.query.filter_by(user_id=user_id, id=id).first()
    if not mood:
        return jsonify({'message': 'Mood not found'}), 404
    
    db.session.delete(mood)
    db.session.commit()
    return jsonify({'message': 'Mood deleted successfully'}), 200    