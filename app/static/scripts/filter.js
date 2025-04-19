function setupFilters() {
    const $cardsContainer = $('.cards-container');
    let $allCards = $cardsContainer.children('.card').detach();

    function applyFiltersAndSort() {
        const searchText = $('#name-filter').val().toLowerCase();

        let sizeFrom = parseInt($('#data-size-from').val()) || 0;
        let sizeTo = parseInt($('#data-size-to').val()) || Infinity;
        if (sizeTo < sizeFrom) sizeTo = Infinity;

        let rowSizeFrom = parseInt($('#row-size-from').val()) || 0;
        let rowSizeTo = parseInt($('#row-size-to').val()) || Infinity;
        if (rowSizeTo < rowSizeFrom) rowSizeTo = Infinity;

        let viewsFrom = parseInt($('#views-from').val()) || 0;
        let viewsTo = parseInt($('#views-to').val()) || Infinity;
        if (viewsTo < viewsFrom) viewsTo = Infinity;

        const filteredCards = $allCards.filter(function() {
            const $card = $(this);

            const cardName = $card.data('name').toLowerCase();
            const cardSize = parseInt($card.data('size')) || 0;
            const cardRowSize = parseInt($card.data('row-size')) || 0;
            const cardViews = parseInt($card.data('views')) || 0;

            const nameMatch = searchText === '' || cardName.includes(searchText);
            const sizeMatch = cardSize >= sizeFrom && cardSize <= sizeTo;
            const rowSizeMatch = cardRowSize >= rowSizeFrom && cardRowSize <= rowSizeTo;
            const viewsMatch = cardViews >= viewsFrom && cardViews <= viewsTo;

            return nameMatch && sizeMatch && rowSizeMatch && viewsMatch;
        });

        const sortPriority = [
            $('#data-size-sort').val(),
            $('#row-size-sort').val(),
            $('#views-sort').val()
        ].filter(Boolean);

        const sortedCards = filteredCards.sort((a, b) => {
            for (const sortType of sortPriority) {
                const [field, order] = sortType.split('_');
                const valueA = $(a).data(field);
                const valueB = $(b).data(field);

                if (valueA !== valueB) {
                    return order === 'asc' ?
                        (valueA - valueB) :
                        (valueB - valueA);
                }
            }
            return 0;
        });

        $cardsContainer.empty().append(sortedCards);
    }

    $('#name-filter, #data-size-from, #data-size-to, #row-size-from, #row-size-to, #views-from, #views-to').on('input change', applyFiltersAndSort);
    $('#data-size-sort').on('change', applyFiltersAndSort);
    $('#row-size-sort').on('change', applyFiltersAndSort);
    $('#views-sort').on('change', applyFiltersAndSort);

    applyFiltersAndSort();
}

$(document).ready(function() {
    setupFilters();
});