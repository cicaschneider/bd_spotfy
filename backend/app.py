from flask import Flask, request, jsonify
from flask_cors import CORS
from backend_rcb import MusicRecommender

app = Flask(__name__)
CORS(app) # Habilita o CORS para permitir requisições do frontend

# Inicializa o recomendador de músicas com o caminho do CSV
# O CSV deve estar na mesma pasta do app.py após descompactar o ZIP
recommender = MusicRecommender("Songs_2024_00.csv")

@app.route("/recommend", methods=["GET"])
def recommend():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Parâmetro \'query\' é obrigatório."}), 400

    recommendations = recommender.recommend_music(query)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

