const FLASK_ROOT_URL = "http://127.0.0.1:5000"
const MAIN_PAGE = FLASK_ROOT_URL + "/datasets";
const DELETE_URL = MAIN_PAGE + "/delete/";
const ADD_URL = MAIN_PAGE + "/add/";
const EDIT_URL = MAIN_PAGE + "/edit/";

function addDataset() {
    event.preventDefault();
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

    const form = document.getElementById('dataset-form');
    const formData = new FormData(form);

    fetch(EDIT_URL + datasetId, {
        method: 'PATCH',
        body: formData,
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

function deleteDataset(datasetId) {
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
