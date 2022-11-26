from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib

app = Flask(__name__)

ca = certifi.where()
client = MongoClient('몽고디비주소',
                     tlsCAFile=ca)
db = client.dbsparta

SECRET_KEY = 'SPARTA'


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/api/register', methods=['POST'])
def api_signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})


@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail'})


@app.route('/save', methods=['POST'])
def save_matches():
    url = 'https://radiokorea.com/event/pages/worldcup2022/matches.php'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

    data = requests.get(url, headers=header)
    soup = BeautifulSoup(data.text, "html.parser")

    matches = soup.find_all("div", {"class": "group"})
  

    for match in matches:
        group = match.find("h3", {"class": "group-title"})

    if group is not None:
        leftcountry = match.find("div", {"class": "l-country"}).text
        leftflag = match.find("div", {"class": "l-flag"}).select('img')[0]['src']
        rightflag = match.find("div", {"class": "r-flag"}).select('img')[0]['src']
        rightcountry = match.find("div", {"class": "r-country"}).text
        time = match.find("div", {"class": "time"}).text
        group = group.text

        count = list(db.world.find({}, {'_id': False}))
        num = len(count) + 1

        doc = {
            'id': num,
            'group': group,
            'leftflag': leftflag,
            'leftcountry': leftcountry,
            'rightflag': rightflag,
            'rightcountry': rightcountry,
            'time': time,
        }
        db.world.insert_one(doc)


@app.route('/show', methods=['GET'])
def show_matches():
    match_list = list(db.world.find({}, {'_id': False}))
    return jsonify({'matches': match_list})


@app.route("/save/comment", methods=["POST"])
def save_comment():
    team_receive = request.form['team_give']
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    option1_receive = request.form['option1_give']
    option2_receive = request.form['option2_give']
    order_receive = request.form['order_give']

    doc = {
        'team': team_receive,
        'title': title_receive,
        'comment': comment_receive,
        'option1': option1_receive,
        'option2': option2_receive,
        'order': order_receive,
    }

    db.comment.insert_one(doc)
    return jsonify({'msg': '댓글 완료!'})


@app.route("/show/comment", methods=["GET"])
def show_comment():
    all_comments = list(db.comment.find({}, {'_id': False}))
    return jsonify({'comments': all_comments})


@app.route("/show/detail", methods=["GET"])
def show_detail():
    id_receive = int(request.args.get('id'))
    match = db.world.find_one({'id': id_receive}, {'_id': False})
    return jsonify({'result': match})


@app.route('/<path>')
def get_path(path):
    return render_template(path + '.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
