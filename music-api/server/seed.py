# server/seed.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server.db.database import db
from server.app import create_app
from server.models.songs import Song
from server.models.user import User
from server.models.mood import Mood
from server.models.genre import Genre
from server.models.artist import Artist
from server.models.music import Music
from services.spotify_service import SpotifyService
from server.models.mood import Mood, mood_song 


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
    return users

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

def link_songs_to_moods():
    from server.models.mood import Mood
    from server.models.songs import Song
    from server.db.database import db

    moods = Mood.query.all()
    songs = Song.query.limit(20).all()

    for mood in moods:
        for song in songs:
            if song not in mood.songs:
                mood.songs.append(song)
        print(f"Linked {len(mood.songs)} songs to mood: {mood.name}")

    db.session.commit()



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
        songs = seed_songs(moods, music)
        db.session.add_all(songs)
        db.session.commit()

        print("Linking songs to moods...")
        link_songs_to_moods()


        print(f"""
        Database seeded successfully!
        - Users: {len(users)}
        - Genres: {len(genres)}
        - Artists: {len(artists)}
        - Music: {len(music)}
        - Moods: {len(moods)}
        - Songs: {len(songs)}


        """)

if __name__ == "__main__":
    seed_database()
