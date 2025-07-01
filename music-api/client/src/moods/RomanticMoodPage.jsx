import { useEffect, useState } from "react";
import "./CalmMood.css"; // Use shared styling if available

const RomanticMoodPage = () => {
  const [mood, setMood] = useState(null);
  const [songs, setSongs] = useState([]);
  const [error, setError] = useState("");

  // Step 1: Fetch Romantic mood
  useEffect(() => {
    const fetchMood = async () => {
      try {
        const res = await fetch("http://localhost:5000/moods", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch moods");

        const moods = await res.json();
        const romantic = moods.find((m) => m.name.toLowerCase() === "romantic");

        if (romantic) {
          setMood(romantic);
        } else {
          setError("Romantic mood not found.");
        }
      } catch (err) {
        console.error("Error fetching moods:", err);
        setError("Error fetching moods.");
      }
    };

    fetchMood();
  }, []);

  // Step 2: Fetch songs under Romantic mood
  useEffect(() => {
    if (!mood) return;

    const fetchSongs = async () => {
      try {
        const res = await fetch(`http://localhost:5000/moods/${mood.id}/songs`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch songs");

        const data = await res.json();
        setSongs(data);
      } catch (err) {
        console.error("Error fetching songs:", err);
        setError("Error fetching songs.");
      }
    };

    fetchSongs();
  }, [mood]);

  // Step 3: Handle delete
  const handleDelete = async (songId) => {
    try {
      const res = await fetch(`http://localhost:5000/moods/${mood.id}/songs/${songId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!res.ok) throw new Error("Failed to delete song");

      setSongs((prev) => prev.filter((s) => s.id !== songId));
    } catch (err) {
      console.error("Error deleting song:", err);
      setError("Error deleting song.");
    }
  };

  return (
    <div>
      <h1>Romantic Mood</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
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
              <button
                onClick={() => handleDelete(song.id)}
                style={{
                  marginTop: "8px",
                  background: "red",
                  color: "white",
                  border: "none",
                  padding: "5px 10px",
                  borderRadius: "4px",
                  cursor: "pointer",
                }}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RomanticMoodPage;
