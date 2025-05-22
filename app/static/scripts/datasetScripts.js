$(document).ready(() => {
    $('.ui.accordion').accordion({
        onOpen: function () {
            this.scrollIntoView({behavior: 'smooth', block: 'start'});
        }
    });
    $('.menu .item').tab();
});

const FLASK_ROOT_URL = "http://127.0.0.1:5000"
const MAIN_PAGE = FLASK_ROOT_URL + "/datasets";
const DELETE_URL = MAIN_PAGE + "/delete/";
const ADD_URL = MAIN_PAGE + "/add/";
const EDIT_URL = MAIN_PAGE + "/edit/";

function addDataset() {
    event.preventDefault();

    const fileInput = document.getElementById('csvUpload');
    const fileError = document.getElementById('file-error');

    const datasetName = document.getElementById('name');
    const nameError = document.getElementById('name-error');

    if (!fileInput.files || fileInput.files.length === 0) {
        fileError.style.display = 'block';
        return;
    } else {
        fileError.style.display = 'none';
    }

    if (datasetName.value === '') {
        nameError.style.display = 'block';
        return;
    } else {
        nameError.style.display = 'none';
    }

    const form = document.getElementById('dataset-form');
    const formData = new FormData(form);

    fetch(ADD_URL, {
        method: 'POST',
        body: formData,
    }).then(response => {
        if (!response.ok)
            throw new Error('Response is not ok');
        document.location.href = MAIN_PAGE;
    })
        .catch(error => {
            console.error('Error:', error);
        });
}

function editDataset(datasetId) {
    event.preventDefault();

    const datasetName = document.getElementById('name');
    const nameError = document.getElementById('name-error');

    if (datasetName.value === '') {
        nameError.style.display = 'block';
        return;
    } else {
        nameError.style.display = 'none';
    }

    const form = document.getElementById('dataset-form');
    const formData = new FormData(form);

    fetch(EDIT_URL + datasetId, {
        method: 'PATCH',
        body: formData,
    })
        .then(response => {
            if (!response.ok)
                throw new Error('Response is not ok');
            document.location.href = FLASK_ROOT_URL + "/dataset/" + datasetId;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function deleteDataset(datasetId) {
    event.preventDefault();

    if(!confirm('Вы уверены?')) {
        return;
    }

    fetch(DELETE_URL + datasetId, {
        method: 'DELETE',
        redirect: 'follow'
    })
        .then(response => {
            if (!response.ok)
                throw new Error('Response is not ok');
            document.location.href = MAIN_PAGE;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function createViewsDownloadsPlots(statistics) {
    statistics = JSON.parse(statistics.replaceAll("&#39;",'"'))

    const views = document.getElementById("views-plot");
    const downloads = document.getElementById("downloads-plot");
    
    const labels = statistics['dates']
    options = {
        plugins: {
            legend: {
                display: false
            }
        }
    }

    const ViewsData = {
    labels: labels,
    datasets: [{
        title: 'Views',
        data: statistics['views'],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
    }]
    };

    const ViewsConfig = {
        type: 'line',
        data: ViewsData,
        options: options
    };

    new Chart(views, ViewsConfig);

    const DownloadsData = {
    labels: labels,
    datasets: [{
        title: 'Downloads',
        data: statistics['downloads'],
        fill: false,
        borderColor: 'rgb(75, 192, 75)',
        tension: 0.1
    }]
    };

    const DownloadsConfig = {
        type: 'line',
        data: DownloadsData,
        options: options
    };
    new Chart(downloads, DownloadsConfig);
}

if (document.getElementById('csvUpload') !== null) {
    document.getElementById('csvUpload').addEventListener('change', function () {
        const label = document.getElementById('button-label');

        if (this.files.length > 0) {
            if (document.getElementById('file-error') !== null) {
                document.getElementById('file-error').style.display = 'none';
            }
            label.textContent = this.files[0].name;
        } else {
            if (document.getElementById('file-error') !== null) {
                label.textContent = 'Загрузить CSV файл';
            } else {
                label.textContent = 'Заменить CSV файл';
            }
        }
    });
}

if (document.getElementById('name') !== null) {
    document.getElementById('name').addEventListener('input', function () {
        document.getElementById('name-error').style.display = 'none';
    });
}



let currentPage = 1;

function showPage(page) {
  const cards = document.getElementsByClassName('chart-card');
  const totalCards = cards.length;
  const totalPages = Math.ceil(totalCards / perPage);

  // Validate page number
  if (page < 1) page = 1;
  if (page > totalPages) page = totalPages;

  // Calculate range
  const start = (page - 1) * perPage;
  const end = start + perPage;

  // Hide all cards
  Array.from(cards).forEach(card => card.style.display = 'none');
  
  // Show cards for current page
  Array.from(cards).slice(start, end).forEach(card => {
    card.style.display = 'block';
  });

  // Update current page
  currentPage = page;

  // Disable buttons when appropriate
  document.querySelector('.pagination .item').disabled = currentPage === 1;
  document.querySelector('.pagination .item:last-child').disabled = currentPage === totalPages;
}

function nextPage() {
  showPage(currentPage + 1);
}

function previousPage() {
  showPage(currentPage - 1);
}

// Initial load
document.addEventListener('DOMContentLoaded', () => showPage(1));



