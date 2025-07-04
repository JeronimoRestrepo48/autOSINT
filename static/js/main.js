// 🔍 OSINT Searcher - JavaScript Mejorado
// Funcionalidad avanzada para la interfaz web en español

// Variables globales
let searchInProgress = false;
let currentSearchId = null;
let searchResults = [];
let chartInstances = {};

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 OSINT Searcher - Iniciando aplicación...');
    initializeApp();
    setupEventListeners();
    setupTooltips();
    console.log('✅ OSINT Searcher - Aplicación inicializada');
});

// Configuración inicial
function initializeApp() {
    // Configurar token CSRF si está disponible
    const csrfToken = document.querySelector('meta[name="csrf-token"]');
    if (csrfToken) {
        window.csrfToken = csrfToken.getAttribute('content');
    
    // Inicializar tema
    initializeTheme();
    
    // Configurar atajos de teclado
    setupKeyboardShortcuts();
}

// Configurar event listeners
function setupEventListeners() {
    // Formulario de búsqueda principal
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', handleSearchSubmit);
    }
    
    // Checkbox de dorking
    const dorkingCheckbox = document.getElementById('enable_dorking');
    const dorkingOptions = document.getElementById('dorkingOptions');
    
    if (dorkingCheckbox && dorkingOptions) {
        dorkingCheckbox.addEventListener('change', function() {
            if (this.checked) {
                dorkingOptions.classList.add('show');
                animateElement(dorkingOptions, 'fade-in');
            } else {
                dorkingOptions.classList.remove('show');
            }
        });
    }
    
    // Botón limpiar formulario
    const clearBtn = document.getElementById('clearForm');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearForm);
    }
    
    // Auto-detección de tipo de búsqueda
    const queryInput = document.getElementById('query');
    const searchTypeSelect = document.getElementById('search_type');
    
    if (queryInput && searchTypeSelect) {
        queryInput.addEventListener('input', function() {
            const value = this.value.toLowerCase().trim();
            autoDetectSearchType(value, searchTypeSelect);
        });
    }
    
    // Botones de exportación
    const exportButtons = document.querySelectorAll('[data-export]');
    exportButtons.forEach(button => {
        button.addEventListener('click', handleExport);
    });
}

// Manejar envío del formulario
async function handleSearchSubmit(event) {
    event.preventDefault();
    
    if (searchInProgress) {
        showNotification('Ya hay una búsqueda en progreso. Por favor espere.', 'warning');
        return;
    }
    
    const formData = new FormData(event.target);
    const searchData = prepareSearchData(formData);
    
    // Validar datos
    if (!validateSearchData(searchData)) {
        return;
    }
    
    await performSearch(searchData);
}

// Preparar datos de búsqueda
function prepareSearchData(formData) {
    const searchData = {
        query: formData.get('query').trim(),
        search_type: formData.get('search_type'),
        enable_dorking: formData.get('enable_dorking') === 'on',
        max_results: parseInt(formData.get('max_results')),
        language: formData.get('language'),
        date_range: formData.get('date_range'),
        risk_filter: formData.get('risk_filter')
    };
    
    // Obtener categorías de dorking si están habilitadas
    if (searchData.enable_dorking) {
        const dorkCategories = [];
        document.querySelectorAll('input[name="dork_categories"]:checked').forEach(cb => {
            dorkCategories.push(cb.value);
        });
        searchData.dork_categories = dorkCategories.length > 0 ? dorkCategories : ['general'];
    }
    
    return searchData;
}

// Validar datos de búsqueda
function validateSearchData(searchData) {
    if (!searchData.query) {
        showNotification('Por favor ingrese una consulta de búsqueda.', 'error');
        focusElement('query');
        return false;
    }
    
    if (searchData.query.length < 2) {
        showNotification('La consulta debe tener al menos 2 caracteres.', 'error');
        focusElement('query');
        return false;
    }
    
    if (searchData.enable_dorking && searchData.dork_categories.length === 0) {
        showNotification('Seleccione al menos una categoría de dorking.', 'warning');
        return false;
    }
    
    return true;
}

