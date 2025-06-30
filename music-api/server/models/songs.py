#from server import db
from server.db.database import db
from server.models.mood import Mood, mood_song

class Song(db.Model):
    __tablename__ = 'songs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer) 
    music_id = db.Column(db.Integer, db.ForeignKey('musics.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    spotify_id = db.Column(db.String(100))
    preview_url = db.Column(db.String)
    image_url = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    db.relationship('Music', backref='songs', lazy=True)
    db.relationship('Genre', backref='songs', lazy=True)
    db.relationship('Artist', backref='songs', lazy=True)
    