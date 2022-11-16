import json
import os.path
import sys
import pandas as pd
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug import Response

from init import app, db, APP_ROOT, APP_FILE
from db_manipulation import *
from collection_statistic import *

# ! 分享页面的链接（上线前用域名地址替换）
SUBMITTING_PAGE = "127.0.0.1:5000/file_submitting"


def value_type_check(sth_to_be_check):
    """调试函数，项目完成后删除

    输出待检查对象的值和类型

    Args:
        sth_to_be_check: 待检查的对象

    Returns:
        None
    """
    print("Value-Type Check!")
    print("Value:\n", sth_to_be_check)
    print("Type:\n", type(sth_to_be_check))


def id_str_to_int(id_str: str):
    """
    将 str 类型的 id 号转换为 int 类型

    Args:
        id_str(str): str 类型的 id 号

    Returns:
        id_int(int): int 类型的 id 号
    """
    if id_str.isalpha():
        return ord(id_str) - ord('a') + 10
    return int(id_str)


@app.route('/personal_homepage', methods=['GET', 'POST'])
@login_required
def personal_homepage():
    """个人主页

    Returns:
        Response: personal_homepage, 携带参数 r_code
    """
    if request.method == 'POST':
        tmp_data = request.form.to_dict()
        '''
        如果是修改个人信息
        {'username': '张隽翊', 'phone': '未设置', 'email': '729695343@qq.com', 'authorization-code': '未设置'}
        
        如果是修改密码
        {'psw_confirm': '123456', 'submit': ''}
        '''
        value_type_check(tmp_data)
        if 'username' in tmp_data.keys():  # * 修改个人信息
            r_code = modify_personal_info(
                current_user.id,
                tmp_data['username'],
                tmp_data['email'],
                tmp_data['authorization-code']
            )
            if r_code == 1:
                print("修改个人信息成功。")
            else:
                print("修改个人信息失败！该用户不存在。")
        else:  # * 修改密码
            r_code = modify_password(
                current_user.id,
                tmp_data['psw_initial'],
                tmp_data['psw_confirm']
            )  # TODO 待修改
            if r_code == 1:
                print("修改密码成功。")
            else:
                print("修改密码失败！")
        return redirect(url_for('personal_homepage', r_code=r_code))
    user_authorization_code = current_user.authorization_code
    if user_authorization_code is None:
        user_authorization_code = "未设置"
    return render_template(
        "personal_homepage.html",
        user_authorization_code=user_authorization_code,
        user_pwd_hash=current_user.password_hash,  # TODO 待修改
        r_code=2
    )


# 用于测试数据库接口函数
@app.route('/test/<int:collection_id>')
def test(collection_id):
    # get_submission_dict(2, 2)
    collection_data_statistics(collection_id)
    return redirect(url_for('index'))


# @app.route('/file_submitting/<int:collection_id>', methods=['GET', 'POST'])
@app.route('/file_submitting/<string:collection_message>', methods=['GET', 'POST'])
def file_submitting(collection_message):
    """问卷提交

    Args:
        collection_message (str): 收集信息字符串，包含收集 id

    Returns:
        Response: 提交成功，重定向到 submit_successfully; 提交失败，转到 file_submitting
    """
    collection_id = id_str_to_int(collection_message[-1])  # ! 从收集信息字符串中提取收集 id
    # print(collection_id)
    # print(type(collection_id))
    if request.method == 'POST':
        submission = request.form
        tmp_file = request.files
        a = list(submission.items(multi=True))
        # file_upload(collection_id, a, tmp_file)
        save_submission(a, collection_id, file_upload(
            collection_id, a, tmp_file))
        # return redirect(url_for('index'))
        return redirect(url_for('submit_successfully'))
    else:
        question_dict = get_question_dict(collection_id)
        print(question_dict)
        if question_dict is None:
            return render_template("404.html")
        return render_template("file_submitting.html",
                               collection=question_dict)


@app.route('/submit_successfully')
def submit_successfully():
    """问卷提交成功

    Returns:
        Response: submit_successfully 提交成功
    """
    return render_template('submit_successfully.html')


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
        if user_action_list[0] == 'share':  # ? 分享，已完成
            submitting_page = 'file_submitting' + '/submit' + collection_id
            # return render_template('file_submitting.html')  # ! Debug
            print(submitting_page)  # ! 调试
            print("分享")
        elif user_action_list[0] == 'collect-details':  # 统计
            # TODO doing...
            print("统计")
        elif user_action_list[0] == 'edit':  # 编辑
            # TODO doing...
            print("编辑")
            # return render_template("file_editing.html", collection=question_dict)
            # return redirect(url_for('file_editing', collection_id=collection_id))
        elif user_action_list[0] == 'restart':  # 重启
            print("重启")
        elif user_action_list[0] == 'copy':  # 复制
            print("复制")
        elif user_action_list[0] == 'stop':  # ? 停止，已完成
            stop_collection(id_str_to_int(collection_id), user_action_list)
            print("停止")
        elif user_action_list[0] == 'del':  # ? 删除，已完成
            delete_collection(id_str_to_int(collection_id))
            print("删除")
        # return redirect(url_for('mycollection'))

    # else:
    update_status(current_user.id)  # 更新当前用户所有收集的 status 字段

    collection_list = Collection_info.query.filter_by(
        creator_id=current_user.id).all()
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


