import time

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import click
import datetime
import json

"""* 数据库配置 """
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')  # 设置数据库连接地址URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
db = SQLAlchemy(app)  # 在扩展类实例化前加载配置
login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = 'login'


class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    """ 用户信息

    Description:
        记录已注册用户的相关信息。

    Attributes:
        id: 主键
        name: 名字（用户昵称）
        username: 用户名
        password_hash: 密码散列值
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字（用户昵称）
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):
        """
        用来设置密码的方法，接受密码作为参数

        Args:
            password(string): 密码（明文）

        Returns:
            None
        """
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):
        """
        用于验证密码的方法

        Args:
            password(string): 密码（明文）

        Returns:
            (bool): 匹配结果
        """
        return check_password_hash(self.password_hash, password)  # 返回布尔值


class FileCollection(db.Model):
    """ TODO 文件收集 （功能待完善）

    Description:
        记录管理者创建的文件收集的相关信息。

    Attributes:
        id: 主键
        collection_title: 收集名称
        start_date: 收集开始时间
        end_date: 收集结束时间
        namelist_path: 应交名单路径
        file_path: 提交文件路径
    """
    id = db.Column(db.Integer, primary_key=True)
    collection_title = db.Column(db.String(20))  # 收集名称
    start_date = db.Column(db.DateTime)  # 收集开始时间
    end_date = db.Column(db.DateTime)  # 收集结束时间
    namelist_path = db.Column(db.String(20))  # 应交名单路径
    file_path = db.Column(db.String(20))  # 提交文件路径

    def set_collection_date(self, deadline: datetime.datetime):
        """
        设置收集的开始和结束时间

        Args:
            deadline: 截止时间

        Returns:
            None
        """
        self.start_date = datetime.datetime.now()  # 开始时间设置为创建收集的时间
        self.end_date = deadline  # 结束时间设置

    def collection_valid(self):
        """
        判断收集是否截止

        Returns:
            (bool): 截止情况
        """
        current_date = datetime.datetime.now()
        return current_date < self.end_date  # 当前时间小于截止时间时收集有效


@app.route('/file_collecting', methods=['GET', 'POST'])
def generate_collection():
    """
    TODO 生成一个收集对象

    Returns:
        None
    """
    if request.method == 'POST':  # 点击了提交按钮
        question_list = request.form  # 获取题目信息列表
        if not question_list:
            flash("Transport Error!")  # 获取失败
            return render_template('index.html')
        else:
            question_list = list(question_list.items(multi=True))
            print(question_list)
            # TODO 存入数据库

        time.sleep(2)  # ? 调试用，实现后删除

        return render_template('index.html')
    return render_template('file_collecting.html')


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


# @app.cli.command()
# @click.option('--username', prompt=True, help='The username used to login.')
# @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
# def admin(username, password):
#     """Create user."""
#     db.create_all()
#     user = User.query.first()
#     if user is not None:
#         click.echo('Updating user...')
#         user.username = username
#         user.set_password(password)  # 设置密码
#     else:
#         click.echo('Creating user...')
#         user = User(username=username, name=username)
#         user.set_password(password)  # 设置密码
#         db.session.add(user)
#
#     db.session.commit()  # 提交数据库会话
#     click.echo('Done.')


@login_manager.user_loader
def load_user(user_id):
    """
    创建用户加载回调函数
    Args:
        user_id: 用户 id

    Returns:
        user: 用户对象
    """
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


# 主界面
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# 登录界面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 检查输入是否为空
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        user = User.query.filter_by(username=username).first()  # 在数据库中查询用户

        # 验证用户名
        if user is None:
            flash('用户名不存在')  # 如果用户名不存在，显示错误消息
            return redirect(url_for('login'))  # 重定向回登录页面

        # 验证密码是否一致
        if user.validate_password(password):
            login_user(user)  # 登入用户
            return redirect(url_for('file_collecting'))  # 重定向到文件收集界面

        flash('Password Error！')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


# 注册界面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        psw = request.form['psw']
        psw_confirm = request.form['psw_confirm']
        # 检查输入是否为空
        if not username or not psw or not psw_confirm:
            flash('Invalid input!')
            return redirect(url_for('register'))

        # 检查2次输入的密码是否一致
        if psw != psw_confirm:
            flash('The passwords entered do not match!')
            return redirect(url_for('register'))

        # 检查注册的用户名是否已经存在
        num = User.query.filter_by(username=username).count()
        if num:
            flash('The username already exists!')
            return redirect(url_for('register'))

        # 注册成功，将用户信息存入数据库
        user = User(username=username, name=username)  # 初始化时，用户昵称和用户名相同
        user.set_password(psw)
        db.session.add(user)
        db.session.commit()  # 提交数据库会话
        flash('Successfully Registered!')
        return redirect(url_for('login'))

    return render_template('register.html')


# 文件收集界面
@app.route('/file_collecting')
def file_collecting():
    return render_template('file_collecting.html')


if __name__ == "__main__":
    app.run(debug=True)
