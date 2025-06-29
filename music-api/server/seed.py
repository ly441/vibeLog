# server/seed.py


from server.db.database import db
from server.app import create_app

import sys


import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.app import create_app
from server.db.database import db

from server.models.user import User
from server.models.mood import Mood
from server.models.genre import Genre
from server.models.artist import Artist
from server.models.music import Music
from server.models.songs import Song
from services.spotify_service import SpotifyService

from faker import Faker
import random
from datetime import datetime

fake = Faker()
spotify = SpotifyService()


PRESET_MOODS = ['Happy', 'Sad', 'Energetic', 'Calm', 'Angry', 'Romantic', 'Focused', 'Chill', 'Excited', 'Melancholy']
DEFAULT_ARTIST_IMAGE = "https://via.placeholder.com/100?text=No+Image"


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

def seed_genres():
    genres = ['Pop', 'Rock', 'Hip Hop', 'Electronic', 'Jazz']
    return [Genre(name=name) for name in genres]

def seed_artists():
    artist_names = random.sample([
        'The Beatles', 'Taylor Swift', 'Kendrick Lamar', 'Daft Punk', 'Miles Davis',
        'Adele', 'Drake', 'Beyoncé', 'Radiohead', 'Eminem',
        'Coldplay', 'Bruno Mars', 'Lizzo', 'Doja Cat', 'Arctic Monkeys',
        'Billie Eilish', 'Ed Sheeran', 'Post Malone', 'SZA', 'Rihanna'
    ], 10)

    artists = []
    for name in artist_names:
        data = spotify.search_artist(name)
        spotify_id = data.get("id") if data else None
        image_url = data.get("images", [{}])[0].get("url", DEFAULT_ARTIST_IMAGE) if data else DEFAULT_ARTIST_IMAGE

        artists.append(Artist(name=name, spotify_id=spotify_id, image_url=image_url))
    return artists

def seed_music(artists, genres):
    music = []
    queries = PRESET_MOODS
    for query in queries:
        results = spotify.search_track(query)
        for track in results[:2]:
            artist_name = track["artists"][0]["name"]
            artist = next((a for a in artists if a.name == artist_name), None)
            if not artist:
                artist_data = spotify.search_artist(artist_name)
                if artist_data:
                    artist = Artist(
                        name=artist_name,
                        spotify_id=artist_data.get("id"),
                        image_url=artist_data.get("images", [{}])[0].get("url", DEFAULT_ARTIST_IMAGE)
                    )
                    db.session.add(artist)
                    db.session.flush()
                    artists.append(artist)

            music.append(Music(
                title=track["name"],
                duration=track["duration_ms"] // 1000,
                release_date=track["album"]["release_date"],
                artist_id=artist.id,
                genre_id=random.choice(genres).id,
                spotify_id=track["id"]
            ))
    return music

def seed_moods(users):
    moods = []
    for user in users:
        for mood in PRESET_MOODS:
            moods.append(Mood(
                user_id=user.id,
                name=mood,
                intensity=random.randint(1, 10),
                description=fake.sentence(),
                created_at=fake.date_time_between(start_date='-30d', end_date='now')
            ))
    return moods

def seed_songs(moods, music):
    songs = []
    for m in music:
        track = spotify.get_track(m.spotify_id)
        if not track:
            continue

        preview_url = track.get("preview_url")
        image_url = track.get("album", {}).get("images", [{}])[0].get("url", "https://via.placeholder.com/150")

        songs.append(Song(
            title=m.title,
            duration=m.duration,
            artist_id=m.artist_id,
            genre_id=m.genre_id,
            spotify_id=m.spotify_id,
            preview_url=preview_url,
            music_id=m.id,
            image_url=image_url
        ))
    return songs



def seed_database():
    app = create_app()
    with app.app_context():
        print("Dropping and recreating database...")
        db.drop_all()
        db.create_all()

        print("Seeding users...")
        users = seed_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding genres...")
        genres = seed_genres()
        db.session.add_all(genres)
        db.session.commit()

        print("Seeding artists...")
        artists = seed_artists()
        db.session.add_all(artists)
        db.session.commit()

        print("Seeding music (this may take a while)...")
        music = seed_music(artists, genres)
        db.session.add_all(music)

        
        

        db.session.commit()


        print("Seeding moods...")
        moods = seed_moods(users)
        db.session.add_all(moods)
        db.session.commit()


        


        print("Seeding songs...")
        songs = seed_songs(moods, music, genres, artists)
        db.session.add_all(songs)
        db.session.commit()

        print("Linking songs to moods...")
        for song in songs:
            random_moods = random.sample(moods, k=random.randint(1, 3))  # Link to 1–3 moods
            for mood in random_moods:
                mood.songs.append(song)

        db.session.commit()  # Commit mood-song associations

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
    

if __name__ == "__main__":
    seed_database()

