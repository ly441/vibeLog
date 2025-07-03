// src/App.jsx
import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import MoodButtons from "./components/MoodButtons";
import ArtistSection from "./components/ArtistSection";
import GenreSection from "./components/GenreSection";
import AuthModal from "./components/AuthModal";
import SongSection from "./components/SongSection";
import ArtistDetail from "./components/ArtistDetail";
import ArtistsPage from "./components/ArtistPage";
import GenrePage from "./components/GenrePage";
import SongsPage from "./components/SongsPage";
import CalmMoodPage from "./moods/CalmMoodPage";
import EnergeticMoodPage from "./moods/EnergeticMoodPage";
import SadMoodPage from "./moods/SadMoodPage";
import HappyMoodPage from "./moods/HappyMoodPage";
import AngryMoodPage from "./moods/AngryMoodPage";
import ChillMoodPage from "./moods/ChillMoodPage";
import RomanticMoodPage from "./moods/RomanticMoodPage";
import MoodyMoodPage from "./moods/MoodyMoodPage";
import UpbeatMoodPage from "./moods/UpbeatMoodPage";
import ReflectiveMoodPage from "./moods/ReflectiveMoodPage";

const API = import.meta.env.VITE_BACKEND_URL || "http://localhost:5000";
console.log("API:", API);

function HomePage({ isAuthenticated, selectedMood, setSelectedMood }) {
  const [artists, setArtists] = useState([]);
  const [genres, setGenres] = useState([]);
  const [songs, setSongs] = useState([]);
  const [moods, setMoods] = useState([]);

  useEffect(() => {
    fetch(`${API}/songs`)
      .then((res) => res.json())
      .then(setSongs)
      .catch((err) => console.error("Failed to fetch songs:", err));

    if (isAuthenticated) {
      Promise.all([
        fetch(`${API}/moods`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }),
        fetch(`${API}/genres`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }),
        fetch(`${API}/artists`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        }),
      ])
        .then(async ([moodsRes, genresRes, artistsRes]) => {
          const moodsData = await moodsRes.json();
          const genresData = await genresRes.json();
          const artistsData = await artistsRes.json();

          const uniqueMoods = [];
          const seen = new Set();
          for (const mood of moodsData) {
            const name = mood.name.toLowerCase();
            if (!seen.has(name)) {
              seen.add(name);
              uniqueMoods.push(mood);
            }
          }

          setMoods(uniqueMoods);
          setGenres(genresData);
          setArtists(artistsData);
        })
        .catch((err) => console.error("Failed to fetch protected data:", err));
    }
  }, [isAuthenticated]);

  return (
    <main className="main-content">
      {isAuthenticated && (
        <MoodButtons moods={moods} onSelectMood={setSelectedMood} />
      )}
      <SongSection
        songs={songs}
        moods={moods}
      />
      <ArtistSection artists={artists} />
      <GenreSection genres={genres} />
    </main>
  );
}

function App() {
  const [authModalVisible, setAuthModalVisible] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem("token")
  );
  const [selectedMood, setSelectedMood] = useState(null);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
    setAuthModalVisible(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
    setSelectedMood(null);
  };

  return (
    <Router>
      <div className="app dark-theme">
        <Navbar
          onLoginClick={() => setAuthModalVisible(true)}
          onLogout={handleLogout}
          isAuthenticated={isAuthenticated}
        />

        <Routes>
          <Route
            path="/"
            element={
              <HomePage
                isAuthenticated={isAuthenticated}
                selectedMood={selectedMood}
                setSelectedMood={setSelectedMood}
              />
            }
          />
          <Route path="/songs" element={<SongsPage />} />
          <Route path="/artist/:id" element={<ArtistDetail />} />
          <Route path="/artists" element={<ArtistsPage />} />
          <Route path="/genres" element={<GenrePage />} />
          <Route path="/moods/calm" element={<CalmMoodPage />} />
          <Route path="/moods/energetic" element={<EnergeticMoodPage />} />
          <Route path="/moods/sad" element={<SadMoodPage />} />
          <Route path="/moods/happy" element={<HappyMoodPage />} />
          <Route path="/moods/angry" element={<AngryMoodPage />} />
          <Route path="/moods/chill" element={<ChillMoodPage />} />
          <Route path="/moods/romantic" element={<RomanticMoodPage />} />
          <Route path="/moods/moody" element={<MoodyMoodPage />} />
          <Route path="/moods/upbeat" element={<UpbeatMoodPage />} />
          <Route path="/moods/reflective" element={<ReflectiveMoodPage />} />
        </Routes>

        {authModalVisible && (
          <AuthModal
            onClose={() => setAuthModalVisible(false)}
            onLoginSuccess={handleLoginSuccess}
          />
        )}
      </div>
    </Router>
  );
}

export default App;
