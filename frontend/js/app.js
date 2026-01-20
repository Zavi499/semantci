// Semantic Keyword Analyzer Frontend Application

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// State Management
const state = {
    currentView: 'analyze',
    history: [],
    currentResult: null
};

// DOM Elements
const elements = {
    // Views
    views: document.querySelectorAll('.view'),
    navBtns: document.querySelectorAll('.nav-btn'),

    // Single Analysis
    keywordInput: document.getElementById('keywordInput'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    loading: document.getElementById('loading'),
    errorMessage: document.getElementById('errorMessage'),
    resultsContainer: document.getElementById('resultsContainer'),
    exampleBtns: document.querySelectorAll('.example-btn'),

    // Batch Analysis
    batchKeywordsInput: document.getElementById('batchKeywordsInput'),
    batchAnalyzeBtn: document.getElementById('batchAnalyzeBtn'),
    parallelCheckbox: document.getElementById('parallelCheckbox'),
    batchLoading: document.getElementById('batchLoading'),
    batchResultsContainer: document.getElementById('batchResultsContainer'),

    // History
    historyList: document.getElementById('historyList'),

    // Status
    apiStatus: document.getElementById('apiStatus'),
    cacheCount: document.getElementById('cacheCount'),
    clearCacheBtn: document.getElementById('clearCacheBtn')
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing Semantic Keyword Analyzer...');
    initializeEventListeners();
    checkAPIHealth();
    loadHistory();
    setInterval(updateCacheStats, 30000); // Update every 30 seconds
});

// Event Listeners
function initializeEventListeners() {
    // Navigation
    elements.navBtns.forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.view));
    });

    // Single Analysis
    elements.analyzeBtn.addEventListener('click', analyzeSingleKeyword);
    elements.keywordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') analyzeSingleKeyword();
    });

    // Example buttons
    elements.exampleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            elements.keywordInput.value = btn.dataset.keyword;
            analyzeSingleKeyword();
        });
    });

    // Batch Analysis
    elements.batchAnalyzeBtn.addEventListener('click', analyzeBatchKeywords');

    // Clear Cache
    elements.clearCacheBtn.addEventListener('click', clearCache);
}

// API Functions
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

async function checkAPIHealth() {
    try {
        const health = await apiRequest('/health');
        elements.apiStatus.classList.remove('offline');
        elements.apiStatus.classList.add('online');
        elements.cacheCount.textContent = health.cache_stats.cached_keywords;
        console.log('API Health:', health);
    } catch (error) {
        elements.apiStatus.classList.remove('online');
        elements.apiStatus.classList.add('offline');
        console.error('API Health Check Failed:', error);
    }
}

async function updateCacheStats() {
    try {
        const stats = await apiRequest('/cache/stats');
        elements.cacheCount.textContent = stats.cached_keywords;
    } catch (error) {
        console.error('Failed to update cache stats:', error);
    }
}

async function clearCache() {
    try {
        await apiRequest('/cache', { method: 'DELETE' });
        showNotification('Cache cleared successfully', 'success');
        updateCacheStats();
    } catch (error) {
        showNotification('Failed to clear cache', 'error');
    }
}

// View Management
function switchView(viewName) {
    if (!viewName) return;

    state.currentView = viewName;

    // Update nav buttons
    elements.navBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === viewName);
    });

    // Update views
    elements.views.forEach(view => {
        view.classList.toggle('active', view.id === `${viewName}View`);
    });

    // Load view data
    if (viewName === 'history') {
        displayHistory();
    }
}

// Single Keyword Analysis
async function analyzeSingleKeyword() {
    const keyword = elements.keywordInput.value.trim();

    if (!keyword) {
        showError('Please enter a keyword');
        return;
    }

    // Show loading state
    elements.loading.classList.add('show');
    elements.errorMessage.classList.remove('show');
    elements.resultsContainer.classList.remove('show');

    try {
        const response = await apiRequest('/analyze', {
            method: 'POST',
            body: JSON.stringify({ keyword })
        });

        if (response.success) {
            state.currentResult = response.data;
            displayResult(response.data, keyword);
            addToHistory(keyword, response.data);
            checkAPIHealth(); // Update cache count
        } else {
            throw new Error(response.error || 'Analysis failed');
        }
    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        elements.loading.classList.remove('show');
    }
}

