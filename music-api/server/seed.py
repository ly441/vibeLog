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
    
 def seed_music(artists, genres):
    from services.spotify_service import SpotifyService
    spotify = SpotifyService()

    search_queries = ['Happy', 'Sad', 'Energetic', 'Calm', 'Angry']
    music = []

    for query in search_queries:
        print(f"Searching for spotify tracks with query: {query}")
        results = spotify.search_track(query)
        print(f"Found {len(results)} tracks for query '{query}'")

        for track in results[:2]:
            print(f"Track: {track['name']} by {[a['name'] for a in track['artists']]}")
            artist_name = track['artists'][0]['name']
            artist = next((a for a in artists if a.name == artist_name), None)
            if not artist:
                artist = Artist(name=artist_name)
                db.session.add(artist)
                db.session.flush()
                artists.append(artist)

            music_track = Music(
                title=track['name'],
                duration=track['duration_ms'] // 1000,
                release_date=track['album']['release_date'],
                artist_id=artist.id,
                genre_id=random.choice([g.id for g in genres]),
                spotify_id=track['id']
            )
            db.session.add(music_track)
            db.session.flush()  #ensures music_track.id is populated
            music.append(music_track)

    print(f"Total music tracks seeded: {len(music)}")
    return music


def seed_moods(users):
    mood_names = ['Happy', 'Sad', 'Energetic', 'Calm', 'Angry']
    moods = []
    for _ in range(count):
        mood = Mood(
            name=fake.word().capitalize(),  # Random mood name
            intensity=random.randint(1, 10),  # Random intensity between 1-10
            description=fake.sentence(nb_words=5),
            user_id=random.choice(users).id
        )
        moods.append(mood)
    return moods


    

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
def seed_songs(moods, music):
    print("Seeding songs...")
    songs = []

    for music_item in music:
        if not music_item or not music_item.title:
            print("Skipping invalid music item:", music_item)
            continue  # skip empty or invalid entries

        song = Song(
            title=music_item.title,
            duration=music_item.duration,
            artist_id=music_item.artist_id,
            genre_id=music_item.genre_id,
            mood_id=random.choice(moods).id,
            spotify_id=music_item.spotify_id,
            music_id=music_item.id
        )
        songs.append(song)

    print(f"Total songs prepared for insert: {len(songs)}")
    return songs  # <-- make sure to return this








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