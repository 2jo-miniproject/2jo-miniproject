const param = window.location.search;
const paramData = new URLSearchParams(param)
const id = paramData.get('id')

$(document).ready(function () {
    listing();
});

function listing() {
    $('#wrap').empty()
    $.ajax({
        type: 'GET',
        url: '/show/detail?id=' + id,
        data: {},
        success: function (response) {
            let rows = response['result']
            let gruop = rows['group']
            let leftflag = rows['leftflag']
            let leftcountry = rows['leftcountry']
            let rightflag = rows['rightflag']
            let rightcountry = rows['rightcountry']
            let time = rows['time']

            let temp_html = `
                            <div class="wrap1" id="wrap1">
                                <p id="group" style="font-size: 20px">&lt;${gruop}&gt;</p>
                                <div class="wrap2">
                                    <div class="team1">
                                        <img src="${leftflag}" width="40px" height="30px" >
                                        <p id="leftcountry"> ${leftcountry}</p>
                                    </div>
                                        <p id="time">${time}</p>
                                    <div class="team2">
                                        <p id="rightcountry">${rightcountry} </p>
                                        <img src="${rightflag}" width="40px" height="30px" >
                                    </div>
                                </div>
                            </div>`
            $('#wrap').append(temp_html)
        }
    })
}

$(document).ready(function () {
    show_option();
});

function show_option() {
    $.ajax({
        type: "GET",
        url: '/show/detail?id=' + id,
        data: {},
        success: function (response) {
            let rows = response['result']
            let option1 = rows['leftcountry']
            let option2 = rows['rightcountry']

            let temp_html = `<div id="options" class="form-group">
                                <label for="exampleSelect1" class="form-label mt-4">Choose your team</label>
                                <select id="team" class="form-select" id="exampleSelect1">
                                    <div>
                                        <option id="option1">${option1}</option>
                                        <option id="option2">${option2}</option>
                                    </div>
                                </select>
                            </div>`
            $('#options').append(temp_html)
        }
    })
}

$(document).ready(function () {
    show_comment();
});

function show_comment() {
    let order = window.location.href.slice(-1)

    $.ajax({
        type: "GET",
        url: '/show/comment',
        data: {},
        success: function (response) {
            let rows = response['comments']
            for (let i = 0; i < rows.length; i++) {
                if (order == rows[i]['order']) {
                    let comment = rows[i]['comment']
                    let team = rows[i]['team']
                    let title = rows[i]['title']

                    let temp_html = `<div class="card border-dark mb-3" style="max-width: 31rem;">
                                            <div class="card-header">${team}</div>
                                            <div class="card-body">
                                                <h4 class="card-title">${title}</h4>
                                                <p class="card-text">${comment}</p>
                                            </div>
                                        </div>`
                    $('#comment_box').append(temp_html)
                }
            }
        }
    });
}

function save_comment() {
    let team = $('#team').val()
    let title = $('#title').val()
    let comment = $('#comment').val()
    let option1 = $('#option1').val()
    let option2 = $('#option2').val()
    let order = window.location.href.slice(-1)

    $.ajax({
        type: "POST",
        url: "/save/comment",
        data: {
            comment_give: comment,
            title_give: title,
            team_give: team,
            option1_give: option1,
            option2_give: option2,
            order_give: order,
        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}