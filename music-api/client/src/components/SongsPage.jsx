// src/components/SongsPage.jsx
import { useEffect, useState } from "react";
import "./SongsPage.css";

const SongsPage = () => {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/songs")
      .then((res) => res.json())
      .then(setSongs)
      .catch((err) => console.error("Failed to fetch songs", err));
  }, []);

  const handleUpdate = async (songId, newTitle) => {
  await fetch(`http://localhost:5000/songs/${songId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify({ title: newTitle }),
  });
  
};


  return (
    <div className="songs-page">
      <h2>All Songs</h2>
      {songs.length === 0 ? (
        <p>No songs found.</p>
      ) : (
        <ul className="songs-list">
          {songs.map((song) => (
            <li key={song.id} className="song-card">
              {song.image_url && (
                <img
                src={song.image_url}
                alt={song.title}
                className="song-image"
                />
              )}
              <strong>{song.title}</strong> — {song.duration}s
              {song.preview_url && (
                <audio controls src={song.preview_url}></audio>

              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SongsPage;
