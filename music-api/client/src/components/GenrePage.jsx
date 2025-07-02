import { useEffect, useState } from "react";
import "./GenrePage.css";

const fetchWithToken = async (url, setter) => {
  const token = localStorage.getItem("token");

  if (!token) {
    console.warn("No token found in localStorage");
    setter([]); // Prevent crash
    return;
  }

  try {
    const res = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      const errorText = await res.text();
      console.error(`Fetch error ${res.status}:`, errorText);
      setter([]); // Prevent map crash
      return;
    }

    const data = await res.json();
    setter(data);
  } catch (err) {
    console.error("Fetch failed:", err);
    setter([]);
  }
};

const GenrePage = () => {
  const [genres, setGenres] = useState([]);

  useEffect(() => {
    fetchWithToken("/genres", setGenres);
  }, []);

  return (
    <div className="genre-page">
      <h2>Genres</h2>
      <div className="genre-list">
        {Array.isArray(genres) &&
          genres.map((genre) => (
            <div className="genre-card" key={genre.id}>
              {genre.name}
            </div>
          ))}
      </div>
    </div>
  );
};

export default GenrePage;
