from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from server.models.genre import Genre
from server.db.database import db

genre_bp = Blueprint('genre', __name__)

@genre_bp.route('/genres', methods=['GET'])
@jwt_required()
def get_genres():
    genres = Genre.query.all()
    return jsonify([{
        'id': g.id,
        'name': g.name
    } for g in genres]), 200