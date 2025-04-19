function setupSearchFilter() {
    const $allCards = $('.cards-container .card');

    function applyFilters() {
        const searchText = $('#name-filter').val().toLowerCase();

        $allCards.each(function() {
            const $card = $(this);
            const cardName = $card.data('name').toLowerCase();
            const isVisible = cardName.includes(searchText);

            $card.toggle(isVisible);
        });
    }

    $('#name-filter').on('input', applyFilters);
}

$(document).ready(function() {
    setupSearchFilter();
});