// Realizar búsqueda
async function performSearch(searchData) {
    searchInProgress = true;
    
    const resultsSection = document.getElementById('resultsSection');
    const searchProgress = document.getElementById('searchProgress');
    const searchResults = document.getElementById('searchResults');
    const searchBtn = document.getElementById('searchBtn');
    
    try {
        // Mostrar interfaz de búsqueda
        showElement(resultsSection);
        showElement(searchProgress);
        searchResults.innerHTML = '';
        
        // Actualizar botón
        updateSearchButton(searchBtn, true);
        
        // Simular progreso
        simulateProgress();
        
        // Realizar petición
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrfToken || ''
            },
            body: JSON.stringify(searchData)
        });
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            hideElement(searchProgress);
            displayResults(result.data);
            showNotification('Búsqueda completada exitosamente.', 'success');
        } else {
            throw new Error(result.error || 'Error desconocido en la búsqueda');
        }
        
    } catch (error) {
        console.error('Error en búsqueda:', error);
        hideElement(searchProgress);
        showErrorResults(error.message);
        showNotification(`Error: ${error.message}`, 'error');
    } finally {
        searchInProgress = false;
        updateSearchButton(searchBtn, false);
    }
}

// Mostrar resultados
function displayResults(data) {
    const searchResults = document.getElementById('searchResults');
    const results = data.results || [];
    
    if (results.length === 0) {
        showEmptyResults();
        return;
    }
    
    // Estadísticas
    const stats = calculateResultStats(results);
    
    // Crear HTML
    let html = createStatsHTML(stats) + createResultsListHTML(results);
    
    searchResults.innerHTML = html;
    animateElement(searchResults, 'fade-in');
    
    // Configurar eventos para resultados
    setupResultsEventListeners();
}

// Calcular estadísticas de resultados
function calculateResultStats(results) {
    return {
        total: results.length,
        highRisk: results.filter(r => r.risk_level === 'high').length,
        mediumRisk: results.filter(r => r.risk_level === 'medium').length,
        lowRisk: results.filter(r => r.risk_level === 'low').length,
        sources: [...new Set(results.map(r => r.source))],
        avgRelevance: results.reduce((sum, r) => sum + (r.relevance_score || 0), 0) / results.length
    };
}

// Crear HTML de estadísticas
function createStatsHTML(stats) {
    return `
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card text-center bg-primary text-white">
                    <div class="card-body">
                        <h3 class="display-6">${stats.total}</h3>
                        <p class="card-text">Total Resultados</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center bg-danger text-white">
                    <div class="card-body">
                        <h3 class="display-6">${stats.highRisk}</h3>
                        <p class="card-text">Alto Riesgo</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center bg-warning text-dark">
                    <div class="card-body">
                        <h3 class="display-6">${stats.mediumRisk}</h3>
                        <p class="card-text">Riesgo Medio</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center bg-success text-white">
                    <div class="card-body">
                        <h3 class="display-6">${stats.lowRisk}</h3>
                        <p class="card-text">Bajo Riesgo</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h5><i class="fas fa-list"></i> Resultados Detallados</h5>
            <div class="btn-group" role="group">
                <button type="button" class="btn btn-outline-primary btn-sm" onclick="exportResults('excel')">
                    <i class="fas fa-file-excel"></i> Excel
                </button>
                <button type="button" class="btn btn-outline-primary btn-sm" onclick="exportResults('pdf')">
                    <i class="fas fa-file-pdf"></i> PDF
                </button>
                <button type="button" class="btn btn-outline-primary btn-sm" onclick="exportResults('csv')">
                    <i class="fas fa-file-csv"></i> CSV
                </button>
            </div>
        </div>
    `;
}

