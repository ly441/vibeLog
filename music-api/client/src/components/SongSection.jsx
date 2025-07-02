import { useState, useRef } from "react";
import { FaPlus } from "react-icons/fa";
import "./SongSection.css";


const SongSection = ({ songs, moods }) => {
  const scrollRef = useRef();
  const fallbackImage = "https://via.placeholder.com/150?text=No+Image";
  const [selectedMoodBySong, setSelectedMoodBySong] = useState({});

  const scroll = (direction) => {
    const { current } = scrollRef;
    if (!current) return;
    current.scrollLeft += direction === "left" ? -300 : 300;
  };

  const handleMoodChange = (songId, moodId) => {
    setSelectedMoodBySong((prev) => ({ ...prev, [songId]: moodId }));
  };

  const handleAddToMood = async (songId) => {
    const moodId = selectedMoodBySong[songId];

    if (!moodId) {
      alert("Please select a mood first.");
      return;
    }

    try {
      const response = await fetch(`/moods/${moodId}/songs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({ song_id: songId }),
      });

      if (!response.ok) throw new Error("Failed to add song");

      alert("Song added to selected mood!");
    } catch (error) {
      console.error("Error adding song to mood:", error);
      alert("Could not add song.");
    }
  };

  return (
    <section className="song-section">
      <h3>Songs</h3>

      <div className="song-list-wrapper">
        <button className="arrow-button arrow-left" onClick={() => scroll("left")}>
          &#8249;
        </button>

        <div className="song-list" ref={scrollRef}>
          {songs.map((song) => (
            <div className="song-card" key={song.id}>
              <img
                src={song.image_url || fallbackImage}
                alt={song.title}
                className="song-image"
                onError={(e) => (e.target.src = fallbackImage)}
              />
              <p className="song-title">{song.title}</p>

              {song.preview_url ? (
                <audio controls>
                  <source src={song.preview_url} type="audio/mp3" />
                  Your browser does not support the audio tag.
                </audio>
              ) : (
                <p className="no-preview">No preview available</p>
              )}

              <select
                value={selectedMoodBySong[song.id] || ""}
                onChange={(e) => handleMoodChange(song.id, e.target.value)}
              >
                <option value="">Add to mood</option>
                {Array.isArray(moods) && moods.map((mood) => (
                  <option key={mood.id} value={mood.id}>
                    {mood.name}
                  </option>
                ))}
              </select>

              <button
                className="add-button"
                title="Add to selected mood"
                onClick={() => handleAddToMood(song.id)}
              >
                <FaPlus />
              </button>
            </div>
          ))}
        </div>

        <button className="arrow-button arrow-right" onClick={() => scroll("right")}>
          &#8250;
        </button>
      </div>
    </section>
  );
};

export default SongSection;
