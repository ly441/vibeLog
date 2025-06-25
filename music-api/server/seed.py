# server/seed.py
from server.db.database import db
from server.app import create_app
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
    genres = [
        Genre(name='Pop'),
        Genre(name='Rock'),
        Genre(name='Hip Hop'),
        Genre(name='Electronic'),
        Genre(name='Jazz')
    ]
    return genres

def seed_artists():
    # Get real artists from Spotify
    spotify_artists = [
        'The Beatles', 'Taylor Swift', 'Kendrick Lamar',
        'Daft Punk', 'Miles Davis'
    ]
    
    artists = []
    for name in spotify_artists:
        artist = Artist(name=name)
        # In a real app, you'd look up the Spotify ID here
        artists.append(artist)
    return artists

def seed_music(artists, genres):
    # Get real tracks from Spotify
    search_queries = [
        'Happy', 'Sad', 'Energetic', 'Calm', 'Angry'
    ]
    
    music = []
    for query in search_queries:
        results = SpotifyService.search_track(query)
        for track in results['tracks'][:2]:  # Get first 2 tracks per query
            artist = next((a for a in artists if a.name in [ar['name'] for ar in track['artists']]), None)
            if not artist:
                continue
                
            music.append(Music(
                title=track['name'],
                duration=track['duration_ms'] // 1000,
                release_date=track['album']['release_date'],
                artist_id=artist.id,
                genre_id=random.choice([g.id for g in genres]),
                spotify_id=track['id']
            ))
    return music

def seed_moods(users):
    mood_names = ['Happy', 'Sad', 'Energetic', 'Calm', 'Angry']
    moods = []
    for user in users:
        for name in mood_names:
            moods.append(Mood(
                user_id=user.id,
                name=name,
                intensity=random.randint(1, 10),
                description=fake.sentence(),
                created_at=fake.date_time_between(start_date='-30d', end_date='now')
            ))
    return moods

def seed_songs(moods, music):
    songs = []
    for mood in moods:
        # Assign 1-3 random songs to each mood
        for _ in range(random.randint(1, 3)):
            song_music = random.choice(music)
            songs.append(Song(
                mood_id=mood.id,
                music_id=song_music.id
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
        
        print("Seeding songs...")
        songs = seed_songs(moods, music)
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