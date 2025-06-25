from server.db.database import db
from datetime import datetime

class Mood(db.Model):
    __tablename__ = 'moods'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)  # happy, sad, etc.
    intensity = db.Column(db.Integer, nullable=False)  # 1-10
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    songs = db.relationship('Song', backref='mood', lazy=True)