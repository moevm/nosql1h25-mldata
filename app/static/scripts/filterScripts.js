const FLASK_ROOT_URL = "http://127.0.0.1:5000"
const MAIN_PAGE = FLASK_ROOT_URL + "/datasets";
const FILTER_URL = MAIN_PAGE + "/filter/";

const filterForm = document.getElementById("filter-form");
filterForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(filterForm);

    fetch(FILTER_URL, {
        method: 'POST',
        body: formData,
    }).then(response => {
        if (!response.ok)
            throw new Error('Response is not ok');
        return response.text();
    }).then(text => {
        alert(text)
    }).catch(error => {
        console.error('Error:', error);
    });
})