// Crear HTML de lista de resultados
function createResultsListHTML(results) {
    let html = '';
    
    results.forEach((result, index) => {
        const riskClass = getRiskClass(result.risk_level);
        const riskBadge = getRiskBadge(result.risk_level);
        const sourceBadge = getSourceBadge(result.source);
        
        html += `
            <div class="card mb-3 result-card ${riskClass}" data-index="${index}">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="card-title mb-0">
                            <a href="${result.url}" target="_blank" class="text-decoration-none" rel="noopener noreferrer">
                                ${escapeHtml(result.title || 'Sin título')}
                                <i class="fas fa-external-link-alt ms-1" style="font-size: 0.8em;"></i>
                            </a>
                        </h6>
                        <div class="badges">
                            ${sourceBadge}
                            ${riskBadge}
                        </div>
                    </div>
                    <p class="card-text text-muted small mb-2">
                        <i class="fas fa-link"></i> ${result.url}
                    </p>
                    ${result.description ? `<p class="card-text">${escapeHtml(result.description)}</p>` : ''}
                    <div class="result-meta">
                        ${result.dork_used ? `
                            <small class="text-muted">
                                <strong><i class="fas fa-search"></i> Dork:</strong> 
                                <code>${escapeHtml(result.dork_used)}</code>
                            </small>
                        ` : ''}
                        ${result.relevance_score ? `
                            <small class="text-muted ms-3">
                                <strong><i class="fas fa-star"></i> Relevancia:</strong> 
                                ${(result.relevance_score * 100).toFixed(1)}%
                            </small>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    });
    
    return html;
}

// Funciones de utilidad para badges y clases
function getRiskClass(riskLevel) {
    const classes = {
        'high': 'high-risk',
        'medium': 'medium-risk',
        'low': 'low-risk'
    };
    return classes[riskLevel] || '';
}

function getRiskBadge(riskLevel) {
    const badges = {
        'high': '<span class="badge bg-danger"><i class="fas fa-exclamation-triangle"></i> Alto Riesgo</span>',
        'medium': '<span class="badge bg-warning text-dark"><i class="fas fa-exclamation-circle"></i> Riesgo Medio</span>',
        'low': '<span class="badge bg-success"><i class="fas fa-check-circle"></i> Bajo Riesgo</span>'
    };
    return badges[riskLevel] || '<span class="badge bg-secondary">Sin clasificar</span>';
}

function getSourceBadge(source) {
    const badges = {
        'google': '<span class="badge bg-primary"><i class="fab fa-google"></i> Google</span>',
        'bing': '<span class="badge bg-info"><i class="fab fa-microsoft"></i> Bing</span>',
        'duckduckgo': '<span class="badge bg-success"><i class="fas fa-search"></i> DuckDuckGo</span>',
        'google_dork': '<span class="badge bg-warning text-dark"><i class="fas fa-robot"></i> Google Dork</span>',
        'domain_analysis': '<span class="badge bg-secondary"><i class="fas fa-globe"></i> Análisis Dominio</span>',
        'ip_analysis': '<span class="badge bg-dark"><i class="fas fa-server"></i> Análisis IP</span>'
    };
    return badges[source] || `<span class="badge bg-light text-dark">${escapeHtml(source)}</span>`;
}

// Auto-detectar tipo de búsqueda
function autoDetectSearchType(value, selectElement) {
    if (!value) return;
    
    // Email
    if (value.includes('@') && value.includes('.')) {
        selectElement.value = 'email';
        return;
    }
    
    // IP
    if (/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(value)) {
        selectElement.value = 'ip';
        return;
    }
    
    // Dominio
    if (value.includes('.') && !value.includes(' ') && value.length > 3) {
        selectElement.value = 'domain';
        return;
    }
    
    // Si contiene espacios, probablemente sea empresa o persona
    if (value.includes(' ')) {
        if (value.toLowerCase().includes('corp') || 
            value.toLowerCase().includes('inc') || 
            value.toLowerCase().includes('ltd') ||
            value.toLowerCase().includes('s.a') ||
            value.toLowerCase().includes('empresa')) {
            selectElement.value = 'company';
        } else {
            selectElement.value = 'person';
        }
        return;
    }
}

// Funciones de utilidad
function showElement(element) {
    if (element) {
        element.style.display = 'block';
        element.classList.add('show');
    }
}

function hideElement(element) {
    if (element) {
        element.style.display = 'none';
        element.classList.remove('show');
    }
}

function animateElement(element, animationClass) {
    if (element) {
        element.classList.add(animationClass);
        setTimeout(() => element.classList.remove(animationClass), 500);
    }
}

function focusElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.focus();
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function updateSearchButton(button, isSearching) {
    if (!button) return;
    
    if (isSearching) {
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Buscando...';
    } else {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-search"></i> Iniciar Búsqueda';
    }
}

function clearForm() {
    const form = document.getElementById('searchForm');
    if (form) {
        form.reset();
    }
    
    const dorkingOptions = document.getElementById('dorkingOptions');
    if (dorkingOptions) {
        dorkingOptions.classList.remove('show');
    }
    
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        hideElement(resultsSection);
    }
    
    showNotification('Formulario limpiado.', 'info');
}

function simulateProgress() {
    const progressBar = document.querySelector('.progress-bar');
    if (!progressBar) return;
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress > 90) progress = 90;
        
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 90) {
            clearInterval(interval);
        }
    }, 500);
}

function showEmptyResults() {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.innerHTML = `
            <div class="alert alert-info text-center">
                <i class="fas fa-info-circle fa-2x mb-3"></i>
                <h5>No se encontraron resultados</h5>
                <p class="mb-0">
                    Intente con diferentes términos de búsqueda o active el Google Dorking 
                    para una búsqueda más exhaustiva.
                </p>
            </div>
        `;
    }
}

function showErrorResults(errorMessage) {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i>
                <strong>Error en la búsqueda:</strong> ${escapeHtml(errorMessage)}
                <hr>
                <p class="mb-0">
                    <small>
                        Verifique su conexión a internet y que los parámetros de búsqueda sean correctos.
                    </small>
                </p>
            </div>
        `;
    }
}

function showNotification(message, type = 'info') {
    // Crear notificación toast
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function setupResultsEventListeners() {
    // Configurar eventos para resultados si es necesario
    console.log('Configurando eventos para resultados...');
}

function setupTooltips() {
    // Configurar tooltips de Bootstrap si está disponible
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter para buscar
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const searchForm = document.getElementById('searchForm');
            if (searchForm && !searchInProgress) {
                searchForm.dispatchEvent(new Event('submit'));
            }
            e.preventDefault();
        }
        
        // Escape para limpiar
        if (e.key === 'Escape') {
            clearForm();
        }
    });
}

function initializeTheme() {
    // Detectar preferencia de tema del usuario
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (prefersDark) {
        document.body.classList.add('dark-theme');
    }
}

function handleExport(event) {
    const format = event.target.getAttribute('data-export');
    exportResults(format);
}

function exportResults(format) {
    if (searchResults.length === 0) {
        showNotification('No hay resultados para exportar.', 'warning');
        return;
    }
    
    showNotification(`Exportando resultados en formato ${format.toUpperCase()}...`, 'info');
    
    // Implementar lógica de exportación
    console.log(`Exportando en formato: ${format}`);
}

// Función global para realizar búsqueda (compatibilidad)
window.performSearch = async function(searchData) {
    if (typeof searchData === 'object') {
        await performSearch(searchData);
    } else {
        // Para compatibilidad con llamadas anteriores
        const form = document.getElementById('searchForm');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }
};

// Función global para exportar resultados
window.exportResults = exportResults;

console.log('🚀 OSINT Searcher JavaScript cargado completamente');

async function quickSearchHandler() {
    const query = document.getElementById('quickQuery').value.trim();
    const searchType = document.getElementById('quickSearchType').value;
    
    if (!query) {
        showNotification('Por favor ingresa una consulta', 'error');
        return;
    }
    
    const searchData = {
        query: query,
        search_type: searchType,
        sources: ['google', 'bing', 'duckduckgo'],
        max_results: 20
    };
    
    await performQuickSearch(searchData);
}

// Perform search
async function performSearch(searchData) {
    searchInProgress = true;
    showLoadingState('search');
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrfToken || ''
            },
            body: JSON.stringify(searchData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            currentSearchId = result.search_id;
            searchResults = result.results || [];
            
            displaySearchResults(result);
            showNotification('Búsqueda completada exitosamente', 'success');
            
            // Update history
            updateSearchHistory();
            
            // Update dashboard if on dashboard page
            if (window.location.pathname === '/dashboard' || window.location.pathname === '/') {
                setTimeout(loadDashboardData, 1000);
            }
        } else {
            throw new Error(result.message || 'Error en la búsqueda');
        }
        
    } catch (error) {
        console.error('Error en la búsqueda:', error);
        showNotification(`Error: ${error.message}`, 'error');
    } finally {
        searchInProgress = false;
        hideLoadingState('search');
    }
}

// Perform quick search
async function performQuickSearch(searchData) {
    const resultsContainer = document.getElementById('quickSearchResults');
    const loadingElement = resultsContainer.querySelector('.loading');
    const resultsElement = document.getElementById('resultsContainer');
    
    resultsContainer.style.display = 'block';
    loadingElement.style.display = 'block';
    resultsElement.style.display = 'none';
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.csrfToken || ''
            },
            body: JSON.stringify(searchData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            displayQuickSearchResults(result, resultsElement);
            showNotification('Búsqueda rápida completada', 'success');
        } else {
            throw new Error(result.message || 'Error en la búsqueda');
        }
        
    } catch (error) {
        console.error('Error en la búsqueda rápida:', error);
        resultsElement.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i>
                Error: ${error.message}
            </div>
        `;
    } finally {
        loadingElement.style.display = 'none';
        resultsElement.style.display = 'block';
    }
}