// Display Single Result
function displayResult(data, keyword) {
    const template = document.getElementById('resultTemplate');
    const clone = template.content.cloneNode(true);

    // Overview
    clone.querySelector('.entity-value').textContent = data.entity;
    clone.querySelector('.entity-type-value').textContent = data.entity_type;
    clone.querySelector('.topic-value').textContent = data.topic;
    clone.querySelector('.intent-value').textContent = data.search_intent;

    // Scores
    const saliencePercent = data.salience;
    const authorityPercent = data.topical_authority;
    const confidencePercent = (data.confidence_scores.overall * 100).toFixed(0);

    clone.querySelector('.salience-score').textContent = saliencePercent.toFixed(1);
    clone.querySelector('.authority-score').textContent = authorityPercent.toFixed(1);
    clone.querySelector('.confidence-score').textContent = confidencePercent;

    clone.querySelector('.salience-fill').style.width = `${saliencePercent}%`;
    clone.querySelector('.authority-fill').style.width = `${authorityPercent}%`;
    clone.querySelector('.confidence-fill').style.width = `${confidencePercent}%`;

    // Attributes
    const attributesList = clone.querySelector('.attributes-list');
    data.attributes.forEach(attr => {
        const tag = document.createElement('span');
        tag.className = 'attribute-tag';
        tag.textContent = attr;
        attributesList.appendChild(tag);
    });

    // Semantic Content
    clone.querySelector('.context-text').textContent = data.context;

    const semanticTags = clone.querySelector('.semantic-tags');
    data.semantic_relevance.slice(0, 10).forEach(term => {
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.textContent = term;
        semanticTags.appendChild(tag);
    });

    const topicClusterTags = clone.querySelector('.topic-cluster-tags');
    data.topic_cluster.forEach(topic => {
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.textContent = topic;
        topicClusterTags.appendChild(tag);
    });

    // Relationships
    const relationshipsList = clone.querySelector('.relationships-list');
    data.relationships.forEach(rel => {
        const item = document.createElement('div');
        item.className = 'relationship-item';
        item.innerHTML = `
            <span class="relationship-type">${rel.type}</span>
            <span class="relationship-entity">${rel.entity}</span>
        `;
        relationshipsList.appendChild(item);
    });

    // Knowledge Graph
    const graphStats = clone.querySelector('.graph-stats');
    graphStats.innerHTML = `
        <div class="graph-stat">
            <i class="fas fa-circle-nodes"></i>
            <span><strong>${data.knowledge_graph.metadata.node_count}</strong> Nodes</span>
        </div>
        <div class="graph-stat">
            <i class="fas fa-arrows-alt-h"></i>
            <span><strong>${data.knowledge_graph.metadata.edge_count}</strong> Edges</span>
        </div>
        <div class="graph-stat">
            <i class="fas fa-chart-pie"></i>
            <span><strong>${(data.knowledge_graph.metadata.graph_density * 100).toFixed(2)}%</strong> Density</span>
        </div>
    `;

    // Taxonomy
    const taxonomyTree = clone.querySelector('.taxonomy-tree');
    data.taxonomy.forEach((level, index) => {
        const item = document.createElement('div');
        item.className = 'taxonomy-level';
        item.innerHTML = `<span class="taxonomy-item">${level}</span>`;
        taxonomyTree.appendChild(item);
    });

    // Ontology
    const ontologyContent = clone.querySelector('.ontology-content');
    const hierarchyItem = document.createElement('div');
    hierarchyItem.className = 'ontology-item';
    hierarchyItem.innerHTML = `
        <h5>Hierarchy</h5>
        <div class="tag-list">
            ${data.ontology.hierarchy.map(h => `<span class="tag">${h}</span>`).join('')}
        </div>
    `;
    ontologyContent.appendChild(hierarchyItem);

    const parentItem = document.createElement('div');
    parentItem.className = 'ontology-item';
    parentItem.innerHTML = `
        <h5>Parent Concepts</h5>
        <div class="tag-list">
            ${data.ontology.parent_concepts.map(p => `<span class="tag">${p}</span>`).join('')}
        </div>
    `;
    ontologyContent.appendChild(parentItem);

    // Schema
    clone.querySelector('.schema-code').textContent = JSON.stringify(data.schema, null, 2);

    // Export button
    clone.querySelector('.export-btn').addEventListener('click', () => {
        downloadJSON(data, `${keyword.replace(/\s+/g, '_')}_analysis.json`);
    });

    // Tab functionality
    setupTabs(clone);

    // Clear and display
    elements.resultsContainer.innerHTML = '';
    elements.resultsContainer.appendChild(clone);
    elements.resultsContainer.classList.add('show');

    // Render knowledge graph
    setTimeout(() => renderKnowledgeGraph(data.knowledge_graph), 100);
}

