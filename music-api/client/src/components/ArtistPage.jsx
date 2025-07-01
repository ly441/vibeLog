// src/components/ArtistsPage.jsx
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./ArtistPage.css";

const fetchWithToken = async (url, setter) => {
  const token = localStorage.getItem("token");
  if (!token) {
    console.warn("No token found");
    return;
  }

  try {
    const res = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      const error = await res.text();
      console.error(`Error ${res.status}:`, error);
      return;
    }

    const data = await res.json();
    setter(data);
  } catch (err) {
    console.error("Fetch failed:", err);
  }
};

const ArtistsPage = () => {
  const [artists, setArtists] = useState([]);

  useEffect(() => {
    fetchWithToken("http://localhost:5000/artists", setArtists);
  }, []);

  const fallbackImage = "https://via.placeholder.com/200x200?text=No+Image";

  return (
    <div className="artists-page">
      <h2>Artists</h2>
      <div className="artists-container">
        {Array.isArray(artists) &&
          artists.map((artist) => (
            <Link
              to={`/artist/${artist.id}`}
              key={artist.id}
              className="artist-card-link"
            >
              
              <div className="artist-card">
                <img
                  src={artist.image_url || fallbackImage}
                  alt={artist.name}
                  onError={(e) => (e.target.src = fallbackImage)}
                />
                <span>{artist.name}</span>
              </div>
            </Link>
          ))}
      </div>
    </div>
  );
};

export default ArtistsPage;