// Display search results
function displaySearchResults(result) {
    const resultsContainer = document.getElementById('searchResults');
    if (!resultsContainer) return;
    
    const results = result.results || [];
    const query = result.query || '';
    const searchType = result.search_type || 'general';
    
    let html = `
        <div class="search-results-header">
            <h3><i class="fas fa-search"></i> Resultados para "${query}"</h3>
            <div class="search-meta">
                <span class="badge badge-info">Tipo: ${searchType}</span>
                <span class="badge badge-success">${results.length} resultados</span>
                <span class="badge badge-secondary">ID: ${result.search_id}</span>
            </div>
        </div>
    `;
    
    if (results.length === 0) {
        html += `
            <div class="no-results">
                <i class="fas fa-search-minus"></i>
                <h4>No se encontraron resultados</h4>
                <p>Intenta con una consulta diferente o cambia las fuentes de búsqueda.</p>
            </div>
        `;
    } else {
        html += '<div class="results-grid">';
        
        results.forEach((item, index) => {
            html += createResultCard(item, index);
        });
        
        html += '</div>';
    }
    
    resultsContainer.innerHTML = html;
    
    // Add result animations
    animateResults();
}

// Display quick search results
function displayQuickSearchResults(result, container) {
    const results = result.results || [];
    const query = result.query || '';
    
    let html = `
        <div class="quick-results-header">
            <h4><i class="fas fa-bolt"></i> Resultados rápidos para "${query}"</h4>
            <span class="badge badge-success">${results.length} resultados</span>
        </div>
    `;
    
    if (results.length === 0) {
        html += `
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i>
                No se encontraron resultados para esta búsqueda.
            </div>
        `;
    } else {
        html += '<div class="quick-results-list">';
        
        results.slice(0, 5).forEach((item, index) => {
            html += createQuickResultItem(item, index);
        });
        
        html += '</div>';
        
        if (results.length > 5) {
            html += `
                <div class="quick-results-more">
                    <a href="/search?query=${encodeURIComponent(query)}" class="btn btn-primary">
                        <i class="fas fa-search-plus"></i> Ver todos los resultados (${results.length})
                    </a>
                </div>
            `;
        }
    }
    
    container.innerHTML = html;
}

