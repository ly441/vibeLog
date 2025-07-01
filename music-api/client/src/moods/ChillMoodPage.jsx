import { useEffect, useState } from "react";

const ChillMoodPage = () => {
  const [songs, setSongs] = useState([]);
  const [moodId, setMoodId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchChillMood = async () => {
      try {
        const res = await fetch("http://localhost:5000/moods", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch moods");

        const moods = await res.json();
        const chill = moods.find((m) => m.name === "Chill");

        if (chill) {
          setMoodId(chill.id);
        } else {
          setError("Chill mood not found");
        }
      } catch (err) {
        setError("Error fetching moods");
        console.error(err);
      }
    };

    fetchChillMood();
  }, []);

  useEffect(() => {
    const fetchSongs = async () => {
      if (!moodId) return;

      try {
        setLoading(true);
        const res = await fetch(`http://localhost:5000/moods/${moodId}/songs`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch songs");

        const data = await res.json();
        setSongs(data);
        setLoading(false);
      } catch (err) {
        setError("Error fetching songs");
        console.error(err);
        setLoading(false);
      }
    };

    fetchSongs();
  }, [moodId]);

  const handleDelete = async (songId) => {
    try {
      const res = await fetch(`http://localhost:5000/moods/${moodId}/songs/${songId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      if (!res.ok) throw new Error("Failed to delete song");

      setSongs((prev) => prev.filter((s) => s.id !== songId));
    } catch (err) {
      setError("Error deleting song");
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Chill Mood Songs</h2>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {!loading && songs.length === 0 && <p>No songs found.</p>}
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

export default ChillMoodPage;
