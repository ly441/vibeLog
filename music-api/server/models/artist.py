from server import db

class Artist(db.Model):
    __tablename__ = 'artists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    spotify_id = db.Column(db.String(100))
    musics = db.relationship('Music', backref='artist', lazy=True)