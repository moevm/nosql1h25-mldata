let $allCards;
let $cardsContainer;
let currentSort = null;

function applyFilters() {
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

    let downloadsFrom = parseInt($('#downloads-from').val()) || 0;
    let downloadsTo = parseInt($('#downloads-to').val()) || Infinity;
    if (downloadsTo < downloadsFrom) downloadsTo = Infinity;

    return $allCards.filter(function () {
        const $card = $(this);
        const cardName = $card.data('name').toLowerCase();
        const cardSize = parseInt($card.data('size')) || 0;
        const cardRowSize = parseInt($card.data('row-size')) || 0;
        const cardViews = parseInt($card.data('views')) || 0;
        const cardDownloads = parseInt($card.data('downloads')) || 0;

        return (searchText === '' || cardName.includes(searchText)) &&
            (cardSize >= sizeFrom && cardSize <= sizeTo) &&
            (cardRowSize >= rowSizeFrom && cardRowSize <= rowSizeTo) &&
            (cardViews >= viewsFrom && cardViews <= viewsTo) &&
            (cardDownloads >= downloadsFrom && cardDownloads <= downloadsTo);
    });
}

function applySort(cards) {
    if (!currentSort) return cards;

    return cards.toArray().sort((a, b) => {
        const valueA = $(a).data(currentSort.field);
        const valueB = $(b).data(currentSort.field);
        return currentSort.order === 'asc' ? valueA - valueB : valueB - valueA;
    });
}

function updateDisplay() {
    const filtered = applyFilters();
    const sorted = applySort(filtered);
    $cardsContainer.empty().append(sorted);
}

function setupFilters() {
    $cardsContainer = $('.cards-container');
    $allCards = $cardsContainer.children('.card').detach();

    $('#name-filter, #data-size-from, #data-size-to, #row-size-from, #row-size-to, #views-from, #views-to, #downloads-from, #downloads-to')
        .on('input change', updateDisplay);

    updateDisplay();
}

function setupSorting() {
    $('#data-size-sort, #row-size-sort, #views-sort, #downloads-sort').on('change', function () {
        const val = $(this).val();
        currentSort = val ? {
            field: val.split('_')[0],
            order: val.split('_')[1]
        } : null;

        if (currentSort) resetOtherSorts(this);
        updateDisplay();
    });
}

function resetOtherSorts(currentElement) {
    $('#data-size-sort, #row-size-sort, #views-sort, #downloads-sort').not(currentElement).val('');
}

$(document).ready(function () {
    setupFilters();
    setupSorting();
});