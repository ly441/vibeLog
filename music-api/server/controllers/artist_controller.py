from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from server.models import Artist
from server import db

artist_bp = Blueprint('artist', __name__)

@artist_bp.route('/artists', methods=['GET'])
@jwt_required()
def get_artists():
    artists = Artist.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'spotify_id': a.spotify_id
    } for a in artists]), 200