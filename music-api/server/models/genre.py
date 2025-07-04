
from server.db.database import db


class Genre(db.Model):
    __tablename__ = 'genres'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    musics = db.relationship('Music', backref='genre', lazy=True)