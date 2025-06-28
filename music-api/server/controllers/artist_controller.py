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