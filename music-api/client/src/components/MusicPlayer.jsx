// src/components/MusicPlayer.jsx
import { useEffect, useState } from "react";
import "./MusicPlayer.css";

const MusicPlayer = ({ selectedMood }) => {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    if (!selectedMood) return;

    const fetchSongs = async () => {
      try {
        const res = await fetch("http://localhost:5000/songs", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        const allSongs = await res.json();
        const moodSongs = allSongs.filter((song) => song.mood_id === selectedMood.id);
        setSongs(moodSongs);
      } catch (err) {
        console.error("Failed to load songs:", err);
      }
    };

    fetchSongs();
  }, [selectedMood]);

  return (
    <div className="music-player">
      <h3>{selectedMood ? `${selectedMood.name} Songs` : "Select a Mood to Play Music"}</h3>
      <ul>
        {songs.map((song) => (
          <li key={song.id}>
            <strong>{song.title}</strong>
            {song.preview_url && (
              <audio controls>
                <source src={song.preview_url} type="audio/mpeg" />
              </audio>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MusicPlayer;