// Create result card
function createResultCard(result, index) {
    const title = result.title || 'Sin título';
    const description = result.description || result.snippet || 'Sin descripción';
    const url = result.url || result.link || '#';
    const source = result.source || 'Desconocido';
    const timestamp = result.timestamp || new Date().toISOString();
    
    return `
        <div class="result-card" data-index="${index}">
            <div class="result-header">
                <h5><a href="${url}" target="_blank" rel="noopener noreferrer">${title}</a></h5>
                <div class="result-meta">
                    <span class="badge badge-primary">${source}</span>
                    <span class="result-date">${formatDate(timestamp)}</span>
                </div>
            </div>
            <div class="result-body">
                <p>${description}</p>
                <div class="result-url">
                    <i class="fas fa-link"></i>
                    <a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>
                </div>
            </div>
            <div class="result-actions">
                <button class="btn btn-sm btn-outline-primary" onclick="saveResult(${index})">
                    <i class="fas fa-bookmark"></i> Guardar
                </button>
                <button class="btn btn-sm btn-outline-secondary" onclick="shareResult(${index})">
                    <i class="fas fa-share"></i> Compartir
                </button>
                <button class="btn btn-sm btn-outline-info" onclick="analyzeResult(${index})">
                    <i class="fas fa-microscope"></i> Analizar
                </button>
            </div>
        </div>
    `;
}

// Create quick result item
function createQuickResultItem(result, index) {
    const title = result.title || 'Sin título';
    const description = (result.description || result.snippet || '').substring(0, 100) + '...';
    const url = result.url || result.link || '#';
    const source = result.source || 'Desconocido';
    
    return `
        <div class="quick-result-item">
            <div class="quick-result-content">
                <h6><a href="${url}" target="_blank" rel="noopener noreferrer">${title}</a></h6>
                <p class="quick-result-description">${description}</p>
                <small class="text-muted">
                    <i class="fas fa-globe"></i> ${source}
                </small>
            </div>
        </div>
    `;
}

// Load dashboard data
async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard-data');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            updateDashboardStats(data.stats);
            updateDashboardCharts(data.charts);
            updateRecentSearches(data.recent_searches);
        }
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

// Update dashboard statistics
function updateDashboardStats(stats) {
    const statsElements = {
        'total_searches': document.querySelector('[data-stat="total_searches"]'),
        'avg_results': document.querySelector('[data-stat="avg_results"]'),
        'max_results': document.querySelector('[data-stat="max_results"]'),
        'total_sources': document.querySelector('[data-stat="total_sources"]')
    };
    
    Object.entries(statsElements).forEach(([key, element]) => {
        if (element && stats[key] !== undefined) {
            element.textContent = stats[key];
            element.classList.add('animate-number');
        }
    });
}

// Update dashboard charts
function updateDashboardCharts(chartData) {
    if (chartData.search_types) {
        updateSearchTypesChart(chartData.search_types);
    }
    
    if (chartData.sources_usage) {
        updateSourcesChart(chartData.sources_usage);
    }
    
    if (chartData.timeline) {
        updateTimelineChart(chartData.timeline);
    }
}

// Update search types chart
function updateSearchTypesChart(data) {
    const ctx = document.getElementById('searchTypesChart');
    if (!ctx) return;
    
    if (chartInstances.searchTypes) {
        chartInstances.searchTypes.destroy();
    }
    
    chartInstances.searchTypes = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: [
                    '#3498db',
                    '#e74c3c',
                    '#2ecc71',
                    '#f39c12',
                    '#9b59b6',
                    '#1abc9c'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}

// Update sources chart
function updateSourcesChart(data) {
    const ctx = document.getElementById('sourcesChart');
    if (!ctx) return;
    
    if (chartInstances.sources) {
        chartInstances.sources.destroy();
    }
    
    chartInstances.sources = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Consultas',
                data: Object.values(data),
                backgroundColor: '#3498db',
                borderColor: '#2980b9',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeOutQuart'
            }
        }
    });
}

// Initialize charts
function initializeCharts() {
    // Set default Chart.js options
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    Chart.defaults.color = '#333';
    Chart.defaults.borderColor = '#ddd';
}

