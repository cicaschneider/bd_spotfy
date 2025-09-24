// Elementos do DOM
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const resultsSection = document.getElementById('resultsSection');
const loadingSection = document.getElementById('loadingSection');
const emptyState = document.getElementById('emptyState');
const cardsContainer = document.getElementById('cardsContainer');
const resultsCount = document.getElementById('resultsCount');

// URL da API do backend Flask
const API_URL = 'http://localhost:5000/recommend';


// Estado da aplicação
let isLoading = false;

// Event listeners
searchButton.addEventListener('click', handleSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});

// Função principal de busca
async function handleSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        showError('Por favor, digite o nome de uma música.');
        return;
    }
    
    if (isLoading) {
        return;
    }
    
    try {
        isLoading = true;
        showLoading();
        
        const recommendations = await getRecommendations(query);
        
        if (recommendations && recommendations.length > 0) {
            showResults(recommendations, query);
        } else {
            showEmptyState();
        }
    } catch (error) {
        console.error('Erro ao buscar recomendações:', error);
        showError('Erro ao buscar recomendações. Verifique se o servidor está rodando e tente novamente.');
    } finally {
        isLoading = false;
    }
}

// Função para buscar recomendações da API
async function getRecommendations(query) {
    const response = await fetch(`${API_URL}?query=${encodeURIComponent(query)}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
}

// Função para mostrar loading
function showLoading() {
    hideAllSections();
    loadingSection.classList.add('show');
}

// Função para mostrar resultados
function showResults(recommendations, query) {
    hideAllSections();
    
    // Atualizar contador
    resultsCount.textContent = `${recommendations.length} recomendações encontradas`;
    
    // Limpar container
    cardsContainer.innerHTML = '';
    
    // Criar cards
    recommendations.forEach((music, index) => {
        const card = createMusicCard(music, index);
        cardsContainer.appendChild(card);
    });
    
    // Mostrar seção de resultados
    resultsSection.classList.add('show');
    
    // Scroll suave para os resultados
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Função para mostrar estado vazio
function showEmptyState() {
    hideAllSections();
    emptyState.classList.add('show');
}

// Função para esconder todas as seções
function hideAllSections() {
    resultsSection.classList.remove('show');
    loadingSection.classList.remove('show');
    emptyState.classList.remove('show');
}

// Função para criar card de música
function createMusicCard(music, index) {
    const card = document.createElement('div');
    card.className = 'music-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    const formattedStreams = formatNumber(music.streams_spotify);
    
    card.innerHTML = `
        <div class="card-header">
            <div class="music-icon">
                <i class="fas fa-music"></i>
            </div>
            <div class="card-title">
                <h3 class="music-title">${escapeHtml(music.musica)}</h3>
                <p class="music-artist">${escapeHtml(music.artista)}</p>
            </div>
        </div>
        <div class="card-content">
            <div class="music-album">
                <i class="fas fa-compact-disc"></i>
                <span>${escapeHtml(music.album)}</span>
            </div>
            <div class="music-streams">
                <i class="fab fa-spotify streams-icon"></i>
                <span class="streams-text">
                    <span class="streams-number">${formattedStreams}</span> streams no Spotify
                </span>
            </div>
        </div>
    `;
    
    // Adicionar animação de entrada
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        card.style.transition = 'all 0.5s ease';
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
    }, index * 100);
    
    return card;
}

// Função para formatar números
function formatNumber(num) {
    if (num >= 1000000000) {
        return (num / 1000000000).toFixed(1) + 'B';
    }
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Função de escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Função para mostrar erros
function showError(message) {

    // Criar toast de erro simples
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #e53e3e;
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(229, 62, 62, 0.3);
        z-index: 1000;
        font-weight: 500;
        max-width: 300px;
        animation: slideIn 0.3s ease;
    `;
    
    toast.innerHTML = `
        <i class="fas fa-exclamation-triangle" style="margin-right: 8px;"></i>
        ${message}
    `;
    
    document.body.appendChild(toast);
    
    // Remoção após 3 segundos
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Adiciono animações CSS dinamicas
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Foca no input de busca
    searchInput.focus();
    
    // Adicionar algumas sugestões de busca interativas
    const suggestions = ['Flowers', 'Houdini', 'Million Dollar Baby', 'Not Like Us'];
    let currentSuggestion = 0;
    
    // Placeholder animado 
    if (window.innerWidth > 768) {
        setInterval(() => {
            if (!searchInput.value && document.activeElement !== searchInput) {
                searchInput.placeholder = `Experimente buscar por "${suggestions[currentSuggestion]}\"...`;
                currentSuggestion = (currentSuggestion + 1) % suggestions.length;
            }
        }, 3000);
    }
});

