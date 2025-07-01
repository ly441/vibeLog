import { useEffect, useState } from "react";

const HappyMoodPage = () => {
  const [songs, setSongs] = useState([]);
  const [moodId, setMoodId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHappyMood = async () => {
      try {
        const res = await fetch("http://localhost:5000/moods", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!res.ok) throw new Error("Failed to fetch moods");

        const moods = await res.json();
        const happy = moods.find((m) => m.name === "Happy");

        if (happy) {
          setMoodId(happy.id);
        } else {
          setError("Happy mood not found");
        }
      } catch (err) {
        setError("Error fetching moods");
        console.error(err);
      }
    };

    fetchHappyMood();
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
      <h2>Happy Mood Songs</h2>
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

export default HappyMoodPage;
