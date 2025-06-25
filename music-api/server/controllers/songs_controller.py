from flask import Blueprint, request, jsonify
from server.models.song import Song
from server.models.music import Music
from server.db.database import db
from flask_jwt_extended import jwt_required

songs_bp = Blueprint('songs', __name__)

@songs_bp.route('/songs', methods=['POST'])
@jwt_required()
def create_song():
    data = request.get_json()

    if not data or not all(k in data for k in ('title', 'duration', 'music_id')):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check that the music record exists
    music = Music.query.get(data['music_id'])
    if not music:
        return jsonify({'message': 'Music record not found'}), 404

    song = Song(title=data['title'], duration=data['duration'], music_id=data['music_id'])

    db.session.add(song)
    db.session.commit()

    return jsonify({
        'id': song.id,
        'title': song.title,
        'duration': song.duration,
        'music_id': song.music_id
    }), 201


@songs_bp.route('/songs', methods=['GET'])
def get_all_songs():
    songs = Song.query.all()
    return jsonify([
        {
            'id': song.id,
            'title': song.title,
            'duration': song.duration,
            'music_id': song.music_id
        } for song in songs
    ])


@songs_bp.route('/songs/<int:id>', methods=['GET'])
def get_song(id):
    song = Song.query.get(id)
    if not song:
        return jsonify({'message': 'Song not found'}), 404

    return jsonify({
        'id': song.id,
        'title': song.title,
        'duration': song.duration,
        'music_id': song.music_id
    })
