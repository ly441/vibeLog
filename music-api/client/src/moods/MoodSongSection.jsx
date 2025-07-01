import { useEffect, useState } from "react";

const MoodSongsSection = ({ mood }) => {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    const fetchSongs = async () => {
      if (!mood) return;

      try {
        const res = await fetch(`http://localhost:5000/moods/${mood.id}/songs`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!res.ok) {
          const errorText = await res.text();
          throw new Error(`HTTP ${res.status}: ${errorText}`);
        }

        const data = await res.json();
        setSongs(data);
      } catch (err) {
        console.error("Failed to fetch mood songs:", err.message);
      }
    };

    fetchSongs();
  }, [mood]);

  if (!mood) return <p>Loading mood...</p>;
  if (songs.length === 0) return <p>No songs linked to this mood yet.</p>;

  return (
    <div>
      <h2>Songs for {mood.name}</h2>
      <ul>
        {songs.map((song) => (
          <li key={song.id}>
            <img src={song.image_url} alt={song.title} width={50} height={50} />
            <span>{song.title}</span>
            {song.preview_url && (
              <audio controls src={song.preview_url}>
                Your browser does not support the audio element.
              </audio>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MoodSongsSection;
