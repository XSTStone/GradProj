from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
import traceback
from db.config import conn, DB_URI

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/home')
def home_logged():
    return render_template('index.html')


# 模型评估
@app.route('/test', methods=['POST', 'GET'])
def judge():
    data = request.args.to_dict()
    factors = []
    for key in data:
        factors.append(data[key])
    print(factors)

    return render_template('test.html', content=data)


# 葡萄酒相关目录
@app.route('/wine-self')
def wine_index():
    return render_template('')


# 葡萄酒品种
@app.route('/wine-self/cate')
def wine_cate():
    return render_template('')


# 葡萄酒特点
@app.route('/wine-self/feature')
def wine_feature():
    return render_template('')


# 偏门知识
@app.route('/wine-self/fun')
def wine_fun():
    return render_template('')


# 质量概述，影响因素
@app.route('/quality')
def quality_index():
    return render_template('')


# 因素详情
@app.route('/quality/<factor>')
def quality_factor(factor):
    return render_template('%s.html' % factor)


@app.route('/account/login', methods=['POST', 'GET'])
def account_login():
    return render_template('account_login.html')


@app.route('/account/register', methods=['POST', 'GET'])
def account_register():
    if request.method == 'GET':
        print('request.method = ', request.method)
        return render_template('account_register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not all([username, password, password2]):
            flash('Parameters lack')
        elif password != password2:
            flash("Confirming password doesn't match original password")
        else:
            new_user = Users(username=username, password=password, id=None)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('account_login'))
    return redirect(url_for('account_register'))


@app.route('/login/check', methods=['POST'])
def login_check():
    print('Got in check')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print('username = ', username)
        print('password = ', password)

        user = Users.query.filter(Users.username == username, Users.password == password).first()
        if user:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('account_login'))


class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(16))


if __name__ == '__main__':
    app.run()
