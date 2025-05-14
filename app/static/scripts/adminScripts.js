$(document).ready(() => {
    $('.ui.accordion').accordion({
        onOpen: function () {
            this.scrollIntoView({behavior: 'smooth', block: 'start'});
        }
    });
});
new DataTable('#users');