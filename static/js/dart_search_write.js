// const base_url = 'http://127.0.0.1:8000'
const base_url = 'http://112.220.72.178'

function openDartDetail(recp_no) {
    const url = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo=' + recp_no
    const option = 'width=1000, height=800, location=no, top=100, left=200'
    window.open(url, name = '', option)
}

function previousPage(currentPage) {
    let target;
    if (currentPage == 1) {
        target = 1;
    }  else {
        target = currentPage - 1;
    }
    let query_string = window.location.href.substring(window.location.href.indexOf('?'), window.location.href.length)
    if (query_string.startsWith('?')) {
        window.location.href = '/article/write' + (target).toString() + query_string
    } else {
        window.location.href = '/article/write' + (target).toString()
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
        window.location.href = '/article/write' + (target).toString() + query_string
    } else {
        window.location.href = '/article/write' + (target).toString()
    }
}

function goPage(page) {
    let query_string = window.location.href.substring(window.location.href.indexOf('?'), window.location.href.length)
    if (query_string.startsWith('?')) {
        window.location.href = '/article/write' + page.toString() + query_string
    } else {
        window.location.href = '/article/write' + page.toString()
    }
}

function goTenPrevious(page) {
    let target = page - 10
    if (target < 0) {
        target = 1
    }
    let query_string = window.location.href.substring(window.location.href.indexOf('?'), window.location.href.length)
    if (query_string.startsWith('?')) {
        window.location.href = '/article/write' + target.toString() + query_string
    } else {
        window.location.href = '/article/write' + target.toString()
    }
}

function goTenNext(page, total) {
    let target = page + 10
    if (target > total) {
        target = total
    }
    let query_string = window.location.href.substring(window.location.href.indexOf('?'), window.location.href.length)
    if (query_string.startsWith('?')) {
        window.location.href = '/article/write' + target.toString() + query_string
    } else {
        window.location.href = '/article/write' + target.toString()
    }
}

function search() {
    document.getElementById('search_form').submit()
}

function changeDates(period) {
    $('#toDate').datepicker('setDate', 'today');
    switch (period) {
        case '1w':
            $('#fromDate').datepicker('setDate', '-1W');
            break;
        case '1m':
            $('#fromDate').datepicker('setDate', '-1M');
            break;
        case '6m':
            $('#fromDate').datepicker('setDate', '-6M');
            break;
        case '1y':
            $('#fromDate').datepicker('setDate', '-1Y');
            break;
        case '2y':
            $('#fromDate').datepicker('setDate', '-2Y');
            break;
        case '3y':
            $('#fromDate').datepicker('setDate', '-3Y');
            break;
        case 'all':
            $('#fromDate').datepicker('setDate', new Date('1999-01-01'));
            break
    }
}

function writeSubmit() {
    const stock = $('#stock').val();
    const title = $('#id_title').val();
    const proto = $('#proto_article').html()
    if (stock == '') {
        alert('????????? ??????????????????.');
        return ''
    }
    if (title == '') {
        alert('????????? ??????????????????.');
        return ''
    }
    if ($('#id_content_iframe').contents().find('.note-editable').text() == '') {
        alert('????????? ??????????????????. ???????????? ????????? ?????? ????????????.');
        return ''
    }
    let dartIds = ''
    $.each($('.dartId'), function () {
        const id = $(this).text()
        dartIds = dartIds + ',' + id
    })
    $('#dartIds').val(dartIds)
    $('#protoArticle').val(proto)
    $('#articleSubmit').submit()
}

function searchCorpConfirm() {
    // let names = ''
    // $.each($('input[name="selected"]:checked'), function () {
    //     names = names + $(this).val() + ','
    // })
    let names = $('input[name="selected"]:checked').val();
    let name = names.substring(0, names.indexOf(','))
    let code = names.substring(names.indexOf(',')+1, names.length)
    $('#corp').val(name)
    $('#stockCode').val(code)
    $('#stock').val(name)
    $('#companysearch').hide()
}

function searchCorps(page) {
    const search_name = $('#pop_corp_name_input').val()
    const corp_type = $('#pop_corp_type').val()

    $.ajax({
        url: '/dart/search_company',
        type: 'post',
        data: {
            search_name: search_name,
            corp_type: corp_type,
            page: page
        },
        dataType: 'json'
    })
        .done(function (response) {
            $('#cur_comp_page').text(response.page_num);
            $('#total_comp_page').text(response.total_page);
            $('#total_comp').text(response.total_num);
            $('#threePrevious').attr('onclick', 'goThreePrevious(' + response.page_num + ')')
            $('#searchPrevious').attr('onclick', 'previousPageSearch(' + response.page_num + ')')
            $('#threeNext').attr('onclick', 'goThreeNext(' + response.page_num + ','+ response.total_page  + ')')
            $('#searchNext').attr('onclick', 'nextPageSearch(' + response.page_num + ','+ response.total_page  + ')')

            if (response.three_pages[0] != null) {
                $('#searchPage1').attr('onclick', 'searchCorps(' + response.three_pages[0] + ')')
                $('#searchPage1Num').text(response.three_pages[0])
            } else {
                $('#searchPage1').attr('style', 'display: none;')
            }
            if (response.three_pages[1] != null) {
                $('#searchPage2').attr('onclick', 'searchCorps(' + response.three_pages[1] + ')')
                $('#searchPage2Num').text(response.three_pages[1])
            } else {
                $('#searchPage2').attr('style', 'display: none;')
            }
            if (response.three_pages[2] != null) {
                $('#searchPage3').attr('onclick', 'searchCorps(' + response.three_pages[2] + ')')
                $('#searchPage3Num').text(response.three_pages[2])
            } else {
                $('#searchPage3').attr('style', 'display: none;')
            }
            addComps(response.data);
        })
}

function addComps(comps) {
    const rows = $('.table_contents');
    rows.html('');
    comps.forEach((comp) => {
        const row = '<div class="table_row">\n' +
            '                <div data-type="Text" data-name="?????????" class="contents_cell wid30 corp_name_sel">\n' +
            '                    <div style="width: 15%;">\n' +
            '                        <input type="radio" name="selected" id="sel" value="' + comp.corp_name + ',' + comp.stock_code + '"/>\n' +
            '                    </div>\n' +
            '                    <div style="width: 85%">\n' +
            '                        <label for="sel">'+ comp.corp_name +'</label>\n' +
            '                    </div>\n' +
            '                </div>\n' +
            '                <div data-type="Text" data-name="????????????" class="contents_cell wid20">\n' +
            '                    <span>' + comp.ceo_name + '</span>\n' +
            '                </div>\n' +
            '                <div data-type="Text" data-name="????????????" class="contents_cell wid20">\n' +
            '                    <span>' + comp.stock_code + '</span>\n' +
            '                </div>\n' +
            '                <div data-type="Text" data-name="?????????" class="contents_cell wid30">\n' +
            '                    <span>' + comp.industry_code + '</span>\n' +
            '                </div>\n' +
            '            </div>'
        rows.append(row);
    })
}


function previousPageSearch(currentPage) {
    if (currentPage == 1){
        searchCorps(currentPage)
    } else {
        searchCorps(currentPage - 1)
    }
}

function nextPageSearch(currentPage, totalPage) {
    if (currentPage + 1 <= totalPage) {
        searchCorps(currentPage + 1)
    }
}

function goThreePrevious(page) {
    let target = page - 3
    if (target < 0) {
        target = 1
    }
    searchCorps(target);
}

function goThreeNext(page, total) {
    let target = page + 3
    if (target > total) {
        target = total
    }
    searchCorps(target);
}