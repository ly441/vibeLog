# server/seed.py

from server.db.database import db
from server.app import create_app

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.app import create_app
from server.db.database import db

from server.models.user import User
from server.models.mood import Mood
from server.models.genre import Genre
from server.models.artist import Artist
from server.models.music import Music
from server.models.songs import Song
from faker import Faker
import random
from datetime import datetime, timedelta


from services.spotify_service import SpotifyService

fake = Faker()
spotify = SpotifyService()


def seed_users(count=5):
    users = []
    for _ in range(count):
        user = User(
            username=fake.unique.user_name(),
            email=fake.unique.email()
        )
        user.set_password('password123')
        users.append(user)
    
    db.session.add_all(users)
    db.session.commit()  # Commit to save users and generate IDs

    return users



def seed_genres(count=5):
    genres = []
    for _ in range(count):
        genre = Genre(name=fake.unique.word().capitalize())
        genres.append(genre)
    
    db.session.add_all(genres)
    db.session.commit()
    return genres



def seed_artists(count=5):
    artists = []
    for _ in range(count):
        artist = Artist(name=fake.unique.name())
        artists.append(artist)

    db.session.add_all(artists)
    db.session.commit()
    return artists

def seed_moods(users, count=10):
    mood_names = ['Happy', 'Sad', 'Energetic', 'Calm', 'Angry']
    moods = []
    for _ in range(count):
        mood = Mood(
            name=random.choice(mood_names),
            intensity=random.randint(1, 10),
            description=fake.sentence(nb_words=5),
            user_id=random.choice(users).id
        )
        moods.append(mood)
    
    db.session.add_all(moods)
    db.session.commit()
    return moods


def seed_music(artists, genres, count=10):
    musics = []
    for _ in range(count):
        music = Music(
            title=fake.sentence(nb_words=3).rstrip('.'),
            duration=random.randint(120, 360),
            release_date=fake.date_this_decade(),
            artist_id=random.choice(artists).id,
            genre_id=random.choice(genres).id,
            spotify_id=fake.uuid4().replace('-', '')[:22]
        )
        musics.append(music)
    
    db.session.add_all(musics)
    db.session.commit()
    return musics


def seed_songs(moods, music, genres, artists, count=20):
    songs = []
    for _ in range(count):
        song = Song(
            title=fake.sentence(nb_words=3).rstrip("."),
            duration=random.randint(120, 360),
            music_id=random.choice(music).id if music else None,
            mood_id=random.choice(moods).id if moods else None,
            genre_id=random.choice(genres).id if genres else None,
            artist_id=random.choice(artists).id if artists else None,
            spotify_id=fake.uuid4()
        )
        if song.title and song.genre_id and song.artist_id:
            songs.append(song)
    
    db.session.add_all(songs)
    db.session.commit()
    return songs


def seed_songs(music, moods, genres, artists, count=20):
    songs = []
    for _ in range(count):
        song = Song(
            title=fake.sentence(nb_words=3).rstrip("."),  # Random song title
            duration=random.randint(120, 360),  # Duration in seconds (2 to 6 minutes)
            music_id=random.choice(music).id if music else None,
            mood_id=random.choice(moods).id if moods else None,
            genre_id=random.choice(genres).id if genres else None,
            artist_id=random.choice(artists).id if artists else None,
            spotify_id=fake.uuid4(),  # Random UUID as a fake Spotify ID
        )

        # Only add if required fields are not None
        if song.title and song.genre_id and song.artist_id:
            songs.append(song)
    return songs

def seed_music(artists, genres, count=10):
    musics = []
    for _ in range(count):
        music = Music(
            title=fake.sentence(nb_words=3).rstrip('.'),
            duration=random.randint(120, 360),
            release_date=fake.date_this_decade(),
            artist_id=random.choice(artists).id,
            genre_id=random.choice(genres).id,
            spotify_id=fake.uuid4().replace('-', '')[:22]  # Simulating Spotify IDs
        )
        musics.append(music)
    return musics


def seed_database():
    app = create_app()
    with app.app_context():
        print("Dropping and recreating database...")
        db.drop_all()
        db.create_all()
        
        print("Seeding users...")
        users = seed_users()
        db.session.add_all(users)
        
        print("Seeding genres...")
        genres = seed_genres()
        db.session.add_all(genres)
        
        print("Seeding artists...")
        artists = seed_artists()
        db.session.add_all(artists)
        
        print("Seeding music (this may take a while as we query Spotify)...")
        music = seed_music(artists, genres)
        db.session.add_all(music)
        
        
        print("Seeding moods...")
        moods = seed_moods(users)
        db.session.add_all(moods)
        db.session.commit()

        
        print("Seeding songs...")
        songs = seed_songs(moods, music, genres, artists)
        db.session.add_all(songs)
        
        db.session.commit()
        print(f"""
        Database seeded successfully!
        - Users: {len(users)}
        - Genres: {len(genres)}
        - Artists: {len(artists)}
        - Music: {len(music)}
        - Moods: {len(moods)}
        - Songs: {len(songs)}
        """)

if __name__ == '__main__':
    seed_database()
    