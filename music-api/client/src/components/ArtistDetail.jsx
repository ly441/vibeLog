// src/components/ArtistDetail.jsx
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "./ArtistDetail.css";

const ArtistDetail = () => {
  const { id } = useParams();
  const [artist, setArtist] = useState(null);
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    fetch(`/artists/${id}`)
      .then((res) => res.json())
      .then(data => {
        console.log("Artist details:", data);
        setArtist(data);
      })
      .catch(err => console.error("Failed to fetch artist", err));

    fetch(`/artist/${id}`)
      .then((res) => res.json())
      .then(data => {
        console.log("Songs for artist:", data);
        setSongs(data);
      })
      .catch(err => console.error("Failed to fetch artist songs", err));
  }, [id]);

  if (!artist) return <p>Loading artist...</p>;

  return (
    <div className="artist-detail">
      <h2>{artist.name}</h2>
      <img src={artist.image_url} alt={artist.name} width="200" />

      {/*Add the song section here*/}
      <div className="songs-section">
        <h3>Songs by {artist.name}</h3>
        {songs.length === 0 ? (
          <p>No songs found for this artist.</p>
        ) : (
          <ul>
            {songs.map((song) => (
              <li key={song.id}>
                <strong>{song.title}</strong> — {song.duration} sec
                {song.preview_url && (
                  <div>
                    <audio controls src={song.preview_url}>
                      Your browser does not support the audio tag.
                    </audio>
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default ArtistDetail;
