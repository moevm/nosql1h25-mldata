const FLASK_ROOT_URL = "http://127.0.0.1:5000"
const MAIN_PAGE = FLASK_ROOT_URL + "/datasets";

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('dataset-form');

    form.addEventListener('submit', event => {
        event.preventDefault();
        const formData = new FormData(form);

        fetch(FLASK_ROOT_URL + '/datasets/add', {
            method: 'POST',
            body: formData,
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
    });
});
