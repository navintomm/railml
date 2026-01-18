/**
 * RailML Designer - Frontend Logic
 * Handles manual entry, file uploads, and tab management
 */

// State Management
let networkNodes = [];
let networkEdges = [];
let uploadedFile = null;

// DOM Elements
const navBtns = document.querySelectorAll('.nav-btn');
const tabContents = document.querySelectorAll('.tab-content');
const networkDisplay = document.getElementById('network-display');
const connFromSelect = document.getElementById('conn-from');
const connToSelect = document.getElementById('conn-to');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toast-message');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    updateNetworkDisplay();
});

// Tab Management
function initTabs() {
    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            // Update buttons
            navBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Update content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `${tabId}-tab`) {
                    content.classList.add('active');
                }
            });
        });
    });
}

// Network Management
function addTrack() {
    const id = document.getElementById('track-id').value.trim();
    const x = parseFloat(document.getElementById('track-x').value);
    const y = parseFloat(document.getElementById('track-y').value);

    if (!id) return showToast("Track ID is required", "error");
    if (networkNodes.some(n => n.id === id)) return showToast("Node ID already exists", "error");

    networkNodes.push({ id, type: 'track', x, y });
    document.getElementById('track-id').value = '';
    
    showToast(`Track ${id} added successfully`);
    updateNetworkDisplay();
    updateSelects();
}

function addSwitch() {
    const id = document.getElementById('switch-id').value.trim();
    const x = parseFloat(document.getElementById('switch-x').value);
    const y = parseFloat(document.getElementById('switch-y').value);

    if (!id) return showToast("Switch ID is required", "error");
    if (networkNodes.some(n => n.id === id)) return showToast("Node ID already exists", "error");

    networkNodes.push({ id, type: 'switch', x, y });
    document.getElementById('switch-id').value = '';
    
    showToast(`Switch ${id} added successfully`);
    updateNetworkDisplay();
    updateSelects();
}

function addPlatform() {
    const id = document.getElementById('platform-id').value.trim();
    const x = parseFloat(document.getElementById('platform-x').value);
    const y = parseFloat(document.getElementById('platform-y').value);

    if (!id) return showToast("Platform ID is required", "error");
    if (networkNodes.some(n => n.id === id)) return showToast("Node ID already exists", "error");

    networkNodes.push({ id, type: 'platform', x, y });
    document.getElementById('platform-id').value = '';
    
    showToast(`Platform ${id} added successfully`);
    updateNetworkDisplay();
    updateSelects();
}

function addConnection() {
    const from = connFromSelect.value;
    const to = connToSelect.value;
    const length = parseFloat(document.getElementById('conn-length').value);

    if (!from || !to) return showToast("Please select both 'from' and 'to' nodes", "error");
    if (from === to) return showToast("Cannot connect a node to itself", "error");
    
    const connId = `${from}_to_${to}`;
    if (networkEdges.some(e => e.id === connId)) return showToast("Connection already exists", "error");

    networkEdges.push({ id: connId, from, to, length });
    
    showToast(`Connection ${from} → ${to} added`);
    updateNetworkDisplay();
}

function removeNode(id) {
    networkNodes = networkNodes.filter(n => n.id !== id);
    // Also remove related edges
    networkEdges = networkEdges.filter(e => e.from !== id && e.to !== id);
    
    updateNetworkDisplay();
    updateSelects();
    showToast(`Node ${id} removed`);
}

function removeEdge(id) {
    networkEdges = networkEdges.filter(e => e.id !== id);
    updateNetworkDisplay();
    showToast("Connection removed");
}

function clearNetwork() {
    if (confirm("Are you sure you want to clear all network elements?")) {
        networkNodes = [];
        networkEdges = [];
        updateNetworkDisplay();
        updateSelects();
        showToast("Network cleared");
    }
}

// UI Rendering
function updateNetworkDisplay() {
    if (networkNodes.length === 0 && networkEdges.length === 0) {
        networkDisplay.innerHTML = `
            <div class="empty-state">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                    <path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
                <p>No network elements added yet</p>
                <span>Start by adding tracks, switches, or platforms</span>
            </div>
        `;
        return;
    }

    let html = '';

    // Render Nodes
    networkNodes.forEach(node => {
        html += `
            <div class="network-item">
                <div class="network-item-icon ${node.type}">
                    ${node.type.substring(0, 1).toUpperCase()}
                </div>
                <div class="network-item-details">
                    <h4>${node.id}</h4>
                    <p>Type: ${node.type.toUpperCase()} | Pos: (${node.x}, ${node.y})</p>
                </div>
                <button class="network-item-remove" onclick="removeNode('${node.id}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                </button>
            </div>
        `;
    });

    // Render Edges
    networkEdges.forEach(edge => {
        html += `
            <div class="network-item">
                <div class="network-item-icon connection">
                    C
                </div>
                <div class="network-item-details">
                    <h4>${edge.from} → ${edge.to}</h4>
                    <p>Length: ${edge.length}m</p>
                </div>
                <button class="network-item-remove" onclick="removeEdge('${edge.id}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                </button>
            </div>
        `;
    });

    networkDisplay.innerHTML = html;
}

function updateSelects() {
    const options = networkNodes.map(node => `<option value="${node.id}">${node.id} (${node.type})</option>`).join('');
    const defaultValue = '<option value="">Select node...</option>';
    
    connFromSelect.innerHTML = defaultValue + options;
    connToSelect.innerHTML = defaultValue + options;
}