// Setup Tabs
function setupTabs(container) {
    const tabBtns = container.querySelectorAll('.tab-btn');
    const tabContents = container.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;

            // Update active states
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const content = container.querySelector(`[data-content="${tabName}"]`);
            if (content) content.classList.add('active');

            // Re-render graph if switching to graph tab
            if (tabName === 'graph' && state.currentResult) {
                setTimeout(() => renderKnowledgeGraph(state.currentResult.knowledge_graph), 100);
            }
        });
    });
}

// Render Knowledge Graph
function renderKnowledgeGraph(kgData) {
    const container = document.getElementById('graphViz');
    if (!container || !kgData) return;

    // Prepare data for vis.js
    const nodes = new vis.DataSet(
        kgData.nodes.map(node => ({
            id: node.id,
            label: node.label,
            title: `${node.type}\n${node.entity_type}`,
            color: getNodeColor(node.type),
            font: { size: 14 },
            shape: 'dot',
            size: node.type === 'main_entity' ? 30 : 20
        }))
    );

    const edges = new vis.DataSet(
        kgData.edges.map(edge => ({
            from: edge.source,
            to: edge.target,
            label: edge.type,
            arrows: 'to',
            font: { size: 10, align: 'top' },
            color: { color: '#6366f1', opacity: 0.6 }
        }))
    );

    const data = { nodes, edges };

    const options = {
        nodes: {
            borderWidth: 2,
            borderWidthSelected: 3
        },
        edges: {
            width: 2,
            smooth: {
                type: 'continuous'
            }
        },
        physics: {
            enabled: true,
            stabilization: {
                iterations: 200
            },
            barnesHut: {
                gravitationalConstant: -2000,
                centralGravity: 0.3,
                springLength: 95,
                springConstant: 0.04,
                damping: 0.09
            }
        },
        interaction: {
            hover: true,
            tooltipDelay: 100,
            zoomView: true
        }
    };

    new vis.Network(container, data, options);
}

// Get node color based on type
function getNodeColor(type) {
    const colors = {
        'main_entity': '#6366f1',
        'related_entity': '#10b981',
        'topic': '#f59e0b',
        'semantic_concept': '#8b5cf6',
        'taxonomy': '#ec4899'
    };
    return colors[type] || '#64748b';
}

// Batch Analysis
async function analyzeBatchKeywords() {
    const text = elements.batchKeywordsInput.value.trim();

    if (!text) {
        showNotification('Please enter keywords', 'error');
        return;
    }

    const keywords = text.split('\n')
        .map(k => k.trim())
        .filter(k => k.length > 0);

    if (keywords.length === 0) {
        showNotification('No valid keywords found', 'error');
        return;
    }

    if (keywords.length > 100) {
        showNotification('Maximum 100 keywords allowed', 'error');
        return;
    }

    // Show loading
    elements.batchLoading.classList.add('show');
    elements.batchResultsContainer.innerHTML = '';

    try {
        const response = await apiRequest('/analyze/batch', {
            method: 'POST',
            body: JSON.stringify({
                keywords,
                parallel: elements.parallelCheckbox.checked
            })
        });

        if (response.success) {
            displayBatchResults(response);
        } else {
            throw new Error('Batch analysis failed');
        }
    } catch (error) {
        showNotification(`Error: ${error.message}`, 'error');
    } finally {
        elements.batchLoading.classList.remove('show');
    }
}

