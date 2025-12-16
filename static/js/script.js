// Age Distribution Chart
const ageCtx = document.getElementById('ageChart').getContext('2d');
new Chart(ageCtx, {
    type: 'bar',
    data: {
        labels: ['Below 20', '21-40', '41-50', 'Above 50'],
        datasets: [{
            label: 'Number of Vendors',
            data: [17, 54, 9, 9],
            backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#4facfe']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: { display: false }
        }
    }
});

// Gender Distribution Chart
const genderCtx = document.getElementById('genderChart').getContext('2d');
new Chart(genderCtx, {
    type: 'doughnut',
    data: {
        labels: ['Male', 'Female'],
        datasets: [{
            data: [75, 5],
            backgroundColor: ['#667eea', '#f093fb']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true
    }
});

// Education Level Chart
const educationCtx = document.getElementById('educationChart').getContext('2d');
new Chart(educationCtx, {
    type: 'pie',
    data: {
        labels: ['No Formal Education', 'Primary', 'Secondary/Higher', 'Graduate'],
        datasets: [{
            data: [29, 20, 30, 1],
            backgroundColor: ['#dc3545', '#ffc107', '#28a745', '#667eea']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true
    }
});

// Stall Location Chart
const locationCtx = document.getElementById('locationChart').getContext('2d');
new Chart(locationCtx, {
    type: 'bar',
    data: {
        labels: ['Market Areas', 'Near Schools/Colleges', 'Public Parks', 'Transport Hubs', 'Others'],
        datasets: [{
            label: 'Number of Vendors',
            data: [34, 20, 10, 10, 6],
            backgroundColor: '#764ba2'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: { display: false }
        }
    }
});

// Food Storage Chart
const storageCtx = document.getElementById('storageChart').getContext('2d');
new Chart(storageCtx, {
    type: 'doughnut',
    data: {
        labels: ['Refrigerator', 'Covered Containers', 'Sell Same Day'],
        datasets: [{
            data: [48, 4, 28],
            backgroundColor: ['#28a745', '#ffc107', '#667eea']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true
    }
});

// Protective Equipment Chart
const protectionCtx = document.getElementById('protectionChart').getContext('2d');
new Chart(protectionCtx, {
    type: 'bar',
    data: {
        labels: ['Use Gloves', 'Wear Aprons'],
        datasets: [{
            label: 'Always/Sometimes',
            data: [47, 13],
            backgroundColor: '#28a745'
        }, {
            label: 'Never',
            data: [33, 67],
            backgroundColor: '#dc3545'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true
    }
});

// Hand Washing Chart
const handwashCtx = document.getElementById('handwashChart').getContext('2d');
new Chart(handwashCtx, {
    type: 'pie',
    data: {
        labels: ['Before Cooking/Serving', 'All Hygiene Measures', 'Minimal'],
        datasets: [{
            data: [52, 24, 4],
            backgroundColor: ['#28a745', '#667eea', '#ffc107']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true
    }
});

// Waste Disposal Chart
const wasteCtx = document.getElementById('wasteChart').getContext('2d');
new Chart(wasteCtx, {
    type: 'doughnut',
    data: {
        labels: ['Trash Bin', 'Waste Collection Service', 'Open Street'],
        datasets: [{
            data: [68, 7, 5],
            backgroundColor: ['#28a745', '#667eea', '#dc3545']
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true
    }
});
