/**
 * Admin Panel - JavaScript
 * توابع مدیریتی و تعاملات کاربری
 */

// Global Variables
const ADMIN_KEY = localStorage.getItem('admin_key') || '';
const API_URL = 'http://localhost:5001/api/admin';

// Dark Mode Toggle
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Load dark mode preference on page load
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Fetch with Admin Key
async function fetchWithAuth(url, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        'X-Admin-Key': ADMIN_KEY,
        ...options.headers
    };

    try {
        const response = await fetch(url, {
            ...options,
            headers
        });

        if (response.status === 401) {
            showError('غیرمجاز - Admin Key نامعتبر');
            redirectToLogin();
            return null;
        }

        return await response.json();
    } catch (error) {
        showError(`خطا: ${error.message}`);
        return null;
    }
}

// Load Users
async function loadUsers() {
    const data = await fetchWithAuth(`${API_URL}/users`);
    
    if (!data) return;

    const tbody = document.getElementById('users-table');
    
    if (data.users && data.users.length > 0) {
        tbody.innerHTML = data.users.map(user => `
            <tr>
                <td>${user.phone_number}</td>
                <td>${user.is_active ? '✅ فعال' : '❌ غیرفعال'}</td>
                <td>${user.subscription_end || 'بدون اشتراک'}</td>
                <td>
                    <button class="button button-primary" onclick="showRenewModal(${user.id})">تمدید</button>
                    <button class="button button-danger" onclick="deleteUser(${user.id})">حذف</button>
                </td>
            </tr>
        `).join('');
    } else {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">کاربری یافت نشد</td></tr>';
    }
}

// Delete User
async function deleteUser(userId) {
    if (!confirm('آیا از حذف این کاربر مطمئن هستید؟')) return;

    const data = await fetchWithAuth(`${API_URL}/users/${userId}`, {
        method: 'DELETE'
    });

    if (data) {
        showSuccess('کاربر حذف شد');
        loadUsers();
    }
}

// Renew Subscription Modal
function showRenewModal(userId) {
    const days = prompt('تعداد روز اشتراک را وارد کنید:');
    
    if (days && !isNaN(days)) {
        renewSubscription(userId, parseInt(days));
    }
}

// Renew Subscription
async function renewSubscription(userId, days) {
    const endDate = new Date();
    endDate.setDate(endDate.getDate() + days);

    const data = await fetchWithAuth(`${API_URL}/users/${userId}/subscription`, {
        method: 'POST',
        body: JSON.stringify({
            subscription_end: endDate.toISOString()
        })
    });

    if (data) {
        showSuccess(`اشتراک تمدید شد (${days} روز)`);
        loadUsers();
    }
}

// Load Statistics
async function loadStatistics() {
    const data = await fetchWithAuth(`${API_URL}/statistics`);
    
    if (data) {
        document.getElementById('total-users').textContent = data.total_users || 0;
        document.getElementById('total-channels').textContent = data.total_channels || 0;
        document.getElementById('total-posts').textContent = data.total_posts || 0;
        document.getElementById('sent-posts').textContent = data.sent_posts || 0;
    }
}

// Load Channels
async function loadChannels() {
    const data = await fetchWithAuth(`${API_URL}/channels`);
    
    if (!data) return;

    const tbody = document.getElementById('channels-table');
    
    if (data.channels && data.channels.length > 0) {
        tbody.innerHTML = data.channels.map(channel => `
            <tr>
                <td>${channel.id}</td>
                <td>${channel.messenger_type}</td>
                <td>${channel.channel_name || '-'}</td>
                <td>${channel.is_active ? '✅ فعال' : '❌ غیرفعال'}</td>
                <td>${channel.created_at}</td>
                <td>
                    <button class="button button-danger" onclick="deleteChannel(${channel.id})">حذف</button>
                </td>
            </tr>
        `).join('');
    } else {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">کانالی یافت نشد</td></tr>';
    }
}

// Delete Channel
async function deleteChannel(channelId) {
    if (!confirm('آیا از حذف این کانال مطمئن هستید؟')) return;

    const data = await fetchWithAuth(`${API_URL}/channels/${channelId}`, {
        method: 'DELETE'
    });

    if (data) {
        showSuccess('کانال حذف شد');
        loadChannels();
    }
}

// Load Posts
async function loadPosts() {
    const data = await fetchWithAuth(`${API_URL}/posts`);
    
    if (!data) return;

    const tbody = document.getElementById('posts-table');
    
    if (data.posts && data.posts.length > 0) {
        tbody.innerHTML = data.posts.map(post => `
            <tr>
                <td>${post.id}</td>
                <td>${post.caption ? post.caption.substring(0, 30) + '...' : '-'}</td>
                <td>${post.post_type}</td>
                <td>${post.scheduled_time}</td>
                <td>
                    ${post.is_sent ? 
                        '<span style="color: green;">✅ ارسال‌شده</span>' : 
                        '<span style="color: orange;">⏳ منتظر</span>'
                    }
                </td>
                <td>
                    <button class="button button-danger" onclick="deletePost(${post.id})">حذف</button>
                </td>
            </tr>
        `).join('');
    } else {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">پستی یافت نشد</td></tr>';
    }
}

// Delete Post
async function deletePost(postId) {
    if (!confirm('آیا از حذف این پست مطمئن هستید؟')) return;

    const data = await fetchWithAuth(`${API_URL}/posts/${postId}`, {
        method: 'DELETE'
    });

    if (data) {
        showSuccess('پست حذف شد');
        loadPosts();
    }
}

// Load Audit Logs
async function loadAuditLogs() {
    const data = await fetchWithAuth(`${API_URL}/logs?page=1&per_page=50`);
    
    if (!data) return;

    const tbody = document.getElementById('logs-table');
    
    if (data.logs && data.logs.length > 0) {
        tbody.innerHTML = data.logs.map(log => `
            <tr>
                <td>${log.timestamp}</td>
                <td>${log.action}</td>
                <td>${log.description}</td>
                <td>${log.ip_address}</td>
                <td><span style="color: green;">✅ ${log.status}</span></td>
            </tr>
        `).join('');
    } else {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">لاگی وجود ندارد</td></tr>';
    }
}

// Notification Functions
function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        border-radius: 4px;
        z-index: 1000;
        animation: slideIn 0.3s ease-in;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Redirect to Login
function redirectToLogin() {
    window.location.href = '/login';
}

// Export Table to CSV
function exportTableToCSV(filename, tableId) {
    const csv = [];
    const rows = document.querySelectorAll(`#${tableId} tr`);
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvRow = Array.from(cols).map(col => col.textContent).join(',');
        csv.push(csvRow);
    });
    
    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}
