from flask import Blueprint, request, jsonify
from server.models.songs import Song
from server.models.music import Music
from server.db.database import db
from flask_jwt_extended import jwt_required

songs_bp = Blueprint('songs', __name__)

# CREATE song
@songs_bp.route('/songs', methods=['POST'])
@jwt_required()
def create_song():
    data = request.get_json()

    if not data or not all(k in data for k in ('title', 'duration', 'music_id')):
        return jsonify({'message': 'Missing required fields'}), 400

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
        'music_id': song.music_id,
        'spotify_id': song.spotify_id,
        'preview_url': song.preview_url,
    }), 201

# GET all songs
@songs_bp.route('/songs', methods=['GET'])
def get_all_songs():
    songs = Song.query.all()
    return jsonify([
        {
            'id': song.id,
            'title': song.title,
            'duration': song.duration,
            'music_id': song.music_id,
            'preview_url': song.preview_url,
            'image_url': song.image_url,
        } for song in songs
    ])

# GET single song
@songs_bp.route('/songs/<int:id>', methods=['GET'])
def get_song(id):
    song = Song.query.get(id)
    if not song:
        return jsonify({'message': 'Song not found'}), 404

    return jsonify({
        'id': song.id,
        'title': song.title,
        'duration': song.duration,
        'music_id': song.music_id,
        'image_url': song.image_url,
        "preview_url": song.preview_url
    })

# GET songs by artist
@songs_bp.route('/songs/artist/<int:artist_id>', methods=['GET'])
def get_songs_by_artist(artist_id):
    songs = Song.query.filter_by(artist_id=artist_id).all()

    return jsonify([
        {
            'id': s.id,
            'title': s.title,
            'duration': s.duration,
            'preview_url': s.preview_url,
            'genre_id': s.genre_id,
            'mood_id': s.mood_id,
            'music_id': s.music_id,
            'image_url': s.image_url,
            'preview_url':s.preview_url,

        } for s in songs
    ]), 200

# UPDATE song info
@songs_bp.route('/songs/<int:id>', methods=['PATCH'])
@jwt_required()
def update_song(id):
    song = Song.query.get(id)
    if not song:
        return jsonify({'message': 'Song not found'}), 404

    data = request.get_json()

    if 'title' in data:
        song.title = data['title']
    if 'duration' in data:
        song.duration = data['duration']
    if 'preview_url' in data:
        song.preview_url = data['preview_url']
    if 'image_url' in data:
        song.image_url = data['image_url']

    db.session.commit()

    return jsonify({
        'id': song.id,
        'title': song.title,
        'duration': song.duration,
        'preview_url': song.preview_url,
        'image_url': song.image_url
    }), 200
