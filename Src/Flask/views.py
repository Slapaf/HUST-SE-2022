import datetime
import json

from models import User
import time
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from init import app, db
from db_manipulation import *

"""
#     TODO 接口设计
#         1. 创建收集后，根据获得的信息将收集存入数据库，设置提交文件的存储路径（作为返回值用于 create_link.html 页面设置），
#             建议用“收集名+随机数”的组合作为收集标识，用于查找定位，防止重名冲突；
#         2. 用户进入 mycollection.html 页面时，遍历数据库中的所有收集，返回两个列表（命名随意）：list1 和 list2
#             list1 存放正在进行的收集（比较 end_date 和用户进入页面时的系统时间），list2 存放已经截止的收集；
#         3. 用户位于 collection_details.html 页面时，如果添加了应交名单，则需要将名单存入对应收集的某个子目录，
#             并更新 namelist_path 属性；
#         4. 其他查询接口暂定自由设计。
"""


# ! 写错地方了，先留着
def time_format(time_to_format):
    """
    将 datetime.timedelta 类型的数据转换成网页上显示的格式，按“天”、“小时”、“分”、“秒”的优先级显示

    Args:
        time_to_format: datetime.timedelta

    Returns:
        time_formatted: str
    """
    if time_to_format.days < 0:
        return ""
    if time_to_format.days > 0:
        return str(time_to_format.days) + "天"
    seconds = time_to_format.seconds
    hours = seconds // 360
    if hours > 0:
        return str(hours) + "小时"
    minute = seconds // 60
    if minute > 0:
        return str(minute) + "分"
    seconds = seconds % 60
    return str(seconds) + "秒"


@app.route('/mycollection', methods=['GET', 'POST'])
@login_required
def mycollection():
    """
        用户进入 collection_details.html 页面时，遍历数据库中的所有收集，返回两个列表（命名随意）：collection_on 和 collection_end
        collection_on 存放正在进行的收集（比较 end_date 和用户进入页面时的系统时间），collection_end 存放已经截止的收集；
    """
    # ? 根据当前时间更新各个收集的状态
    for collection in Collection_info.query.filter_by(creator_id=current_user.id):
        if collection.end_date <= datetime.now():
            collection.status = '2'  # * 标记为已截止
        else:
            collection.status = '0'  # * 标记为进行中
    db.session.commit()
    # ? 查询进行中的收集
    collection_on = Collection_info.query.filter_by(creator_id=current_user.id, status='0').all()
    # ? 查询已截止的收集
    collection_end = Collection_info.query.filter_by(creator_id=current_user.id, status='2').all()
    # print("正在进行的收集：")
    # for v in collection_on:
    #     print(v.collection_title)
    # print("已经截止的收集：")
    # for v in collection_end:
    #     print(v.collection_title)

    collection_list = Collection_info.query.filter_by(creator_id=current_user.id)
    parameter_dict_list = []
    for collection in collection_list:
        # ? 对时间进行格式化处理
        # tmp_time: datetime.timedelta = deadline_countdown(collection.id)
        # ? 获取已收集文件数
        file_count = 0
        question_list = Question_info.query.filter_by(collection_id=collection.id).all()
        for question in question_list:
            if question.file_path is not None:  # * 有文件路径，说明此题为文件收集题
                file_count += count_filenum(collection.id, question.qno)
        # * 创建一个字典类型，用于传参，可删除
        tmp_dict = {'username': current_user.name,
                    'collection_title': collection.collection_title,
                    'collection_status': "进行中" if collection.status == '0' else "已截止",
                    'submit_count': count_submission(collection.id),
                    'file_collected': file_count,
                    'deadline': collection.end_date.strftime('%Y-%m-%d %H:%M:%S')
                    }
        parameter_dict_list.append(tmp_dict)
        # print(tmp_dict)

    return render_template('mycollection.html',
                           username=current_user.name,
                           json_object=json.dumps(parameter_dict_list),
                           json_length=len(parameter_dict_list)
                           )


# @app.route('/collection_details', methods=['GET', 'POST'])
# @login_required
# def collection_details():
#     # Todo 数据库提供查询已收问卷数、一首文件数量、截止倒计时操作的接口
#     print('已收问卷数:', count_submission(1))
#     print('已收文件数量:', count_filenum(1, 3))
#     print('截止倒计时:', deadline_countdown(1))
#     # Todo 已完成
#     return render_template('collection_details.html')


@app.route('/file_collecting', methods=['GET', 'POST'])
@login_required
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
            # TODO 存入数据库
            add_FC(list(question_list.items(multi=True)))  # ! 多传一个参数：当前登录用户名
            flash("Successfully create a collection!")
            # TODO 已完成

        return redirect(url_for('index'))
    return render_template('file_collecting.html')


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
            flash('The username doesn\'t exist!')  # 如果用户名不存在，显示错误消息
            return redirect(url_for('login'))  # 重定向回登录页面

        # 密码错误
        if not user.validate_password(password):
            flash('Password Error！')  # 如果验证失败，显示错误消息
            return redirect(url_for('login'))  # 重定向回登录页面

        login_user(user)  # 登入用户
        return redirect(url_for('index'))  # 重定向到文件收集界面

    return render_template('login.html')


# 退出登录
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()  # 登出用户
    flash('Goodbye!')
    return redirect(url_for('index'))  # 重定向回首页


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
        user.set_filepath()  # ! 设置用户空间路径
        db.session.add(user)
        db.session.commit()  # 提交数据库会话
        flash('Successfully Registered!')
        path = './FileStorage/' + user.userpath
        os.mkdir(path)  # 创建用户目录
        return redirect(url_for('login'))

    return render_template('register.html')


# 文件收集界面
@app.route('/file_collecting')
def file_collecting():
    return render_template('file_collecting.html')


# 收集记录界面
@app.route('/collect_details')
def collect_details():
    return render_template('collection_details.html')
