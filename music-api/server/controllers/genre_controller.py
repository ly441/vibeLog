from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from server.models.genre import Genre
from server.db.database import db

genre_bp = Blueprint('genre', __name__)

    



# Get all genres
@genre_bp.route('/genres', methods=['GET'])
@jwt_required()
def get_genres():
    genres = Genre.query.all()
    return jsonify([{
        'id': g.id,
        'name': g.name
    } for g in genres]), 200

# Create new genre
@genre_bp.route('/genres', methods=['POST'])
@jwt_required()
def create_genre():
    data = request.get_json()
    
    # Validate required field
    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({'error': 'Genre name is required'}), 400
    
    name = data['name'].strip()
    
    # Check for duplicate genre
    if Genre.query.filter_by(name=name).first():
        return jsonify({'error': 'Genre already exists'}), 409
    
    try:
        new_genre = Genre(name=name)
        db.session.add(new_genre)
        db.session.commit()
        
        return jsonify({
            'id': new_genre.id,
            'name': new_genre.name
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get single genre by ID
@genre_bp.route('/genres/<int:genre_id>', methods=['GET'])
@jwt_required()
def get_genre(genre_id):
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({'error': 'Genre not found'}), 404
    
    return jsonify({
        'id': genre.id,
        'name': genre.name
    }), 200

# Update genre
@genre_bp.route('/genres/<int:genre_id>', methods=['PUT'])
@jwt_required()
def update_genre(genre_id):
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({'error': 'Genre not found'}), 404
    
    data = request.get_json()
    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({'error': 'Genre name is required'}), 400
    
    new_name = data['name'].strip()
    
    # Check if new name conflicts with existing genre
    existing_genre = Genre.query.filter(
        Genre.id != genre_id,
        Genre.name == new_name
    ).first()
    
    if existing_genre:
        return jsonify({'error': 'Genre name already exists'}), 409
    
    try:
        genre.name = new_name
        db.session.commit()
        
        return jsonify({
            'id': genre.id,
            'name': genre.name
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete genre
@genre_bp.route('/genres/<int:genre_id>', methods=['DELETE'])
@jwt_required()
def delete_genre(genre_id):
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({'error': 'Genre not found'}), 404
    
    try:
        db.session.delete(genre)
        db.session.commit()
        return jsonify({'message': 'Genre deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        # Handle potential foreign key constraint violations
        if "foreign key constraint" in str(e).lower():
            return jsonify({
                'error': 'Cannot delete genre as it is associated with existing content'
            }), 409
        return jsonify({'error': str(e)}), 500    