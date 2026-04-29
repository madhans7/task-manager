// Task Manager JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if using Bootstrap tooltips
    initializeTooltips();
    
    // Setup form validation
    setupFormValidation();
    
    // Setup rating form
    setupRatingForm();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
}

/**
 * Setup form validation
 */
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

/**
 * Setup rating form submission via AJAX
 */
function setupRatingForm() {
    const ratingForm = document.querySelector('form[action*="/rate"]');
    if (ratingForm) {
        ratingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitRating();
        });
    }
}

/**
 * Submit rating via AJAX
 */
function submitRating() {
    const form = document.querySelector('form[action*="/rate"]');
    const formData = new FormData(form);
    const url = form.getAttribute('action');
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showAlert('success', data.message);
            // Reset form
            form.reset();
            // Reload page after 1.5 seconds
            setTimeout(() => location.reload(), 1500);
        } else if (data.error) {
            showAlert('danger', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'An error occurred while submitting the rating.');
    });
}

/**
 * Show flash message alert
 */
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = bootstrap.Alert.getOrCreateInstance(alertDiv);
        alert.close();
    }, 5000);
}

/**
 * Format date input
 */
function formatDateInput(inputSelector) {
    const dateInput = document.querySelector(inputSelector);
    if (dateInput) {
        dateInput.addEventListener('change', function() {
            const date = new Date(this.value);
            if (!isNaN(date)) {
                this.value = date.toISOString().split('T')[0];
            }
        });
    }
}

/**
 * Update progress bar in real-time
 */
function updateProgressBar(percentage) {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = percentage + '%';
        progressBar.setAttribute('aria-valuenow', percentage);
        progressBar.textContent = percentage + '%';
    }
}

/**
 * Confirm action before proceeding
 */
function confirmAction(message = 'Are you sure?') {
    return confirm(message);
}

/**
 * Disable button to prevent double submission
 */
function disableSubmitButton(buttonSelector) {
    const button = document.querySelector(buttonSelector);
    if (button) {
        button.addEventListener('click', function() {
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
        });
    }
}

/**
 * Format relative time (e.g., "2 hours ago")
 */
function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
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

/**
 * Search tasks with debounce
 */
function searchTasks(query) {
    clearTimeout(window.searchTimeout);
    
    if (query.length < 2) {
        return;
    }
    
    window.searchTimeout = setTimeout(() => {
        window.location.href = `/tasks/search?q=${encodeURIComponent(query)}`;
    }, 500);
}

/**
 * Export data to CSV
 */
function exportToCSV(tableName, filename) {
    const table = document.getElementById(tableName);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        cols.forEach(col => {
            csvRow.push('"' + col.innerText + '"');
        });
        csv.push(csvRow.join(','));
    });
    
    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV file
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], {type: 'text/csv'});
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Initialize charts for dashboard (if using Chart.js)
 */
function initializeDashboardCharts() {
    // Placeholder for chart initialization
    // Can be extended with Chart.js library
}
/**
 * Add a red flag to an employee
 */
function addFlag(employeeId) {
    if (!confirm('Are you sure you want to add a red flag?')) return;
    
    fetch(`/tasks/employee/${employeeId}/flag`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showAlert('success', data.message);
            const span = document.getElementById(`flags-${employeeId}`);
            if (span) {
                let flagsHtml = '';
                for (let i = 0; i < data.count; i++) {
                    flagsHtml += '<i class="fas fa-flag text-danger"></i> ';
                }
                span.innerHTML = `${flagsHtml} (${data.count}/7)`;
            }
        } else if (data.error) {
            showAlert('danger', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'An error occurred.');
    });
}
