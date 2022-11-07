import datetime
import json
from models import User
import time
import pandas as pd
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from init import app, db
from db_manipulation import *

# ! 分享页面的链接（上线前用域名地址替换）
SUBMITTING_PAGE = "127.0.0.1:5000/file_submitting"

sample = [('collection_id', 4),
          ('submitter_id', 1),
          ('question_name1', '姓名lala'),
          ('submit_name1', '计胜翔'),
          ('question_file2', '文件haha'),
          ('submit_file2', '二十大观看心得.docx'),
          ('question_sno3', '学号xixi'),
          ('submit_sno3', 'U202015362'),
          ('question_radio4', '单选题nie'),
          ('submit_checked_radio4', 'C'),
          ('question_multipleChoice5', '多选题kk'),
          ('submit_checked_mulans5', 'A'),
          ('submit_checked_mulans5', 'B'),
          ('question_qnaire6', '你喜欢跑步吗？'),
          ('submit_checked_qnaire6', '1')]

@app.route('/personal_homepage', methods=['GET', 'POST'])
def personal_homepage():
    return render_template("personal_homepage.html")

# 用于测试数据库接口函数
@app.route('/test')
def test():
    # # submission_record(3)
    # delete_collection(1)
    save_submission(sample)
    return redirect(url_for('index'))


# @app.route('/file_submitting/<int:collection_id>', methods=['GET', 'POST'])
@app.route('/file_submitting/<collection_message>', methods=['GET', 'POST'])
def file_submitting(collection_message):
    collection_id = int(collection_message[-1])  # ! 从收集信息字符串中提取收集 id
    print(collection_id)
    print(type(collection_id))
    if request.method == 'POST':
        submission = request.form
        print(submission)
        a = list(submission.items(multi=True))
        # TODO：目前前端传过来的数据中没有collection_id和submitter_id
        save_submission(a)
        return redirect(url_for('index'))
    else:
        question_dict = get_question_Dict(collection_id)
        print(question_dict)
        if question_dict is None:
            return render_template("404.html")
        return render_template("file_submitting.html",
                               collection=question_dict)


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
    # * 如果检测到对收集的操作
    if request.method == 'POST':
        user_action = request.form['hidden-input']  # 获取用户操作的相关信息
        # print(user_action)
        user_action_list = user_action.split('$')
        # print(user_action_list)
        collection_id = user_action_list[1]  # 待操作的收集 id
        # * 根据第一个参数确定操作类型
        if user_action_list[0] == 'share':  # 分享
            submitting_page = 'file_submitting' + '/submit' + collection_id
            # return render_template('file_submitting.html')  # ! Debug
            print(submitting_page)  # ! 调试
        elif user_action_list[0] == 'collect-details':  # 统计
            # TODO
            pass
        elif user_action_list[0] == 'edit':  # 编辑
            pass
        elif user_action_list[0] == 'restart':  # 重启
            pass
        elif user_action_list[0] == 'copy':  # 复制
            pass
        elif user_action_list[0] == 'stop':  # 停止
            stop_collection(int(collection_id), user_action_list)
        elif user_action_list[0] == 'del':  # 删除
            delete_collection(int(collection_id))  # TODO 有问题
        return redirect(url_for('mycollection'))

    update_status(current_user.id)  # 更新当前用户所有收集的 status 字段

    collection_list = Collection_info.query.filter_by(creator_id=current_user.id).all()
    parameter_dict_list = []
    for collection in collection_list:
        # ? 对时间进行格式化处理
        # tmp_time: datetime.timedelta = deadline_countdown(collection.id)
        # ? 获取已收集文件数
        # file_count = 0
        # question_list = Question_info.query.filter_by(collection_id=collection.id).all()
        # for question in question_list:
        #     if question.file_path is not None:  # * 有文件路径，说明此题为文件收集题
        #         file_count += count_filenum(collection.id, question.qno)
        # * 创建一个字典类型，用于传参，可删除
        tmp_dict = {
            'username': current_user.username,
            'collection_title': collection.collection_title,
            'collection_status': "进行中" if collection.status == '0' else "已截止",
            'collection_id': collection.id,  # ! 多传一个收集 id
            'submit_count': count_submission(collection_id=collection.id),
            'deadline': collection.end_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        parameter_dict_list.append(tmp_dict)
        # print(tmp_dict)

    return render_template(
        'mycollection.html',
        username=current_user.name,
        user_email=current_user.email,
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
    生成一个收集对象
    """
    if request.method == 'POST':  # 点击了提交按钮
        question_list = request.form  # 获取题目信息列表
        if not question_list:
            flash("Transport Error!")  # 获取失败
            return render_template('index.html')
        else:
            a = list(question_list.items(multi=True))
            print(a)  # ! 调试用
            t = add_FC(a, current_user.id)
            # question = get_question_MultiDict(t)
            # print(question)
            flash("Successfully create a collection!")

        return redirect(url_for('index'))
    return render_template('file_collecting.html')


# 主界面
@app.route('/')
@app.route('/index')
# @app.route('/index', methods=['GET', 'POST'])
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
        email = request.form['email']
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
        user.set_userpath()  # * 设置用户空间路径
        user.set_email(email)  # * 设置用户邮箱
        db.session.add(user)
        db.session.commit()  # 提交数据库会话
        flash('Successfully Registered!')
        path = './FileStorage/' + user.userpath
        # ! 异常处理
        try:
            os.makedirs(path)  # 创建用户目录
        except OSError:
            if not os.path.isdir(path):
                print("用户目录创建失败！")
        return redirect(url_for('login'))

    return render_template('register.html')


# 文件收集界面
@app.route('/file_collecting')
def file_collecting():
    return render_template('file_collecting.html')


# 收集记录界面
@app.route('/collection_details', methods=['GET', 'POST'])
def collection_details():
    if request.method == 'POST':
        namelist_data = request.form.to_dict()  # * 获取应交名单数据
        name_list = namelist_data['name_data'].split(' ')
        # TODO 若输入名单最后多按下了回车，则最后一个名字末尾有多余的 \r\n
        namelist_csv = pd.DataFrame(columns=["姓名"], data=name_list)
        # print(namelist_csv)
        namelist_path = './FileStorage/' + Collection_info.query.filter_by(
            creator_id=current_user.id).first().namelist_path
        # print(namelist_path)
        os.mkdir(namelist_path)
        namelist_csv.to_csv(namelist_path + "/应交名单.csv", encoding='utf-8')  # * 保存为 csv 文件
        return redirect(url_for('collection_details'))
    return render_template('collection_details.html')
