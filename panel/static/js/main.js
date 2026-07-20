// API Configuration
const API_BASE = '/api';
let authToken = localStorage.getItem('authToken');

// Navigation
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', (e) => {
        if (e.target.href.includes('#')) {
            const sectionId = e.target.hash.substring(1);
            showSection(sectionId);
        }
    });
});

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'block';
    }
}

// API Functions
async function apiCall(endpoint, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });

        if (!response.ok) {
            if (response.status === 401) {
                logout();
                return null;
            }
            throw new Error(`API error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API call error:', error);
        return null;
    }
}

// Dashboard Functions
async function loadDashboard() {
    const data = await apiCall('/stats/dashboard');
    if (data) {
        document.getElementById('bot-status').textContent = data.bot_status || 'Unknown';
        document.getElementById('posts-today').textContent = data.posts_today || '0';
        document.getElementById('active-sources').textContent = data.active_sources || '0';
        document.getElementById('total-downloads').textContent = data.total_downloads || '0';
    }
}

// Channel Management
async function loadChannels() {
    const data = await apiCall('/channels');
    if (data && data.channels) {
        const tbody = document.getElementById('channels-tbody');
        tbody.innerHTML = '';
        
        if (data.channels.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4">No channels configured</td></tr>';
            return;
        }

        data.channels.forEach(channel => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${channel.name}</td>
                <td><span class="badge ${channel.enabled ? 'success' : 'danger'}">${channel.enabled ? 'Enabled' : 'Disabled'}</span></td>
                <td>${channel.posts || 0}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="removeChannel('${channel.id}')">Remove</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }
}

function showAddChannelModal() {
    document.getElementById('add-channel-modal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('add-channel-modal').style.display = 'none';
}

async function addChannel() {
    const name = document.getElementById('channel-name').value;
    if (!name) {
        alert('Please enter a channel name');
        return;
    }

    const data = await apiCall('/channels', {
        method: 'POST',
        body: JSON.stringify({ name, enabled: true })
    });

    if (data) {
        alert('Channel added successfully');
        closeModal();
        loadChannels();
        document.getElementById('channel-name').value = '';
    }
}

async function removeChannel(channelId) {
    if (!confirm('Are you sure you want to remove this channel?')) {
        return;
    }

    const data = await apiCall(`/channels/${channelId}`, {
        method: 'DELETE'
    });

    if (data) {
        alert('Channel removed successfully');
        loadChannels();
    }
}

// Scheduler Functions
async function saveSchedulerSettings() {
    const interval = document.getElementById('interval-select').value;
    const data = await apiCall('/scheduler/interval', {
        method: 'PUT',
        body: JSON.stringify({ interval_minutes: parseInt(interval) })
    });

    if (data) {
        alert('Scheduler settings saved');
    }
}

// Settings Functions
async function saveSettings() {
    const watermark = document.getElementById('watermark-input').value;
    const notifications = document.getElementById('notifications-input').checked;

    const data = await apiCall('/settings', {
        method: 'PUT',
        body: JSON.stringify({ watermark, notifications })
    });

    if (data) {
        alert('Settings saved');
    }
}

// Logout
function logout() {
    localStorage.removeItem('authToken');
    window.location.href = '/login';
}

// Event Listeners
document.getElementById('add-channel-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    addChannel();
});

document.getElementById('scheduler-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    saveSchedulerSettings();
});

document.getElementById('settings-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    saveSettings();
});

// Initialize
window.addEventListener('DOMContentLoaded', () => {
    if (!authToken) {
        window.location.href = '/login';
        return;
    }

    loadDashboard();
    loadChannels();
    
    // Refresh dashboard every 30 seconds
    setInterval(loadDashboard, 30000);
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    const modal = document.getElementById('add-channel-modal');
    if (e.target === modal) {
        closeModal();
    }
});