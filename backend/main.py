from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware

# ------------------- FastAPI e CORS -------------------
app = FastAPI(title="Spotify 2024 Song Similarity")
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Carregar CSV -------------------
df = pd.read_csv('Songs_2024.csv', encoding='latin1')

df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
df.fillna({
    'Track': 'Unknown',
    'Album Name': 'Unknown',
    'Artist': 'Unknown',
    'Spotify Streams': 0,
    'Track Score': 0,
    'All Time Rank': 0
}, inplace=True)

num_cols = ['Spotify Streams', 'Track Score', 'All Time Rank']
for col in num_cols:
    df[col] = df[col].astype(str).str.replace(',', '').astype(float)

# ------------------- Preservar coluna original de Streams -------------------
df['Spotify Streams Original'] = df['Spotify Streams'].copy()

# ------------------- Codificação e normalização -------------------
le_track = LabelEncoder()
df['Track_encoded'] = le_track.fit_transform(df['Track'])

le_artist = LabelEncoder()
df['Artist_encoded'] = le_artist.fit_transform(df['Artist'])

scaler = MinMaxScaler()
df[['Spotify Streams', 'Track Score', 'All Time Rank']] = scaler.fit_transform(
    df[['Spotify Streams', 'Track Score', 'All Time Rank']]
)

features = ['Spotify Streams', 'Track Score', 'All Time Rank', 'Track_encoded', 'Artist_encoded']
cosine_sim = cosine_similarity(df[features])

# ------------------- Função para formatar números grandes -------------------
def format_streams(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f}B"
    elif n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    else:
        return str(int(n))

# ------------------- API -------------------
class SongRequest(BaseModel):
    track_name: str

@app.post("/similar_songs")
def similar_songs(request: SongRequest, top_n: int = 5):
    track_lower = request.track_name.strip().lower()
    matches = df[df['Track'].str.lower() == track_lower]

    if matches.empty:
        return {"error": "Track not found"}

    idx = matches.index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    indices = [i[0] for i in sim_scores]

    result = df.iloc[indices][['Track', 'Artist', 'Album Name', 'Spotify Streams Original']].copy()
    result['Spotify Streams'] = result['Spotify Streams Original'].apply(format_streams)
    result = result.drop(columns=['Spotify Streams Original'])

    return result.to_dict(orient='records')
