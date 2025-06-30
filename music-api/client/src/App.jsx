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

const PRESET_MOODS = [
  "Happy", "Sad", "Energetic", "Calm", "Angry",
  "Romantic", "Moody", "Chill", "Upbeat", "Reflective"
];

const fetchWithToken = async (url, setter) => {
  const token = localStorage.getItem("token");
  if (!token) return;

  try {
    const res = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`HTTP ${res.status}: ${errorText}`);
    }

    const data = await res.json();
    setter(data);
  } catch (err) {
    console.error(`Error fetching from ${url}:`, err.message);
  }
};

const seedMoodsIfMissing = async () => {
  const token = localStorage.getItem("token");
  if (!token) return;

  try {
    const res = await fetch("http://localhost:5000/moods", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) return;

    const moods = await res.json();
    const existing = moods.map((m) => m.name.toLowerCase());

    for (const mood of PRESET_MOODS) {
      if (!existing.includes(mood.toLowerCase())) {
        await fetch("http://localhost:5000/moods", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ name: mood }),
        });
      }
    }
  } catch (err) {
    console.error("Error seeding moods:", err);
  }
};

function HomePage({ isAuthenticated, selectedMood, setSelectedMood }) {
  const [artists, setArtists] = useState([]);
  const [genres, setGenres] = useState([]);
  const [songs, setSongs] = useState([]);
  const [moods, setMoods] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/songs")
      .then(res => res.json())
      .then(data => setSongs(data))
      .catch(err => console.error("Failed to fetch songs:", err));

    const loadData = async () => {
      if (isAuthenticated) {
        await seedMoodsIfMissing();

        await fetchWithToken("http://localhost:5000/moods", (fetchedMoods) => {
          const uniqueMoods = [];
          const seen = new Set();

          for (const mood of fetchedMoods) {
            const name = mood.name.toLowerCase();
            if (!seen.has(name)) {
              seen.add(name);
              uniqueMoods.push(mood);
            }
          }

          setMoods(uniqueMoods);
        });

        fetchWithToken("http://localhost:5000/genres", setGenres);
        fetchWithToken("http://localhost:5000/artists", setArtists);
      }
    };

    loadData();
  }, [isAuthenticated]);

  const handleAddToMood = async (songId) => {
  if (!selectedMood) {
    alert("Please select a mood first.");
    return;
  }

  try {
    const res = await fetch(`http://localhost:5000/moods/${selectedMood.id}/songs`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ song_id: songId }),
    });

    if (!res.ok) throw new Error("Failed to add song");

    alert(`Song added to ${selectedMood.name} mood`);

    const data = await res.json();
    console.log("Add song response:", data)

    //Refetch moods after adding
    await fetchWithToken("http://localhost:5000/moods", (fetchedMoods) => {
      //setMoods(uniqueMoods);
      const uniqueMoods = [];
      const seen = new Set();

      for (const mood of fetchedMoods) {
        const name = mood.name.toLowerCase();
        if (!seen.has(name)) {
          seen.add(name);
          uniqueMoods.push(mood);
        }
      }

      console.log("Fetched moods:", fetchedMoods);
      setMoods(uniqueMoods);
    });

  } catch (err) {
    console.error("Error adding song:", err);
    alert("Failed to add song to mood.");
  }
};


  return (
    <main className="main-content">
      {isAuthenticated && (
        <MoodButtons moods={moods} onSelectMood={setSelectedMood} />
      )}
      <SongSection 
        songs={songs}
        moods={moods}
        handleAddToMood={handleAddToMood}
        selectedMood={selectedMood}
      />
      <ArtistSection artists={artists} />
      <GenreSection genres={genres} />
    </main>
  );
}

function App() {
  const [authModalVisible, setAuthModalVisible] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem("token"));
  const [selectedMood, setSelectedMood] = useState(null);

  const handleLoginSuccess = async () => {
    setIsAuthenticated(true);
    setAuthModalVisible(false);
    await seedMoodsIfMissing();
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
          <Route path="/moods/sad" element={<SadMoodPage />} />
          <Route path="/moods/happy" element={<HappyMoodPage />} />
          <Route path="/moods/chill" element={<ChillMoodPage />} />
          <Route path="/moods/angry" element={<AngryMoodPage />} />
          <Route path="/moods/romantic" element={<RomanticMoodPage />} />
          <Route path="/moods/moody" element={<MoodyMoodPage />} />
          <Route path="/moods/upbeat" element={<UpbeatMoodPage />} />
          <Route path="/moods/reflective" element={<ReflectiveMoodPage />} />
          <Route path="/moods/energetic" element={<EnergeticMoodPage />} />
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