// Show notification
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification alert alert-${type} alert-dismissible fade show`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.5s ease-out;
    `;
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-triangle',
        warning: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
    };
    
    notification.innerHTML = `
        <i class="${icons[type] || icons.info}"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove notification
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

// Show loading state
function showLoadingState(context) {
    const loadingElements = document.querySelectorAll(`[data-loading="${context}"]`);
    loadingElements.forEach(element => {
        element.style.display = 'block';
    });
    
    const buttons = document.querySelectorAll('button[type="submit"]');
    buttons.forEach(button => {
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
    });
}

// Hide loading state
function hideLoadingState(context) {
    const loadingElements = document.querySelectorAll(`[data-loading="${context}"]`);
    loadingElements.forEach(element => {
        element.style.display = 'none';
    });
    
    const buttons = document.querySelectorAll('button[type="submit"]');
    buttons.forEach(button => {
        button.disabled = false;
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
        } else {
            button.innerHTML = '<i class="fas fa-search"></i> Buscar';
        }
    });
}

// Enable tooltips
function enableTooltips() {
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
}

// Enable animations
function enableAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-visible');
            }
        });
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// Animate results
function animateResults() {
    const resultCards = document.querySelectorAll('.result-card');
    resultCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-fadeInUp');
    });
}

// Initialize theme
function initializeTheme() {
    const savedTheme = localStorage.getItem('osint-theme');
    if (savedTheme) {
        document.body.setAttribute('data-theme', savedTheme);
    }
}

// Setup keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl+/ or Cmd+/ for search focus
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="text"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                bootstrap.Modal.getInstance(modal)?.hide();
            });
        }
    });
}

// Handle window resize
function handleWindowResize() {
    // Redraw charts on resize
    Object.values(chartInstances).forEach(chart => {
        if (chart && typeof chart.resize === 'function') {
            chart.resize();
        }
    });
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function truncateText(text, length = 100) {
    if (text.length <= length) return text;
    return text.substring(0, length) + '...';
}

// Export functions
function exportHistory() {
    showNotification('Exportando historial...', 'info');
    window.location.href = '/api/export/history';
}

function exportResults() {
    if (!currentSearchId) {
        showNotification('No hay resultados para exportar', 'warning');
        return;
    }
    
    showNotification('Exportando resultados...', 'info');
    window.location.href = `/api/export/results/${currentSearchId}`;
}

// Result actions
function saveResult(index) {
    const result = searchResults[index];
    if (!result) return;
    
    showNotification('Resultado guardado', 'success');
    // TODO: Implement save functionality
}

function shareResult(index) {
    const result = searchResults[index];
    if (!result) return;
    
    if (navigator.share) {
        navigator.share({
            title: result.title,
            text: result.description,
            url: result.url
        });
    } else {
        // Fallback to clipboard
        navigator.clipboard.writeText(result.url);
        showNotification('URL copiada al portapapeles', 'success');
    }
}

function analyzeResult(index) {
    const result = searchResults[index];
    if (!result) return;
    
    showNotification('Analizando resultado...', 'info');
    // TODO: Implement analysis functionality
}

// History functions
function filterHistory() {
    const type = document.getElementById('filterType')?.value;
    const status = document.getElementById('filterStatus')?.value;
    const date = document.getElementById('filterDate')?.value;
    const query = document.getElementById('searchQuery')?.value;
    
    const rows = document.querySelectorAll('#historyTable tbody tr');
    
    rows.forEach(row => {
        let show = true;
        
        if (type && row.dataset.type !== type) show = false;
        if (status && row.dataset.status !== status) show = false;
        if (date && !isWithinDateRange(row.dataset.date, date)) show = false;
        if (query && !row.textContent.toLowerCase().includes(query.toLowerCase())) show = false;
        
        row.style.display = show ? '' : 'none';
    });
}

function isWithinDateRange(dateString, days) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    return diffDays <= parseInt(days);
}

function sortTable(columnIndex) {
    const table = document.getElementById('historyTable');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        return aValue.localeCompare(bValue);
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

function toggleSelectAll() {
    const checkboxes = document.querySelectorAll('.row-select');
    const selectAll = document.getElementById('selectAll');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAll.checked;
    });
}

// Make functions globally available
window.performQuickSearch = performQuickSearch;
window.showNotification = showNotification;
window.exportHistory = exportHistory;
window.exportResults = exportResults;
window.saveResult = saveResult;
window.shareResult = shareResult;
window.analyzeResult = analyzeResult;
window.filterHistory = filterHistory;
window.sortTable = sortTable;
window.toggleSelectAll = toggleSelectAll;

}
