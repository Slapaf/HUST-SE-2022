import random
import string
import datetime
import re
import yagmail

from init import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    """ 用户信息

    Description:
        记录已注册用户的相关信息。

    Attributes:
        1. id: 主键
        2. name: 名字（用户昵称）
        3. username: 用户名
        4. password_hash: 密码散列值
        5. userpath: 用户空间路径
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字（用户昵称）
    username = db.Column(db.String(20), unique=True)  # 用户名（不可重复）
    password_hash = db.Column(db.String(128))  # 密码散列值
    userpath = db.Column(db.String(20), unique=True)  # 用户空间路径
    email = db.Column(db.String(20), nullable=False, unique=True)  # 用户邮箱
    yag = None

    authorization_code = db.Column(db.String(20), unique=True)  # 邮箱授权码

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

    def set_userpath(self):
        """
        用于设置用户空间路径的方法。路径的前若干位为用户名和 user 标识，后面用随机字符串补齐，总长度 20 位。

        Returns:
            None
        """
        self.userpath = self.username + 'user' + ''.join(
            random.sample(string.ascii_letters + string.digits, 20 - len(self.username) - len('user'))
        )

    def set_email(self, email):
        """
        用于设置用户邮箱的方法

        Args:
            email(str): 需要设置的邮箱

        Returns:
            None
        """
        self.email = email

    def user_authentication(self, user_email: str, user_pwd: str, host='smtp.sina.com'):
        """
        用户认证

        Args:
            user_email(str): 用户邮箱
            user_pwd(str): 邮箱授权码
            host(str): 发送邮件服务器地址

        Returns:
            None
        """
        self.yag = yagmail.SMTP(
            user=user_email,
            password=user_pwd,
            host=host
        )

    def send_email(self, to_email: str or list, email_title: str, email_message: str):
        """
        发送邮件，可以单发也可以群发，取决于传入参数 to_email 的类型

        Args:
            to_email(str or list): 目标邮箱地址，若为列表则代表群发
            email_title(str): 邮件标题
            email_message(str): 邮件正文，可以使用 HTML 格式的字符串

        Returns:

        """
        if self.yag is None:
            return False
        if type(to_email) == "str":  # 单发
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", to_email) is None:
                print("目标邮箱地址错误！")
                return False
            self.yag.send(
                to=to_email,
                subject=email_title,
                contents=email_message
            )
            return True
        else:
            for email_addr in to_email:  # 群发
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email_addr) is None:
                    print("目标邮箱地址错误！")
                    return False
                self.yag.send(
                    to=email_addr,
                    subject=email_title,
                    contents=email_message
                )
            return True


class Collection_info(db.Model):
    """ 文件收集主表

    Description:
        记录已创建收集的相关信息。

    Attributes:
        1. id: 主键
        2. creator: 创建人员名称（不可为空）
        3. creator_id: 创建人员 ID
        4. collection_title: 收集名称（不可为空）
        5. description: 收集描述（不可为空）
        6. start_date: 开始时间，自动设置为创建收集的时间
        7. end_date: 结束时间（不可为空）
        8. status: 收集的状态（0 发布，1 暂存，2 已结束，3 已失效）
        9. namelist_path: 应交名单路径
    """
    # * 收集状态常量定义
    RELEASE, SAVED, FINISHED, OVERDUE = '0', '1', '2', '3'  # ? 发布，暂存，已结束，已失效

    id = db.Column(db.Integer, primary_key=True)  # 主键
    creator = db.Column(db.String(20), nullable=False)  # 创建人员名称（不可以为空）
    creator_id = db.Column(db.Integer)  # 创建人员ID
    collection_title = db.Column(db.String(20), nullable=False)  # 收集名称（不可以为空）
    description = db.Column(db.Text, nullable=False)  # 收集描述（不可以为空）
    start_date = db.Column(db.DateTime, default=datetime.datetime.now())  # 开始时间自动设置为创建收集的时间
    end_date = db.Column(db.DateTime, nullable=False)  # 收集结束时间（不可以为空）
    status = db.Column(db.CHAR)  # 当前状态：0 发布(正在收集);1 暂存;2 已结束;3 已失效
    namelist_path = db.Column(db.String(30))  # 应交名单路径

    def collection_valid(self):
        """
        判断收集是否截止

        Returns:
            (bool): 截止情况
        """
        current_date = datetime.datetime.now()
        return current_date < self.end_date  # 当前时间小于截止时间时收集有效


class Question_info(db.Model):
    """ 问题主表

    Description:
        记录已创建收集的相关信息。

    Attributes:
        1. id: 主键
        2. collection_id: 关联文件收集主表的 id
        3. num: 问题序号
        4. question_type: 问题类型——0:解答题（需上传文件），1:单选，2:多选，3:填空
        5、question_title：问题标题
        5. question_description: 问题描述（不可为空）
        TODO 6. required_flag: 是否为必填项（暂定）
        7. rename_rule: 文件重命名规则
        8. file_path: 提交文件路径
    """
    # * 问题类型常量
    FILE_UPLOAD = '0'  # ? 解答题
    SINGLE_CHOICE = '1'  # ?，单选
    MULTI_CHOICE = '2'  # ?多选
    NAME = '3'  # ?姓名
    SNO = '4'  # ?学号
    SINGLE_QUESTIONNAIRE = '5'  # ?问卷题目(单选)
    MULTI_QUESTIONNAIRE = '6'  # ?问卷题目(多选)

    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer)  # 关联文件收集主表id
    qno = db.Column(db.Integer)  # 问题序号
    question_type = db.Column(db.CHAR)  # 问题类型：0 解答题（需上传文件）;1 单选;2 多选;3 填空;
    question_title = db.Column(db.String(20), nullable=False)  # 问题标题（不可以为空）
    question_description = db.Column(db.Text)  # 问题描述
    # required_flag = db.Column(db.BOOLEAN, nullable=False)  # （暂定） 0 必填;1 非必填
    rename_rule = db.Column(db.String(20))  # 文件重命名规则，其值为题目顺序
    file_path = db.Column(db.String(30))  # 提交文件路径（文件上传题需设置，其余类型不必）


class Answer_info(db.Model):
    """ 答案表

    Description:
        记录已创建收集的相关信息。

    Attributes:
        1. id: 主键
        2、collection_id：关联文件收集主表id
        3. question_id: 关联问题主表 id、
        4、qno：关联问题主表问题序号
        5. answer_option: 答案不可为空
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer)  # 关联文件收集主表id
    question_id = db.Column(db.Integer)  # 关联问题主表id
    qno = db.Column(db.Integer)  # 关联问题主表问题序号
    answer_option = db.Column(db.CHAR, nullable=False)  # 答案不可为空


