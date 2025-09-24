# 🎶 Music Match: Recomendador de Músicas do Spotify

## ✨ Sobre o Projeto
O Music Match é um projeto de recomendação de músicas baseado em casos (RBC), desenvolvido para a disciplina de Inteligência Artificial. A ideia é criar um sistema que sugere novas faixas para usuários com base em suas preferências musicais, usando uma abordagem onde a similaridade entre novos casos (usuários com preferências específicas) é comparada a casos já existentes (histórico de usuários e playlists).
O sistema funciona em duas partes:   
  - Backend (Python): Responsável por processar os dados do Spotify e aplicar o algoritmo de RBC para gerar as recomendações.
  - Frontend (HTML, CSS, JS): Interface de usuário onde o usuário interage para receber as sugestões de músicas.
 
## 🚀 Tecnologias Utilizadas
 Backend
  - Linguagem de Programação: Python
  - Bibliotecas: Pandas, Scikit-learn, Numpy

 Frontend
  - Linguagens: HTML, CSS, JavaScript

## 📦 Estrutura de arquivos
```
bd_spotify/
backend/
 ├─ _pycache_/
 ├─ app
 ├─ backend_rcb
 ├─ Songs_2024_00.csv
frontend/
 ├─ venv/
 ├─ index.html
 ├─ script.js
 ├─ styles.css
venv/
 ├─ Include/
 ├─ Lib/
 ├─ Scripts/
 ├─ .gitgnore
 ├─ pyvenv
```

## 🛠 Como rodar o projeto

1. Configuração do Ambiente Python
   - Abra o terminal do VS Code
   - Crie um ambiente virtual 
   ```
   python -m venv venv
   ```
  - Ative o ambiente virtual
    No Windowns:
   ```
   .\venv\Scripts\activate
   ```
   No macOS/Linux:
   ````
   source venv/bin/activate
   ````
  - Verifique se (venv) aparece no início da linha de comando.
  - Instale as dependências (com o ambiente virtual ativo e selecionado)
   ```
   pip install pandas scikit-learn Flask Flask-Cors 
   ```
2. Iniciando o Backend (API Flask):
   - No Terminal (com o ambiente virtual ativado), navegue até a pasta backend:
   ```
   cd backend  
   ```
   - Execute o servidor Flask:
  ````
  python app.py
  ````
  - Você verá uma mensagem indicando que o servidor Flask está rodando em http://127.0.0.1:5000 ou http://0.0.0.0:5000.
3. Iniciando o Frontend (Servidor HTTP):
  - Abra um NOVO Terminal
  - Ative o ambiente virtual novamente neste novo terminal
  - Navegue até a pasta frontend:
    ```
    cd frontend
    ```
  - Inicie um servidor HTTP simples para servir os arquivos estáticos:
  ````
  python -m http.server 8000    
  ````
  - Você verá uma mensagem como Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/ ) ....

4. Acesse a Aplicação
   - Abra seu navegador web e acesse:
   ````
   http://localhost:8000
   ````
## 👨‍💻 Integrantes do Grupo

- Kauan Amélio Cipriani
- Guilherme Depiné Neto  	      
- Maria Cecilia	Schneider de Oliveira        
- Vitor Hugo Konzen	        
         
