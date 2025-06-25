from server.db.database import db

class Music(db.Model):
    __tablename__ = 'musics'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer)  # in seconds
    release_date = db.Column(db.Date)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    spotify_id = db.Column(db.String(100))
    songs = db.relationship('Song', backref='music', lazy=True)