@app.route('/download')
@login_required
def send_statistic_file() -> Response:
    """返回请求的文件，用于查看汇总和下载文件

    Returns:
        Response: 请求的文件。请求参数为 zip，返回压缩包；请求参数为 excel，返回提交情况。
    """
    tmp_data = request.args.to_dict()
    print(tmp_data)
    collection_id = id_str_to_int(tmp_data['collectionId'])
    file_type = tmp_data['fileType']
    if file_type == 'zip':  # * 用户请求所有收集文件
        print("collection_id: ", collection_id)
        tmp_path = Collection_info.query.get(collection_id).collection_path
        # if sys.platform.startswith('win'):
        #                 #     tmp_path = tmp_path.replace("/", "\\")
        # print("收集文件路径: ", tmp_path)
        # * zip 压缩文件以收集标题命名
        zip_file_name = Collection_info.query.get(collection_id).collection_title + '.zip'
        # print("收集标题: ", zip_file_name)
        source_dir = os.path.join(APP_FILE, tmp_path)
        destination_dir = os.path.join(APP_FILE, current_user.userpath)
        print("源路径: ", source_dir)
        print("目标路径: ", destination_dir)
        # ! 返回压缩包
        # * 生成压缩文件
        generate_zip(source_dir, os.path.join(destination_dir, zip_file_name))
        response = make_response(destination_dir, zip_file_name)
        return response
    else:  # * 用户请求汇总表格
        namelist_path = os.path.join(
            APP_FILE,
            Collection_info.query.get(collection_id).collection_path
        )
        # * Excel 以收集标题命名
        excel_name = Collection_info.query.get(collection_id).collection_title + '.xlsx'
        # * 汇总表格路径
        excel_path = namelist_path
        # * 应交名单列表
        who_should_submit_list = []
        if os.path.exists(os.path.join(namelist_path, '应交名单.csv')):
            who_should_submit_list = pd.read_csv(namelist_path + "/应交名单.csv", encoding='utf-8')['姓名'].to_list()
        # * 已交名单列表
        who_has_submitted_list = [
            submission[0] for submission in submission_record(collection_id=collection_id)
        ]
        # * 生成汇总表格
        generate_excel(who_should_submit_list, who_has_submitted_list, excel_name, excel_path)
        response = make_response(excel_path, excel_name)
        return response


