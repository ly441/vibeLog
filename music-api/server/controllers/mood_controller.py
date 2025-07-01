from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models.mood import Mood
from server.models.songs import Song
from server.db.database import db

mood_bp = Blueprint('mood', __name__)

PRESET_MOODS = [
    'Happy', 'Sad', 'Energetic', 'Calm', 'Angry',
    'Romantic', 'Moody', 'Chill', 'Upbeat', 'Reflective'
]

# GET all moods for a user
@mood_bp.route('/moods', methods=['GET'])
@jwt_required()
def get_moods():
    user_id = get_jwt_identity()
    moods = Mood.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            'id': m.id,
            'name': m.name,
            'intensity': m.intensity,
            'description': m.description,
            'created_at': m.created_at.isoformat(),
            'song_count': len(m.songs)
        } for m in moods
    ]), 200


# POST (create mood if it doesn't exist)
@mood_bp.route('/moods', methods=['POST'])
@jwt_required()
def create_mood():
    user_id = get_jwt_identity()
    data = request.get_json()

    name = data.get("name")
    if not name or name not in PRESET_MOODS:
        return jsonify({'error': 'Invalid or missing mood name'}), 400

    # Check if already exists
    mood = Mood.query.filter_by(user_id=user_id, name=name).first()
    if mood:
        return jsonify({
            'message': 'Mood already exists',
            'id': mood.id,
            'name': mood.name
        }), 200

    new_mood = Mood(
        user_id=user_id,
        name=name,
        intensity=data.get('intensity', 5),
        description=data.get('description', '')
    )
    db.session.add(new_mood)
    db.session.commit()

    return jsonify({
        'id': new_mood.id,
        'name': new_mood.name,
        'message': 'Mood created'
    }), 201


# Add a song to a mood
@mood_bp.route('/moods/<int:mood_id>/songs', methods=['POST'])
@jwt_required()
def add_song_to_user_mood(mood_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    song_id = data.get("song_id")

    mood = Mood.query.filter_by(id=mood_id, user_id=user_id).first()
    song = Song.query.get(song_id)

    if not mood or not song:
        return jsonify({"error": "Mood or Song not found"}), 404

    if song not in mood.songs:
        mood.songs.append(song)
        db.session.commit()

    return jsonify({
        "message": "Song added to mood",
        "mood_id": mood.id,
        "song_id": song.id
    }), 201


# GET all songs under a mood
@mood_bp.route('/moods/<int:mood_id>/songs', methods=['GET'])
@jwt_required()
def get_songs_for_mood(mood_id):
    user_id = get_jwt_identity()
    mood = Mood.query.filter_by(id=mood_id, user_id=user_id).first()

    if not mood:
        return jsonify({'error': 'Mood not found'}), 404

    return jsonify([
        {
            'id': song.id,
            'title': song.title,
            'duration': song.duration,
            'preview_url': song.preview_url,
            'image_url': song.image_url
        } for song in mood.songs
    ]), 200


# DELETE song from mood
@mood_bp.route('/moods/<int:mood_id>/songs/<int:song_id>', methods=['DELETE'])
@jwt_required()
def remove_song_from_mood(mood_id, song_id):
    user_id = get_jwt_identity()
    mood = Mood.query.filter_by(id=mood_id, user_id=user_id).first()

    if not mood:
        return jsonify({'error': 'Mood not found'}), 404

    song = Song.query.get(song_id)
    if not song:
        return jsonify({'error': 'Song not found'}), 404

    if song in mood.songs:
        mood.songs.remove(song)
        db.session.commit()

    return jsonify({'message': f'Song removed from {mood.name} mood'}), 200
