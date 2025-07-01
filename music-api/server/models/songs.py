from server.db.database import db
from server.models.mood import mood_song  # Only import the table, not Mood class!

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

    moods = db.relationship('Mood', secondary=mood_song, back_populates='songs')
    music = db.relationship('Music', back_populates='songs')
    genre = db.relationship('Genre', backref='songs')
    artist = db.relationship('Artist', backref='songs')
