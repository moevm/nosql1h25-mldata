$(document).ready(() => {
    $('.ui.accordion').accordion({
        onOpen: function () {
            this.scrollIntoView({behavior: 'smooth', block: 'start'});
        }
    });
});
new DataTable('#users');

const FLASK_ROOT_URL = "http://127.0.0.1:5000"
const ADMIN_PAGE = FLASK_ROOT_URL + "/admin";
const BAN_URL = FLASK_ROOT_URL + "/ban/";
const UNBAN_URL = FLASK_ROOT_URL + "/unban/";

function ban(user_id) {
    event.preventDefault();

    if(!confirm('Вы уверены?')) {
        return;
    }

    console.log(BAN_URL + user_id)

    fetch(BAN_URL + user_id, {
        method: 'POST',
        redirect: 'follow'
    })
        .then(response => {
            if (!response.ok)
                throw new Error('Response is not ok');
            document.location.href = ADMIN_PAGE;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function unban(user_id) {
    event.preventDefault();

    if(!confirm('Вы уверены?')) {
        return;
    }

    fetch(UNBAN_URL + user_id, {
        method: 'POST',
        redirect: 'follow'
    })
        .then(response => {
            if (!response.ok)
                throw new Error('Response is not ok');
            document.location.href = ADMIN_PAGE;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}