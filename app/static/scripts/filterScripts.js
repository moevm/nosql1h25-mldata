$(document).ready(() => {
    $('.ui.accordion').accordion();
});

const FLASK_ROOT_URL = "http://127.0.0.1:5000"
const MAIN_PAGE = FLASK_ROOT_URL + "/datasets";
const FILTER_URL = MAIN_PAGE + "/filter/";

const filterForm = document.getElementById("filter-form");
filterForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(filterForm);

    if (parseFloat(formData.get('size-from')) > parseFloat(formData.get('size-to')) || parseInt(formData.get('row-size-from')) > parseInt(formData.get('row-size-to')) || parseInt(formData.get('column-size-from')) > parseInt(formData.get('column-size-to'))) {
        alert("Значение 'От' не может быть больше значения 'До'");
        return;
    }

    fetch(FILTER_URL, {
        method: 'POST',
        body: formData,
    }).then(response => {
        if (!response.ok)
            throw new Error('Response is not ok');
        return response.json();
    }).then(json => {
        redrawCards(json);
    }).catch(error => {
        console.error('Error:', error);
    });
})

const container = document.getElementById('cards-container');

function redrawCards(arrayOfBriefs) {
    container.replaceChildren();

    for (let brief of arrayOfBriefs) {
        container.appendChild(createCard(brief));
    }
}

function createCard(brief) {
    const card = document.createElement('a');
    card.className = 'ui card';
    card.href = `/dataset/${brief.dataset_id}/`;

    const content = document.createElement('div');
    content.className = 'content';

    const header = document.createElement('div');
    header.className = 'header';
    header.textContent = brief.dataset_name;

    const description = document.createElement('div');
    description.className = 'description';
    description.textContent = brief.dataset_description;

    const lineBreak = document.createElement('br');

    const typeAndSize = document.createElement('div');
    typeAndSize.className = 'description';
    typeAndSize.textContent = `${brief.dataset_type}, ${brief.dataset_size} кбайт`;

    content.appendChild(header);
    content.appendChild(description);
    content.appendChild(lineBreak);
    content.appendChild(typeAndSize);

    card.appendChild(content);

    return card
}
