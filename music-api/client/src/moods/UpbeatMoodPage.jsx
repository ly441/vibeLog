// src/moods/UpbeatMoodPage.jsx
import { useEffect, useState } from "react";

const UpbeatMoodPage = () => {
  const [songs, setSongs] = useState([]);
  const [moodId, setMoodId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  
  useEffect(() => {
    const fetchMoods = async () => {
      try {
        const res = await fetch("http://localhost:5000/moods", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!res.ok) throw new Error("Failed to fetch moods");
        const moods = await res.json();

        const upbeat = moods.find((m) => m.name.toLowerCase() === "upbeat");
        if (upbeat) {
          setMoodId(upbeat.id);
        } else {
          setError("Upbeat mood not found");
        }
      } catch (err) {
        console.error(err);
        setError("Error fetching moods");
      }
    };
    fetchMoods();
  }, []);

  
  useEffect(() => {
    if (!moodId) return;
    const fetchSongs = async () => {
      setLoading(true);
      try {
        const res = await fetch(`http://localhost:5000/moods/${moodId}/songs`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!res.ok) throw new Error("Failed to fetch songs");
        const data = await res.json();
        setSongs(data);
      } catch (err) {
        console.error(err);
        setError("Error fetching songs");
      } finally {
        setLoading(false);
      }
    };
    fetchSongs();
  }, [moodId]);

  
  const handleDelete = async (songId) => {
    try {
      const res = await fetch(
        `http://localhost:5000/moods/${moodId}/songs/${songId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      if (!res.ok) throw new Error("Failed to delete song");
      setSongs((s) => s.filter((x) => x.id !== songId));
    } catch (err) {
      console.error(err);
      setError("Error deleting song");
    }
  };

  return (
    <div>
      <h2>Upbeat Mood Songs</h2>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {!loading && songs.length === 0 && <p>No songs in this mood yet.</p>}
      {songs.map((song) => (
        <div key={song.id}>
          <p>{song.title}</p>
          <audio controls src={song.preview_url} />
          <button onClick={() => handleDelete(song.id)}>Remove</button>
        </div>
      ))}
    </div>
  );
};

export default UpbeatMoodPage;
