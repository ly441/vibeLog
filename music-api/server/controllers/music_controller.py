from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from server.models.music import Music
from server.models.artist import Artist
from server.models.genre import  Genre
from server import db
from services.spotify_service import SpotifyService

spotify = SpotifyService

#from services.spotify_service import SpotifyService



music_bp = Blueprint('music', __name__)
artist_bp = Blueprint('artist', __name__)
genre_bp = Blueprint('genre', __name__)
SpotifyService_bp = Blueprint('spotify_service', __name__)

@music_bp.route('/track/<track_id>', methods=["GET"])
def get_track_info(track_id):
    try:
        track_data = spotify.get_track(track_id)
        return jsonify({
            "name": track_data["name"],
            "artist": track_data["artists"][0]["name"],
            "album": track_data["album"]["name"],
            "preview_url": track_data.get("preview_url"),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        spotify_results = Spotify.search_track(query)
        return jsonify(spotify_results), 200
    
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'artist': m.artist.name,
        'genre': m.genre.name if m.genre else None
    } for m in local_results]), 200

@artist_bp.route('/artists', methods=['GET'])
@jwt_required()
def get_artists():
    artists = Artist.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'spotify_id': a.spotify_id
    } for a in artists]), 200

@genre_bp.route('/genres', methods=['GET'])
@jwt_required()
def get_genres():
    genres = Genre.query.all()
    return jsonify([{
        'id': g.id,
        'name': g.name
    } for g in genres]), 200

@SpotifyService_bp.route('/spotify/search', methods=['GET'])
@jwt_required()
def search_spotify():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    results = SpotifyService.search_track(query)
    return jsonify(results), 200