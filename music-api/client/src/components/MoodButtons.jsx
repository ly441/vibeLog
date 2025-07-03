const API = import.meta.env.VITE_BACKEND_URL || "";

// src/components/MoodButtons.jsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./MoodButtons.css";

const PRESET_MOODS = [
  "Happy", "Sad", "Energetic", "Calm",
  "Angry", "Romantic", "Moody",
  "Chill", "Upbeat", "Reflective"
];

const fetchWithToken = async (url, method = "GET", body = null) => {
  const token = localStorage.getItem("token");
  if (!token) return [];

  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const res = await fetch(url, options);
  if (!res.ok) {
    const error = await res.text();
    console.error(`Error ${res.status}: ${error}`);
    return [];
  }

  return await res.json();
};

const MoodButtons = ({ onSelectMood }) => {
  const [selectedMoods, setSelectedMoods] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const loadMoods = async () => {
      const data = await fetchWithToken("${API}/moods");
      setSelectedMoods(data.map((m) => m.name));
    };
    loadMoods();
  }, []);

  const toggleMood = async (moodName) => {
    // Toggle mood selection in backend
    await fetchWithToken("${API}/moods", "POST", { name: moodName });

    // Fetch updated moods from backend
    const updated = await fetchWithToken("${API}/moods");
    setSelectedMoods(updated.map((m) => m.name));

    // Select full mood object to pass
    const fullMood = updated.find((m) => m.name === moodName);
    if (onSelectMood && fullMood) {
      onSelectMood(fullMood);
    }

    // Navigate to mood page
    navigate(`${API}/moods/${moodName.toLowerCase()}`);
  };

  return (
    <div className="mood-buttons">
      <h3>Select a Mood</h3>
      <div className="mood-list">
        {PRESET_MOODS.map((mood) => (
          <button
            key={mood}
            className={`mood-button ${selectedMoods.includes(mood) ? "selected" : ""}`}
            onClick={() => toggleMood(mood)}
          >
            {mood}
          </button>
        ))}
      </div>
    </div>
  );
};

export default MoodButtons;
