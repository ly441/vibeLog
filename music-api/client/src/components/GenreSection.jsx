// src/components/GenreSection.jsx
import "./GenreSection.css";

const GenreSection = ({ genres }) => {
  return (
    <section className="genre-section">
      <h3>Explore Genres</h3>
      <div className="genre-list">
        {genres.map((genre) => (
          <div key={genre.id} className="genre-card">
            <span>{genre.name}</span>
          </div>
        ))}
      </div>
    </section>
  );
};

export default GenreSection;
