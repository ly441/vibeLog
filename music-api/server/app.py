from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from server.config import Config
from server.db.database import db
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)

    # Register blueprints - ADD ALL CONTROLLERS HERE
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    
    # Register blueprints - ADD ALL CONTROLLERS HERE
    from server.controllers.auth_controller import auth_bp
    from server.controllers.mood_controller import mood_bp
    from server.controllers.song_controller import song_bp
    from server.controllers.artist_controller import artist_bp
    from server.controllers.genre_controller import genre_bp
    from server.controllers.music_controller import music_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(song_bp)
    app.register_blueprint(artist_bp)
    app.register_blueprint(genre_bp)
    app.register_blueprint(music_bp)
    
    # ADD ERROR HANDLERS
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404
        
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {"error": "Internal server error"}, 500
    
    return app