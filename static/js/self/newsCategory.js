function toPage() {
    let pageInput = $('.input_page_number').val();
    if (parseInt(pageInput) > pageMax) {
        window.location.href = pageMax;
    } else if (pageInput === '0') {
        window.location.href = '1';
    } else {
        window.location.href = pageInput;
    }
}

function toPreviousPage() {
    let pageInput = $('.input_page_number').val();
    if (pageInput === 1) {
        window.location.href = 1;
    } else {
        window.location.href = toString(parseInt(pageInput) - 1);
    }
}

function toNextPage() {
    let pageInput = $('.input_page_number').val();
    if (parseInt(pageInput) === pageMax) {
        window.location.href = pageMax;
    } else {
        window.location.href = parseInt(pageInput) + 1;
    }
}