// Display Batch Results
function displayBatchResults(response) {
    const container = elements.batchResultsContainer;

    // Summary
    const summary = document.createElement('div');
    summary.className = 'batch-summary';
    summary.innerHTML = `
        <h3>Batch Analysis Summary</h3>
        <div class="batch-stats">
            <div class="batch-stat">
                <div class="batch-stat-value">${response.processed}</div>
                <div class="batch-stat-label">Processed</div>
            </div>
            <div class="batch-stat">
                <div class="batch-stat-value">${Object.keys(response.results).length}</div>
                <div class="batch-stat-label">Results</div>
            </div>
            <div class="batch-stat">
                <div class="batch-stat-value">${response.errors ? response.errors.length : 0}</div>
                <div class="batch-stat-label">Errors</div>
            </div>
        </div>
    `;
    container.appendChild(summary);

    // Results grid
    const grid = document.createElement('div');
    grid.className = 'batch-results-grid';

    Object.entries(response.results).forEach(([keyword, result]) => {
        if (result.error) {
            // Error item
            const item = document.createElement('div');
            item.className = 'batch-result-item';
            item.style.borderLeft = '4px solid var(--danger-color)';
            item.innerHTML = `
                <div class="batch-result-header">
                    <div class="batch-result-keyword">${keyword}</div>
                </div>
                <div style="color: var(--danger-color);">
                    <i class="fas fa-exclamation-circle"></i> ${result.error}
                </div>
            `;
            grid.appendChild(item);
        } else {
            // Success item
            const item = document.createElement('div');
            item.className = 'batch-result-item';
            item.innerHTML = `
                <div class="batch-result-header">
                    <div class="batch-result-keyword">${keyword}</div>
                    <div class="batch-result-scores">
                        <span title="Salience"><i class="fas fa-star"></i> ${result.salience.toFixed(1)}</span>
                        <span title="Authority"><i class="fas fa-shield-alt"></i> ${result.topical_authority.toFixed(1)}</span>
                    </div>
                </div>
                <div class="batch-result-info">
                    <div class="batch-info-item">
                        <div class="batch-info-label">Type</div>
                        <div class="batch-info-value">${result.entity_type}</div>
                    </div>
                    <div class="batch-info-item">
                        <div class="batch-info-label">Topic</div>
                        <div class="batch-info-value">${result.topic}</div>
                    </div>
                    <div class="batch-info-item">
                        <div class="batch-info-label">Intent</div>
                        <div class="batch-info-value">${result.search_intent}</div>
                    </div>
                </div>
            `;
            item.addEventListener('click', () => {
                switchView('analyze');
                elements.keywordInput.value = keyword;
                displayResult(result, keyword);
            });
            grid.appendChild(item);
        }
    });

    container.appendChild(grid);
    checkAPIHealth(); // Update cache
}

// History Management
function addToHistory(keyword, data) {
    const historyItem = {
        keyword,
        timestamp: new Date().toISOString(),
        entity: data.entity,
        type: data.entity_type,
        salience: data.salience,
        data
    };

    state.history.unshift(historyItem);

    // Keep only last 50
    if (state.history.length > 50) {
        state.history = state.history.slice(0, 50);
    }

    saveHistory();
}

function loadHistory() {
    try {
        const saved = localStorage.getItem('analysisHistory');
        if (saved) {
            state.history = JSON.parse(saved);
        }
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

function saveHistory() {
    try {
        localStorage.setItem('analysisHistory', JSON.stringify(state.history));
    } catch (error) {
        console.error('Failed to save history:', error);
    }
}

function displayHistory() {
    const container = elements.historyList;

    if (state.history.length === 0) {
        container.innerHTML = '<p class="empty-state">No analysis history yet. Start analyzing keywords!</p>';
        return;
    }

    container.innerHTML = '';

    state.history.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';

        const timeAgo = getTimeAgo(new Date(item.timestamp));

        historyItem.innerHTML = `
            <div class="history-header">
                <div class="history-keyword">${item.keyword}</div>
                <div class="history-time">${timeAgo}</div>
            </div>
            <div class="history-info">
                <span><strong>Type:</strong> ${item.type}</span>
                <span><strong>Salience:</strong> ${item.salience.toFixed(1)}</span>
            </div>
        `;

        historyItem.addEventListener('click', () => {
            switchView('analyze');
            elements.keywordInput.value = item.keyword;
            displayResult(item.data, item.keyword);
        });

        container.appendChild(historyItem);
    });
}

// Utility Functions
function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorMessage.classList.add('show');
    setTimeout(() => {
        elements.errorMessage.classList.remove('show');
    }, 5000);
}

function showNotification(message, type = 'info') {
    // Simple notification (could be enhanced with a toast library)
    alert(message);
}

function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);

    let interval = seconds / 31536000;
    if (interval > 1) return Math.floor(interval) + ' years ago';

    interval = seconds / 2592000;
    if (interval > 1) return Math.floor(interval) + ' months ago';

    interval = seconds / 86400;
    if (interval > 1) return Math.floor(interval) + ' days ago';

    interval = seconds / 3600;
    if (interval > 1) return Math.floor(interval) + ' hours ago';

    interval = seconds / 60;
    if (interval > 1) return Math.floor(interval) + ' minutes ago';

    return 'just now';
}

// Export for debugging
window.appState = state;
window.apiRequest = apiRequest;
