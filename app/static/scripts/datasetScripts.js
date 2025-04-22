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