@app.route('/collection_details/<string:collection_id>', methods=['GET', 'POST'])
@login_required
def collection_details(collection_id) -> Response | str:
    """收集详情页面

    Args:
        collection_id (str): 收集 id

    Returns:
        Response: collection_details 收集详情页面
    """
    if request.method == 'POST':
        namelist_data = request.form.to_dict()  # * 获取应交名单数据
        print("前端数据: ", namelist_data)
        if 'hidden-input' in namelist_data.keys():
            # namelist_path = './FileStorage/' + \
            #                 Collection_info.query.filter_by(creator_id=current_user.id).first().namelist_path
            namelist_path = os.path.join(APP_FILE,
                                         Collection_info.query.get(id_str_to_int(collection_id)).collection_path)
            print("应交名单路径：", namelist_path)
            namelist = pd.read_csv(
                namelist_path + "/应交名单.csv", encoding='utf-8')
            # * 删除被点击的名字
            delete_name = namelist_data['hidden-input']
            namelist = namelist[~namelist['姓名'].isin([delete_name])]
            # namelist = namelist[~(namelist['姓名'].str == namelist_data['hidden-input'])]
            namelist.to_csv(namelist_path + "/应交名单.csv",
                            encoding='utf-8', index=False)  # * 保存为 csv 文件
            return redirect(url_for('collection_details', collection_id=collection_id))
        name_list = list(set(namelist_data['name_data'].split()))
        namelist_csv = pd.DataFrame(columns=["姓名"], data=name_list)
        # print(namelist_csv)
        # namelist_path = './FileStorage/' + Collection_info.query.filter_by(
        #     creator_id=current_user.id).first().namelist_path
        namelist_path = os.path.join(APP_FILE,
                                     Collection_info.query.get(id_str_to_int(collection_id)).collection_path)
        print(namelist_path)
        # print(namelist_path)
        # os.mkdir(namelist_path)
        if os.path.exists(namelist_path + "/应交名单.csv"):
            tmp_csv = pd.read_csv(
                namelist_path + '/应交名单.csv', encoding='utf-8')
            for name in name_list:
                if name in tmp_csv['姓名'].values:
                    name_list.remove(name)
            pd.DataFrame(data=name_list).to_csv(namelist_path + "/应交名单.csv", mode='a', header=False,
                                                encoding='utf-8')
        else:
            namelist_csv.to_csv(namelist_path + "/应交名单.csv",
                                encoding='utf-8')  # * 保存为 csv 文件
        return redirect(url_for('collection_details', collection_id=collection_id))

    collection_id = id_str_to_int(collection_id)  # * 转换为实际的收集 id
    parameter_dict_list = []
    # submission_list = submission_record(
    #     collection_id=collection_id)  # * 获取对应 id 的收集信息
    submission_list = submission_record_v2(
        collection_id=collection_id
    )  # * 获取对应 id 的收集信息
    print(submission_list)
    # TODO 数据库提供方法
    # who_has_submitted_list = [submission[0]
    #                           for submission in submission_list]  # * 已提交列表
    who_has_submitted_list = [submission[1]
                              for submission in submission_list]  # * 已提交列表
    # namelist_path = './FileStorage/' + \
    #                 Collection_info.query.filter_by(creator_id=current_user.id).first().namelist_path
    namelist_path = os.path.join(APP_FILE,
                                 Collection_info.query.get(collection_id).collection_path)
    who_should_submit_list = []
    if os.path.exists(namelist_path + "/应交名单.csv"):
        who_should_submit_list = pd.read_csv(namelist_path + "/应交名单.csv",
                                             encoding='utf-8')['姓名'].tolist()
        print(who_should_submit_list)
    # * 已提交名单生成逻辑：在应交名单中且提交了文件
    submitted_list = list(set(who_has_submitted_list) &
                          set(who_should_submit_list))
    print("已提交名单: ", submitted_list)
    # * 未提交名单生成逻辑：在应交名单中但未提交文件
    not_submitted_list = list(
        set(who_should_submit_list) - set(who_has_submitted_list))
    print("未提交名单: ", not_submitted_list)
    # for idx, submission in enumerate(submission_list):
    for submission in submission_list:
        # * 创建一个字典类型，用于传参
        idx = submission[0]  # 提交 id
        submitter_name = submission[1]  # 提交者姓名
        submit_time = submission[2]  # 提交时间
        file_submitted_count = submission[3]  # 提交文件数量
        file_submitted_list = submission[4]  # 提交文件列表
        tmp_dict = {
            'submitter_id': idx,  # ! 已经修正为提交 id
            'submitter_name': submitter_name,
            'submit_time': submit_time.strftime('%Y-%m-%d %H:%M:%S'),
            'file_submitted_count': file_submitted_count,
            'file_submitted_list': file_submitted_list
        }
        parameter_dict_list.append(tmp_dict)

    return render_template(
        'collection_details.html',
        json_object=parameter_dict_list,
        json_length=len(parameter_dict_list),
        submission_count=count_submission(collection_id=collection_id),
        filenum_count=count_filenum(collection_id=collection_id),
        ddl_countdown=Collection_info.query.get(
            collection_id).end_date.strftime('%Y-%m-%d %H:%M:%S'),
        submitted_list=submitted_list,
        not_submitted_list=not_submitted_list
    )


# 文件收集界面
@app.route('/file_collecting')
@login_required
def file_collecting() -> str:
    """文件收集界面

    Returns:
        str: file_collecting 文件收集页面
    """
    return render_template('file_collecting.html')


@app.route('/file_collecting/<string:collection_id>', methods=['GET', 'POST'])
@login_required
def copy_collection(collection_id) -> Response | str:
    """复制收集

    Args:
        collection_id (str): 待复制的收集 id
    """
    if request.method == 'POST':
        question_list = request.form
        if not question_list:
            flash("复制收集失败！")
            return render_template('index.html')
        a = list(question_list.items(multi=True))
        print(a)
        add_FC(a, current_user.id)
        flash("复制收集成功！")
        print("复制收集成功！")
        return redirect(url_for('index'))
    collection_id = id_str_to_int(collection_id)
    question_dict = get_question_dict(collection_id)
    print(question_dict)
    if question_dict is None:
        return render_template("404.html")
    return render_template('file_collecting.html', collection=question_dict)


