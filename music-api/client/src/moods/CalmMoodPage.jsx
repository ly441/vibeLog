import { useEffect, useState } from "react";
import "./CalmMood.css";

const CalmMoodPage = () => {
  const [mood, setMood] = useState(null);
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    const fetchMood = async () => {
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        const res = await fetch("http://localhost:5000/moods", {
          headers: { Authorization: `Bearer ${token}` },
        });

        const moodList = await res.json();
        const calmMood = moodList.find((m) => m.name.toLowerCase() === "calm");
        if (calmMood) setMood(calmMood);
      } catch (err) {
        console.error("Failed to fetch moods:", err);
      }
    };

    fetchMood();
  }, []);

  useEffect(() => {
    if (!mood) return;

    const fetchSongs = async () => {
      const token = localStorage.getItem("token");
      try {
        const res = await fetch(`http://localhost:5000/moods/${mood.id}/songs`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        const data = await res.json();
        setSongs(data);
      } catch (err) {
        console.error("Failed to fetch mood songs:", err);
      }
    };

    fetchSongs();
  }, [mood]);

  // DELETE song from mood
  const handleDelete = async (songId) => {
    const token = localStorage.getItem("token");
    try {
      const res = await fetch(`http://localhost:5000/moods/${mood.id}/songs/${songId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.ok) {
        setSongs((prev) => prev.filter((song) => song.id !== songId));
      } else {
        console.error("Failed to delete song");
      }
    } catch (err) {
      console.error("Error deleting song:", err);
    }
  };

  return (
    <div>
      <h1>Calm Mood</h1>
      {songs.length === 0 ? (
        <p>No songs available for this mood yet.</p>
      ) : (
        <div className="mood-songs">
          {songs.map((song) => (
            <div key={song.id} className="song-card">
              <img
                src={song.image_url || "https://via.placeholder.com/150?text=No+Image"}
                alt={song.title}
                width={150}
                height={150}
                onError={(e) => (e.target.src = "https://via.placeholder.com/150?text=No+Image")}
              />
              <p>{song.title}</p>
              {song.preview_url ? (
                <audio controls src={song.preview_url}></audio>
              ) : (
                <p style={{ fontStyle: "italic", color: "#aaa" }}>No preview</p>
              )}

              {/*Delete Button */}
              <button onClick={() => handleDelete(song.id)} style={{ marginTop: "8px", background: "red", color: "white", border: "none", padding: "5px 10px", borderRadius: "4px", cursor: "pointer" }}>
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CalmMoodPage;
