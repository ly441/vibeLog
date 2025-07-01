from server.db.database import db
from datetime import datetime

# Join table
mood_song = db.Table(
    'mood_song',
    db.Column('mood_id', db.Integer, db.ForeignKey('moods.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'), primary_key=True)
)

class Mood(db.Model):
    __tablename__ = 'moods'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    intensity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    songs = db.relationship('Song', secondary=mood_song, back_populates='moods')
