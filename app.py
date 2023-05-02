from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
import traceback
from flask_wtf import FlaskForm
from static.config import conn, DB_URI
from static import infos
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from user.user import User_Session
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    password_cfm = StringField('Password Confirm', validators=[DataRequired()])


app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'account_login'


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


@app.route('/logged')
@login_required
def index():
    print('GOT In')
    return render_template('index_web.html', username=current_user.username)


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
        password_hash = generate_password_hash(password)
        print(password_hash)
        new_user = Users_db(username=username, password=password_hash, id=None)
        users = Users_db.query.filter(Users_db.username == username).first()
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
        return render_template('account_register.html', err_info=infos.reg_err_infos[3],
                               err_type=infos.reg_err_types[3])


@app.route("/account-login/<err_type>/", methods=['POST', 'GET'])
def account_login(err_type):
    print('err_type = ', err_type)
    return render_template('account_login.html', err_type=err_type)


@app.route('/login/check', methods=['POST'])
def account_login_check():
    print('Got in check')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users_db.query.filter(Users_db.username == username, Users_db.password == password).first()
        if user:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('account_login'))


@app.route('/account-my')
def account_my():
    return None


@login_manager.user_loader
def load_user(user_id):
    return User_Session.get(user_id=user_id)


def get_user_in_db(username):
    user = Users_db.query.filter(Users_db.username == username).first()
    if user:
        return user
    else:
        return None


class Users_db(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(200))

    def get_username(self):
        return self.username

    def get_id(self):
        return self.id

    def get_password(self):
        return self.password


class User_Session(UserMixin):
    """登陆_User类"""

    def __init__(self, user):
        self.username = user.get_username()
        self.password_hash = user.get_password()
        self.id = user.get_id()

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取User Entity，为login_user提供支持"""
        if not user_id:
            return None
        found_user = Users_db.query.filter(Users_db.id == user_id).first()
        if found_user:
            return found_user
        else:
            return None


@app.route('/account-login-web', methods=('GET', 'POST'))
def account_login_web():
    print('Got in login web')
    err_type = None
    username = request.form.get('username')
    password = request.form.get('password')
    print('username = ', username)
    print('password = ', password)
    found_user_in_db = get_user_in_db(username=username)

    if found_user_in_db is None:
        err_type = 'username'
    else:
        user = User_Session(found_user_in_db)
        if user.verify_password(password):
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            err_type = 'password'

    # return render_template('account_login.html', err_type=err_type)
    return redirect(url_for('account_login', err_type=err_type))


@app.route('/account-login-web-page', methods=('GET', 'POST'))
def account_login_web_page():
    form = LoginForm()
    return render_template('login.html', form=form, err_msg='empty')


@app.route('/account-register-web-page', methods=('GET', 'POST'))
def account_register_web_page():
    return render_template('account_register.html')


if __name__ == '__main__':
    app.run()
