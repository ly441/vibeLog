from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from server.models.artist import Artist
from server.db.database import db

artist_bp = Blueprint('artist', __name__)

@artist_bp.route('/artists', methods=['GET'])
@jwt_required()
def get_artists():
    artists = Artist.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'spotify_id': a.spotify_id,
        'image_url': a.image_url
    } for a in artists]), 200

@artist_bp.route('/artists/<int:id>', methods=['GET'])
def get_artist(id):
    artist = Artist.query.get_or_404(id)
    return jsonify({
        'id': artist.id,
        'name': artist.name,
        'spotify_id': artist.spotify_id,
        'image_url': artist.image_url
    }), 200



# Get all artists
@artist_bp.route('/artists', methods=['GET'])
@jwt_required()
def get_artists():
    artists = Artist.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'spotify_id': a.spotify_id
    } for a in artists]), 200

# Create new artist
@artist_bp.route('/artists', methods=['POST'])
@jwt_required()
def create_artist():
    data = request.get_json()
    
    # Validate required fields
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing required field: name'}), 400
    
    # Check for duplicate name
    if Artist.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Artist with this name already exists'}), 409

    new_artist = Artist(
        name=data['name'],
        spotify_id=data.get('spotify_id')  # Optional field
    )

    try:
        db.session.add(new_artist)
        db.session.commit()
        return jsonify({
            'id': new_artist.id,
            'name': new_artist.name,
            'spotify_id': new_artist.spotify_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get single artist by ID
@artist_bp.route('/artists/<int:artist_id>', methods=['GET'])
@jwt_required()
def get_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if not artist:
        return jsonify({'error': 'Artist not found'}), 404
    
    return jsonify({
        'id': artist.id,
        'name': artist.name,
        'spotify_id': artist.spotify_id
    }), 200

# Update artist
@artist_bp.route('/artists/<int:artist_id>', methods=['PUT'])
@jwt_required()
def update_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if not artist:
        return jsonify({'error': 'Artist not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields if provided
    if 'name' in data:
        # Check for name conflict with other artists
        if Artist.query.filter(Artist.id != artist_id, Artist.name == data['name']).first():
            return jsonify({'error': 'Another artist already has this name'}), 409
        artist.name = data['name']
    
    if 'spotify_id' in data:
        artist.spotify_id = data['spotify_id']

    try:
        db.session.commit()
        return jsonify({
            'id': artist.id,
            'name': artist.name,
            'spotify_id': artist.spotify_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete artist
@artist_bp.route('/artists/<int:artist_id>', methods=['DELETE'])
@jwt_required()
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if not artist:
        return jsonify({'error': 'Artist not found'}), 404
    
    try:
        db.session.delete(artist)
        db.session.commit()
        return jsonify({'message': 'Artist deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500    