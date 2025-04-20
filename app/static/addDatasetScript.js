const FLASK_ROOT_URL = "http://127.0.0.1:5000"


document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('dataset-form').addEventListener('submit', event => {
        event.preventDefault();

        const formData = new FormData(this);

        fetch(FLASK_ROOT_URL + '/datasets/add', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok)
                    throw new Error('Response is not ok');

                return response.json();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
