import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [trackName, setTrackName] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Função para resumir números
  const formatStreams = (num) => {
    if (num >= 1_000_000_000) return (num / 1_000_000_000).toFixed(1) + "B";
    if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + "M";
    if (num >= 1_000) return (num / 1_000).toFixed(1) + "K";
    return num.toString();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!trackName.trim()) {
      setError("Digite o nome da música");
      return;
    }
    setError("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/similar_songs",
        { track_name: trackName }
      );
      setResults(response.data);
    } catch (err) {
      console.error("Erro ao buscar músicas:", err);
      setError("Erro ao buscar músicas. Veja o console para detalhes.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>Spotify Songs - Similaridade</h1>
      </header>

      <section className="form-section">
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Digite o nome da música"
            value={trackName}
            onChange={(e) => setTrackName(e.target.value)}
          />
          <button type="submit" className="btn-submit" disabled={!trackName.trim() || loading}>
            {loading ? "Buscando..." : "Buscar Músicas Similares"}
          </button>
        </form>
        {error && <p className="error">{error}</p>}
      </section>

      <section className="results-section">
        <h2>Músicas Similares</h2>
        <div className="cards-container">
          {results.length === 0 && !loading && <p>Nenhuma música encontrada ainda.</p>}
          {results.map((song, idx) => (
            <div className="song-card" key={idx}>
              <h3>{song.Track}</h3>
              <p><strong>Artista:</strong> {song.Artist}</p>
              <p><strong>Álbum:</strong> {song["Album Name"]}</p>
              <p><strong>Streams:</strong> {formatStreams(song["Spotify Streams"])}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;
