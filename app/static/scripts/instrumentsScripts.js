const fileInput = document.getElementById('zipUpload');
const fileError = document.getElementById('file-error');

const uploadForm = document.getElementById('upload-form');
uploadForm.addEventListener('submit', (e) => {
    e.preventDefault();

    if (!fileInput.files || fileInput.files.length === 0) {
        fileError.style.display = 'block';
        return;
    } else {
        fileError.style.display = 'none';
    }

    const form = document.getElementById('upload-form');
    const formData = new FormData(form);

    fetch("http://127.0.0.1:5000/datasets/import", {
        method: 'POST',
        body: formData,
    }).then(response => {
        if (!response.ok)
            throw new Error('Response is not ok');
        window.location.href = response.headers.get('redirect');
    }).catch(error => {
        console.error('Error:', error);
    });
});

fileInput.addEventListener('change', (e) => {
    e.preventDefault();

    const label = document.getElementById('button-label');

    if (e.target.files.length > 0) {
        document.getElementById('file-error').style.display = 'none';
        label.textContent = e.target.files[0].name;
    } else {
        label.textContent = 'Загрузить ZIP файл';
    }
});