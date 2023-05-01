from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
import traceback
from static.config import conn, DB_URI
from static import infos

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/home1')
def home1():
    return render_template('index.html')


@app.route('/home2')
def home2():
    return render_template('home2.html')


@app.route('/')
def default_page():
    return render_template('home2.html')


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
@app.route('/wine-self/trivia')
def wine_trivia():
    return render_template('')


# 质量概述，影响因素
@app.route('/quality')
def quality_index():
    return render_template('')


# 因素详情
@app.route('/quality/<factor>')
def quality_factor(factor):
    return render_template('%s.html' % factor)


@app.route('/account-register-page', methods=['GET'])
def account_register_page():
    print('Got in')
    return render_template('account_register.html', err_info=infos.reg_err_infos[4])


@app.route('/account-register-check', methods=['POST'])
def account_register_check():
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if not all([username, password, password2]):
        return redirect(url_for('account_register_err_handler', err_type=infos.reg_err_types[2]))
    elif password != password2:
        return redirect(url_for('account_register_err_handler', err_type=infos.reg_err_types[1]))
    else:
        new_user = Users(username=username, password=password, id=None)
        users = Users.query.filter(Users.username == username).first()
        if users is not None:
            print(users.username)
            return redirect(url_for('account_register_err_handler', err_type=infos.reg_err_types[0]))
        else:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('account_login'))


@app.route('/account-register-err/?<string:err_type>')
def account_register_err_handler(err_type):
    print('err_type = ', err_type)
    if err_type == infos.reg_err_types[0]:
        return render_template('account_register.html', err_info=infos.reg_err_infos[0], err_type=err_type)
    elif err_type == infos.reg_err_types[1]:
        return render_template('account_register.html', err_info=infos.reg_err_infos[1], err_type=err_type)
    elif err_type == infos.reg_err_types[2]:
        return render_template('account_register.html', err_info=infos.reg_err_infos[2], err_type=err_type)
    else:
        return render_template('account_register.html', err_info=infos.reg_err_infos[3], err_type=infos.reg_err_types[3])


@app.route('/account-login', methods=['POST', 'GET'])
def account_login():
    return render_template('account_login.html')


@app.route('/login/check', methods=['POST'])
def login_check():
    print('Got in check')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter(Users.username == username, Users.password == password).first()
        if user:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('account_login'))


@app.route('/account-')


class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(16))


if __name__ == '__main__':
    app.run()
