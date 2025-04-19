function setupFilters() {
    const $cardsContainer = $('.cards-container');
    let $allCards = $cardsContainer.children('.card').detach();

    function applyFiltersAndSort() {
        const searchText = $('#name-filter').val().toLowerCase();

        const sizeFrom = parseInt($('#data-size-from').val()) || 0;
        const sizeTo = parseInt($('#data-size-to').val()) || Infinity;

        const sortOrder = $('#data-size-sort').val();

        const filteredCards = $allCards.filter(function() {
            const $card = $(this);

            const cardName = $card.data('name').toLowerCase();
            const cardSize = parseInt($card.data('size')) || 0;

            const nameMatch = searchText === '' || cardName.includes(searchText);
            const sizeMatch = cardSize >= sizeFrom && cardSize <= sizeTo;

            return nameMatch && sizeMatch;
        });

        const sortedCards = filteredCards.sort(function(a, b) {
            const sizeA = parseInt($(a).data('size')) || 0;
            const sizeB = parseInt($(b).data('size')) || 0;

            return sortOrder === 'asc' ? sizeA - sizeB : sizeB - sizeA;
        });

        $cardsContainer.empty().append(sortedCards);
    }

    $('#name-filter, #data-size-from, #data-size-to').on('input change', applyFiltersAndSort);
    $('#data-size-sort').on('change', applyFiltersAndSort);

    applyFiltersAndSort();
}

$(document).ready(function() {
    setupFilters();
});