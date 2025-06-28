#from server import db
from server.db.database import db


class Song(db.Model):
    __tablename__ = 'songs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer)  # in seconds
    music_id = db.Column(db.Integer, db.ForeignKey('musics.id'), nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    spotify_id = db.Column(db.String(100))
    preview_url = db.Column(db.String)
    image_url = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    db.relationship('Music', backref='songs', lazy=True)
    db.relationship('Mood', backref='songs', lazy=True)
    db.relationship('Genre', backref='songs', lazy=True)
    db.relationship('Artist', backref='songs', lazy=True)
    