@app.route('/file_collecting', methods=['GET', 'POST'])
@login_required
def generate_collection() -> Response | str:
    """生成一个收集对象

    Returns:
        Response: 
            若为 POST 请求，创建成功，重定向到 create_link 页面；创建失败，转到 index 页面
            若为 GET 请求，转到 file_collecting 页面
    """
    if request.method == 'POST':  # 点击了提交按钮
        question_list = request.form  # 获取题目信息列表
        if not question_list:
            flash("Transport Error!")  # 获取失败
            return render_template('index.html')
        else:
            a = list(question_list.items(multi=True))
            print('创建收集：', a)  # ! 调试用
            collection_id = add_FC(a, current_user.id)
            # question = get_question_MultiDict(t)
            # print(question)
            flash("Successfully create a collection!")
        # return redirect(url_for('index'))
        share_link = "127.0.0.1:5000/file_submitting/submit" + id_int_to_str(collection_id)
        # return render_template('create_link.html', share_link=share_link)
        return redirect(url_for('create_link', share_id=id_int_to_str(collection_id)))

    return render_template('file_collecting.html')


@app.route('/create_link/<string:share_id>')
def create_link(share_id) -> Response:
    """生成收集链接

    Args:
        share_id (str): 分享 id

    Returns:
        Response: create_link 页面，生成收集链接
    """
    return render_template('create_link.html', share_link="127.0.0.1:5000/file_submitting/submit" + share_id)


# 主界面
@app.route('/')
@app.route('/index')
# @app.route('/index', methods=['GET', 'POST'])
def index() -> Response:
    """收件箱主页

    Returns:
        Response: index 主页
    """
    return render_template('index.html')


# 登录界面
@app.route('/login', methods=['GET', 'POST'])
def login() -> Response:
    """登录页面

    Returns:
        Response:
            若为 POST 请求，登录成功重定向回 index 主页，登录失败重定向回 login 页面
            若为 GET 请求，转到 login 页面
    """
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
def logout() -> Response:
    """退出登录

    Returns:
        Response: index.html 主页
    """
    logout_user()  # 登出用户
    flash('Goodbye!')
    return redirect(url_for('index'))  # 重定向回首页


# 注册界面
@app.route('/register', methods=['GET', 'POST'])
def register() -> Response:
    """注册页面

    Returns:
        Response:
            若为 POST 请求，注册成功重定向回 login 页面，注册失败重定向回 register 页面
            若为 GET 请求，转到 register 页面
    """
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
        # path = './FileStorage/' + user.userpath
        path = os.path.join(APP_FILE, user.userpath)
        print(path)
        # ! 异常处理
        try:
            os.makedirs(path)  # 创建用户目录
        except OSError:
            if not os.path.isdir(path):
                print("用户目录创建失败！")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/file_editing/<string:collection_id>', methods=['GET', 'POST'])
def file_editing(collection_id) -> Response:
    """收集编辑界面

    Args:
        collection_id (str): 收集 id

    Returns:
        Response:
            若为 POST 请求，编辑成功重定向回 index 主页，编辑失败转 index 主页
            若为 GET 请求，查询到收集转 file_editing 页面，未查询到转 404 页面
    """
    if request.method == 'POST':
        question_list = request.form
        value_type_check(question_list)
        if not question_list:
            flash("提交编辑失败！")
            print("提交编辑失败！")
            return render_template('index.html')
        else:
            a = list(question_list.items(multi=True))
            print("编辑后的内容：", a)  # ! 调试用
            modify_collection(id_str_to_int(collection_id), a)
            print("提交编辑成功！")
            return redirect(url_for('mycollection'))  # 编辑完成，返回主页
    collection_id = id_str_to_int(collection_id)
    question_dict = get_question_dict(collection_id)
    print(question_dict)
    if question_dict is None:
        return render_template("404.html")
    return render_template('file_editing.html', collection=question_dict)


@app.route('/file_preview')
def file_preview():
    """问卷预览

    Returns:
        Response: _description_
    """
    tmp_data = request.args.to_dict()
    print(tmp_data)
    collection_id = id_str_to_int(tmp_data['collectionId'])
    submission_id = id_str_to_int(tmp_data['submissionId'])
    print("collection_id: {} submission_id: {}".format(collection_id, submission_id))
    submission_dict = get_submission_dict(collection_id=collection_id, submission_id=submission_id)
    print("submission_dict: {}".format(submission_dict))
    print("预览")
    return render_template('file_preview.html', collection=submission_dict)


@app.route('/statistics')
def statistics():
    tmp_data = request.args.to_dict()
    print("统计参数: ", tmp_data)
    if 'collectionId' not in tmp_data.keys():
        print("统计参数错误")
        redirect(url_for('404'))
    collection_id = id_str_to_int(tmp_data['collectionId'])
    choice_statistics, qnaire_statistics = collection_data_statistics(collection_id)
    print("choice_statistics: ", choice_statistics)
    print("qnaire_statistics: ", qnaire_statistics)
    new_dict = {
        "data_choice": choice_statistics,
        "data_qnaire": qnaire_statistics
    }
    print("new_dict: ", new_dict)
    json_message = json.dumps(new_dict, indent=2,
                              sort_keys=True, ensure_ascii=False)
    return json_message
