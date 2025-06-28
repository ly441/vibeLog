import { useRef } from "react";
import "./ArtistSection.css";
import { Link } from "react-router-dom";

const ArtistSection = ({ artists }) => {
  const listRef = useRef(null);
  const fallbackImage = "https://via.placeholder.com/100?text=No+Image";

  const scroll = (direction) => {
    if (listRef.current) {
      listRef.current.scrollBy({
        left: direction === "left" ? -200 : 200,
        behavior: "smooth",
      });
    }
  };

  return (
    <section className="artist-section">
      <h3>Popular Artists</h3>
      <div className="artist-list-wrapper">
        <button className="arrow-button arrow-left" onClick={() => scroll("left")}>
          &#8592;
        </button>


        <div className="artist-list" ref={listRef}>
          {artists.map((artist) => (
            <Link
              to={`/artist/${artist.id}`}
              key={artist.id}
              className="artist-card-link"
            >

              
              <div className="artist-card">
                <img
                  src={artist.image_url || fallbackImage}
                  alt={artist.name}
                  className="artist-image"
                />
                <span>{artist.name}</span>
              </div>
            </Link>
          ))}
        </div>
        <button className="arrow-button arrow-right" onClick={() => scroll("right")}>
          &#8594;
        </button>
      </div>
    </section>
  );
};

export default ArtistSection;
