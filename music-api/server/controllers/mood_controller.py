from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.mood import Mood

from server.models.songs import Song
from server.models.music import Music

from server.db.database import db

mood_bp = Blueprint('mood', __name__)
song_bp = Blueprint('song', __name__)
music_bp = Blueprint('music', __name__)

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
@song_bp.route('/songs', methods=['POST'])
@jwt_required()
def create_song():
    user_id = get_jwt_identity()
    data = request.get_json()

    song = Song(
        user_id=user_id,
        title=data['title'],
        artist=data['artist'],
        album=data['album'],
        genre=data['genre']
    )
    db.session.add(song)
    db.session.commit()

    return jsonify({
        'id': song.id,
        'title': song.title,
        'message': 'Song created successfully'
    }), 201

@music_bp.route('/music', methods=['POST'])
@jwt_required()
def create_music():
    user_id = get_jwt_identity()
    data = request.get_json()

    music = Music(
        user_id=user_id,
        title=data['title'],
        artist=data['artist'],
        album=data['album'],
        genre=data['genre']
    )
    db.session.add(music)
    db.session.commit()

    return jsonify({
        'id': music.id,
        'title': music.title,
        'message': 'Music created successfully'
    }), 201