// File Upload Handling
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    uploadedFile = file;
    const preview = document.getElementById('upload-preview');
    const details = document.getElementById('file-details');

    preview.style.display = 'block';
    details.innerHTML = `
        <div style="margin-bottom: 10px;"><strong>File Name:</strong> ${file.name}</div>
        <div style="margin-bottom: 10px;"><strong>Size:</strong> ${(file.size / 1024).toFixed(2)} KB</div>
        <div><strong>Type:</strong> ${file.type || 'RailML/XML'}</div>
    `;
    
    showToast("File uploaded and ready for processing");
}

// Processing and Analysis
async function generateNetwork() {
    if (networkNodes.length === 0) return showToast("Please add some nodes first", "error");
    
    showToast("Generating network analysis...", "info");
    
    const stationData = {
        name: document.getElementById('station-name').value || "New Station",
        code: document.getElementById('station-code').value || "NST",
        signal_distance: parseFloat(document.getElementById('signal-distance').value),
        nodes: networkNodes,
        edges: networkEdges
    };

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(stationData)
        });
        
        const result = await response.json();
        displayAnalysis(result);
        
        // Switch to analysis tab
        document.querySelector('[data-tab="analysis"]').click();
        showToast("Analysis complete!", "success");
    } catch (error) {
        console.error("Error generating network:", error);
        // Fallback for demo/no-backend
        simulateAnalysis(stationData.name);
    }
}

async function processUploadedFile() {
    if (!uploadedFile) return showToast("No file selected", "error");
    
    showToast("Processing RailML file...", "info");
    
    const formData = new FormData();
    formData.append('file', uploadedFile);
    formData.append('signal_distance', document.getElementById('upload-signal-distance').value);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        displayAnalysis(result);
        
        document.querySelector('[data-tab="analysis"]').click();
        showToast("RailML analysis complete!", "success");
    } catch (error) {
        console.error("Error processing file:", error);
        simulateAnalysis(uploadedFile.name);
    }
}

function displayAnalysis(data) {
    const analysisContent = document.getElementById('analysis-content');
    
    let statsHtml = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${data.stats.total_nodes}</div>
                <div class="stat-label">Total Nodes</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${data.stats.total_edges}</div>
                <div class="stat-label">Total Connections</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${data.stats.cdl_zones || 0}</div>
                <div class="stat-label">CDL Zones</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${data.stats.signals || 0}</div>
                <div class="stat-label">Signals Placed</div>
            </div>
        </div>

        <div class="card card-wide" style="margin-top: 2rem;">
            <div class="card-header">
                <h3><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12l-18 12 4.5-12L3 0z"/></svg> Network Visualization</h3>
            </div>
            <div class="card-body" style="text-align: center; background: #0f172a;">
                <img src="${data.image_path || 'placeholder.png'}" alt="Network Visualization" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">
            </div>
        </div>

        <div class="grid-layout" style="margin-top: 2rem;">
            <div class="card">
                <div class="card-header">
                    <h3>CDL Zones Detected</h3>
                </div>
                <div class="card-body">
                    <ul style="list-style: none; padding: 0;">
                        ${(data.cdl_details || []).map(cdl => `
                            <li style="padding: 10px; border-bottom: 1px solid var(--border-primary); color: var(--color-danger); font-weight: 600;">
                                • ${cdl}
                            </li>
                        `).join('') || '<li style="color: var(--text-muted);">No CDL zones detected</li>'}
                    </ul>
                </div>
            </div>
            <div class="card">
                <div class="card-header">
                    <h3>Signal Requirements</h3>
                </div>
                <div class="card-body">
                    <ul style="list-style: none; padding: 0;">
                        ${(data.signal_details || []).map(sig => `
                            <li style="padding: 10px; border-bottom: 1px solid var(--border-primary); color: var(--color-success); font-weight: 500;">
                                • ${sig}
                            </li>
                        `).join('') || '<li style="color: var(--text-muted);">No signals required</li>'}
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    analysisContent.innerHTML = statsHtml;
}

// Fallback simulator for demonstration
function simulateAnalysis(name) {
    const mockData = {
        stats: {
            total_nodes: networkNodes.length || 12,
            total_edges: networkEdges.length || 10,
            cdl_zones: 2,
            signals: 4
        },
        image_path: 'railway_station_network.png',
        cdl_details: ['EXIT_POINT_A (Merge Switch)', 'PLATFORM_2_FEED'],
        signal_details: [
            'SIG_01: 500m before EXIT_POINT_A',
            'SIG_02: 500m before EXIT_POINT_A',
            'SIG_03: 500m before PLATFORM_2',
            'SIG_04: 500m before PLATFORM_2'
        ]
    };
    
    displayAnalysis(mockData);
    document.querySelector('[data-tab="analysis"]').click();
    showToast("Simulation generated using existing assets", "warning");
}

// Helper Functions
function showToast(message, type = "success") {
    toastMessage.textContent = message;
    
    // Reset colors
    toast.style.background = 'linear-gradient(135deg, var(--color-success), hsl(142, 71%, 35%))';
    if (type === "error") toast.style.background = 'var(--color-danger)';
    if (type === "info") toast.style.background = 'var(--color-primary)';
    if (type === "warning") toast.style.background = 'var(--color-accent)';

    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}
