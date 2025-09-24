import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy as np

class MusicRecommender:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.tfidf_matrix = None
        self.vectorizer = None
        self._load_and_preprocess_data()

    def _load_and_preprocess_data(self):
        try:
            self.df = pd.read_csv(self.csv_path, encoding='iso-8859-1')
        except Exception as e:
            print(f"Erro ao carregar o CSV: {e}")
            return

        # Seleciona colunas relevantes e renomeia para facilitar
        self.df = self.df[[
            'Track', 
            'Album Name', 
            'Artist', 
            'Spotify Streams', 
            'Spotify Popularity', 
            'YouTube Views'
        ]].copy()
        
        self.df.rename(columns={
            'Track': 'musica',
            'Album Name': 'album',
            'Artist': 'artista',
            'Spotify Streams': 'streams_spotify',
            'Spotify Popularity': 'popularidade_spotify',
            'YouTube Views': 'views_youtube'
        }, inplace=True)

        # Limpa e converte colunas numéricas
        for col in ['streams_spotify', 'views_youtube']:
            self.df[col] = self.df[col].astype(str).str.replace('[$,.]', '', regex=True)
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
        
        self.df['popularidade_spotify'] = pd.to_numeric(self.df['popularidade_spotify'], errors='coerce').fillna(0)

        # Preenche valores ausentes em colunas de texto
        self.df['musica'].fillna('Desconhecida', inplace=True)
        self.df['album'].fillna('Desconhecido', inplace=True)
        self.df['artista'].fillna('Desconhecido', inplace=True)

        # Remove caracteres especiais e converte para minúsculas na busca busca
        self.df['musica_limpa'] = self.df['musica'].apply(self._clean_text)
        self.df['artista_limpo'] = self.df['artista'].apply(self._clean_text)
        self.df['album_limpo'] = self.df['album'].apply(self._clean_text)

        # Cria uma coluna combinada para o TF-IDF
        self.df['combinado'] = self.df['musica_limpa'] + ' ' + self.df['artista_limpo'] + ' ' + self.df['album_limpo']

        # Inicializa TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(stop_words=None) # Não remover stop words para nomes de músicas/artistas
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combinado'])

    def _clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r'[^a-z0-9\s]', '', text) # Remove caracteres especiais, mantém letras, números e espaços
        return text

    def recommend_music(self, query_music, top_n=5):
        query_music_cleaned = self._clean_text(query_music)
        
        # Encontra a música exata ou mais próxima na base de dados
        # Primeiro, ela tenta encontrar uma correspondência exata ou próxima na coluna
        match_index = self.df[self.df['musica_limpa'].str.contains(query_music_cleaned, na=False, case=False)].index
        
        if not match_index.empty:
            # Se houver correspondência, usa a primeira encontrada como base
            idx = match_index[0]
        else:
            # Se não houver correspondência direta, vetoriza a query e encontra a mais similar
            query_vec = self.vectorizer.transform([query_music_cleaned])
            cosine_similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            idx = cosine_similarities.argsort()[-1]
            
            # Se a similaridade for muito baixa, pode significar que a música não foi encontrada
            if cosine_similarities[idx] < 0.1: # Limiar de similaridade, pode ser ajustado
                return [] # Vai retorna lista vazia se não encontrar nada

        # Calcula similaridade de cosseno com todas as músicas
        cosine_similarities = cosine_similarity(self.tfidf_matrix[idx:idx+1], self.tfidf_matrix).flatten()
        
        # Obtem os índices das músicas mais similares (excluindo a própria música)
        similar_indices = cosine_similarities.argsort()[:-top_n-2:-1] # Exclui a própria música e pega top_n
        
        # Filtra por similaridade mínima para evitar recomendações irrelevantes
        similar_indices = [i for i in similar_indices if cosine_similarities[i] > 0.2 and i != idx] # Ajustar limiar

        recommendations = []
        for i in similar_indices:
            song = self.df.iloc[i]
            recommendations.append({
                'musica': song['musica'],
                'artista': song['artista'],
                'album': song['album'],
                'streams_spotify': int(song['streams_spotify'])
            })
        return recommendations

# Exemplo de uso (teste local)
if __name__ == '__main__':
    recommender = MusicRecommender("Songs_2024_00.csv") # Caminho relativo
    if recommender.df is not None:
        print('\nTestando recomendação para \'Flowers\':')
        recs = recommender.recommend_music('Flowers')
        for r in recs:
            print(r)
        
        print('\nTestando recomendação para \'MILLION DOLLAR BABY\':')
        recs = recommender.recommend_music('MILLION DOLLAR BABY')
        for r in recs:
            print(r)

        print('\nTestando recomendação para uma música inexistente:')
        recs = recommender.recommend_music('Musica Inexistente')
        if not recs:
            print('Nenhuma recomendação encontrada.')
        else:
            for r in recs:
                print(r)

        print('\nTestando recomendação para \'Not Like Us\':')
        recs = recommender.recommend_music('Not Like Us')
        for r in recs:
            print(r)

        print('\nTestando recomendação para \'i like the way you kiss me\':')
        recs = recommender.recommend_music('i like the way you kiss me')
        for r in recs:
            print(r)

        print('\nTestando recomendação para \'Houdini\':')
        recs = recommender.recommend_music('Houdini')
        for r in recs:
            print(r)

