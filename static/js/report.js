function previousPage(currentPage) {
    let target;
    if (currentPage == 1) {
        target = 1;
    }  else {
        target = currentPage - 1;
    }
    let query_string = window.location.href.substring(window.location.href.indexOf('?'), window.location.href.length)
    if (query_string.startsWith('?')) {
        window.location.href = '/report/' + (target).toString() + query_string
    } else {
        window.location.href = '/report/' + (target).toString()
    }
}

function nextPage(currentPage, totalPage) {
    let target;
    if (currentPage + 1 <= totalPage) {
        target = currentPage + 1;
    }  else {
        target = currentPage;
    }
    let query_string = window.location.href.substring(window.location.href.indexOf('?'), window.location.href.length)
    if (query_string.startsWith('?')) {
        window.location.href = '/report/' + (target).toString() + query_string
    } else {
        window.location.href = '/report/' + (target).toString()
    }
}

function goTenPrevious(page) {
    let target = page - 10
    if (target < 0) {
        target = 1
    }
    let query_string = window.location.href.substring(window.location.href.indexOf('?'), window.location.href.length)
    if (query_string.startsWith('?')) {
        window.location.href = '/report/' + target.toString() + query_string
    } else {
        window.location.href = '/report/' + target.toString()
    }
}

function goTenNext(page, total) {
    let target = page + 10
    if (target > total) {
        target = total
    }
    let query_string = window.location.href.substring(window.location.href.indexOf('?'), window.location.href.length)
    if (query_string.startsWith('?')) {
        window.location.href = '/report/' + target.toString() + query_string
    } else {
        window.location.href = '/report/' + target.toString()
    }
}