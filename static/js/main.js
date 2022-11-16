$(document).ready(function () {
    listing();
});

function listing() {
    $.ajax({
            type: 'GET',
            url: '/show',
            data: {},
            success: function (response) {
                let rows = response['matches']
                for (let i = 0; i < rows.length; i++) {
                    let gruop = rows[i]['group']
                    let leftflag = rows[i]['leftflag']
                    let leftcountry = rows[i]['leftcountry']
                    let rightflag = rows[i]['rightflag']
                    let rightcountry = rows[i]['rightcountry']
                    let time = rows[i]['time']
                    let id = rows[i]['id']

                    let temp_html = `
                                    <div onclick="location.href='/review?id=${id}'" id="wrap">
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
                                      </div>
                                    </div>`

                    $('#wrap').append(temp_html)
                }
            }
        }
    )
}

function logout() {
    $.removeCookie('mytoken');
    alert('로그아웃!')
    window.location.href = '/login'
}