class Option_info(db.Model):
    """
    问卷题目选项表

    Attributes:
        1、id：主键
        2、collection_id：关联文件收集主表id
        3、question_id：关联问题主表id
        4、qno：关联问题主表问题序号
        5、option_sn：选项序号
        6、option_content：选项内容（不可以为空）
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer)  # 关联文件收集主表id
    question_id = db.Column(db.Integer)  # 关联问题主表id
    qno = db.Column(db.Integer)  # 关联问题主表问题序号
    option_sn = db.Column(db.Integer)  # 选项序号
    option_content = db.Column(db.Text, nullable=False)  # 选项内容（不可以为空）


class Submission_info(db.Model):
    """
    问卷提交信息

    Attributes:
        1、id: 主键
        2、collection_id: 关联文件收集主表id（不可为空）
        3、collection_title：关联文件收集主表收集名称（不可以为空）
        4、submitter_id：提交者的用户id
        5、submitter_name：提交者的用户名username
        6、submit_time：提交时间（不可以为空）
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer)  # 关联文件收集主表id
    collection_title = db.Column(db.String(20))  # 关联文件收集主表收集名称
    submitter_id = db.Column(db.Integer)  # 提交者的用户id
    submitter_name = db.Column(db.String(20))  # 提交者的用户名username
    submit_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())  # 提交时间（不可以为空）


class Submit_Content_info(db.Model):
    """
    提交内容信息表，记录问卷填写情况。

    Attributes:
        1. id: 主键
        2. Submission_id: 关联问卷提交信息表id
        3. collection_id: 关联文件收集主表id（不可为空）
        4. question_id: 关联问题主表id（不可为空）
        5、qno：问题序号
        6、result：某个人对这一题的填写结果（若为文件上传题，则此字段存放上传的文件名称）（不可为空）
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    submission_id = db.Column(db.Integer)  # 关联问卷提交信息表id
    collection_id = db.Column(db.Integer, nullable=False)  # 关联文件收集主表id（不可为空）
    question_id = db.Column(db.Integer, nullable=False)  # 关联问题主表id（不可为空）
    qno = db.Column(db.Integer)  # 问题序号
    # TODO result的nullable限制待定
    result = db.Column(db.String(30), nullable=False)  # 某个人对这一题的填写结果（若为文件上传题，则此字段存放上传的文件名称）（不可为空）
