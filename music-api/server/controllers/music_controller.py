from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from server.models import Music, Artist, Genre
from server import db


from server.services.spotify_service import SpotifyService
=======
from services.spotify_service import SpotifyService


from services.spotify_service import SpotifyService


music_bp = Blueprint('music', __name__)

@music_bp.route('/music', methods=['GET'])
@jwt_required()
def get_all_music():
    music_list = Music.query.all()
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'artist': m.artist.name,
        'genre': m.genre.name if m.genre else None
    } for m in music_list]), 200

@music_bp.route('/music/search', methods=['GET'])
@jwt_required()
def search_music():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    # Search in our database first
    local_results = Music.query.filter(Music.title.ilike(f'%{query}%')).limit(5).all()
    
    if not local_results:
        # Fall back to Spotify if no local results
        spotify_results = SpotifyService.search_track(query)
        return jsonify(spotify_results), 200
    
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'artist': m.artist.name,
        'genre': m.genre.name if m.genre else None
    } for m in local_results]), 200