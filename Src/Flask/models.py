import random, smtplib, string, datetime, re, yagmail
from init import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """ 用户信息表。

    记录已注册用户的相关信息。

    Attributes:
        id: 主键，自增
        name: 用户昵称（不可为空）
        username: 用户名（不可为空，不可重复）
        password_hash: 密码散列值（不可为空）
        userpath: 用户空间路径（不可为空，不可重复）
        email: 用户邮箱（不可为空）
        authorization_code: 邮箱授权码
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(30), nullable=False)  # 用户昵称
    username = db.Column(db.String(30), nullable=False, unique=True)  # 用户名
    password_hash = db.Column(db.String(128), nullable=False)  # 密码散列值
    userpath = db.Column(db.String(50), nullable=False, unique=True)  # 用户空间路径
    email = db.Column(db.String(30), nullable=False)  # 用户邮箱
    authorization_code = db.Column(db.String(30))  # 邮箱授权码

    def set_password(self, password: str) -> None:
        """设置密码

        Args:
            password: 密码（明文）

        """
        self.password_hash = generate_password_hash(
            password)  # 根据用户输入的密码生成密码散列值

    def validate_password(self, password: str) -> bool:
        """验证密码

        Args:
            password: 密码（明文）

        Returns:
            布尔值，表示密码是否正确
        """
        return check_password_hash(self.password_hash, password)

    def set_userpath(self) -> None:
        """设置用户空间路径"""

        # 路径的前若干位为用户名和 user 标识，后面用随机字符串补齐，总长度 20 位。
        self.userpath = self.username + 'user' + ''.join(
            random.sample(string.ascii_letters + string.digits,
                          20 - len(self.username) - len('user'))
        )

    def set_email(self, email: str) -> None:
        """设置用户邮箱

        Args:
            email: 邮箱
        """
        self.email = email

    def email_authentication(self, user_email: str = email,
                             user_pwd: str = authorization_code,
                             host: str = 'smtp.sina.com'):
        """邮箱认证

        Args:
            user_email: 用户邮箱
            user_pwd: 邮箱授权码
            host: 发送邮件服务器地址
        """
        return yagmail.SMTP(user=user_email, password=user_pwd, host=host)

    def send_email(self, to_email, email_title: str, email_message: str) -> bool:
        """发送邮件，可以单发也可以群发，取决于传入参数 to_email 的类型

        Args:
            to_email: 目标邮箱地址，若为列表则代表群发
            email_title: 邮件标题
            email_message: 邮件正文，可以使用 HTML 格式的字符串

        Returns:
            布尔值，表示是否发送成功
        """
        server = "smtp." + self.email.split('@')[1]
        print(server)
        yag = yagmail.SMTP(user=self.email, password=self.authorization_code, host=server)
        if yag is None:
            print("yag is None!")
            return False
        if type(to_email) == "str":  # 单发
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", to_email) is None:
                print("目标邮箱地址错误！")
                return False
            try:
                yag.send(
                    to=to_email,
                    subject=email_title,
                    contents=email_message
                )
            except smtplib.SMTPAuthenticationError:
                print("授权码错误！")
            return True
        else:
            for email_addr in to_email:  # 群发
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email_addr) is None:
                    print("目标邮箱地址错误！")
                    return False
                try:
                    yag.send(
                        to=email_addr,
                        subject=email_title,
                        contents=email_message
                    )
                except smtplib.SMTPAuthenticationError:
                    print("授权码错误！")

            return True


class Collection_info(db.Model):
    """ 收集表。

    记录已创建收集的相关信息。

    Attributes:
        id: 主键
        creator: 创建人员名称（不可为空）
        creator_id: 创建人员ID（外键：关联user.id；不可为空）
        collection_title: 收集标题（不可为空）
        description: 收集描述（不可为空）
        start_date: 开始时间，自动设置为创建收集的时间（不可为空）
        end_date: 结束时间（不可为空）
        status: 收集的状态（'0' 发布，'1' 暂存，'2' 已结束，'3' 已失效）（不可为空）
        namelist_path: 应交名单路径
    """
    # * 收集状态常量定义
    RELEASE, SAVED, FINISHED, OVERDUE = '0', '1', '2', '3'  # ? 发布，暂存，已结束，已失效

    id = db.Column(db.Integer, primary_key=True)  # 主键
    creator = db.Column(db.String(30), nullable=False)  # 创建人员名称
    creator_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)  # 创建人员ID
    collection_title = db.Column(db.String(50), nullable=False)  # 收集名称
    description = db.Column(db.Text, nullable=False)  # 收集描述
    start_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now())  # 开始时间
    end_date = db.Column(db.DateTime, nullable=False)  # 收集结束时间
    status = db.Column(db.Enum(RELEASE, SAVED, FINISHED,
                               OVERDUE), nullable=False)  # 当前状态
    collection_path = db.Column(db.String(50))  # 应交名单路径

    # def collection_valid(self) -> bool:
    #     """判断收集是否截止
    #
    #     Returns:
    #         bool: 截止情况
    #     """
    #     current_date = datetime.datetime.now()
    #     return current_date < self.end_date  # 当前时间小于截止时间时收集有效


class Question_info(db.Model):
    """ 题目表。

    记录已创建收集的题目相关信息。

    Attributes:
        id: 主键
        collection_id: 收集id（外键：关联collection_info.id）（不可为空）
        qno: 题目序号（不可为空）
        question_type: 题目类型（不可为空）: '0' 上传文件题; '1' 单选; '2' 多选; '3' 姓名题; '4' 学号题; '5' 问卷题(单选); '6' 问卷题(多选)
        question_title: 问题标题（不可为空）
        question_description: 问题描述
        rename_rule: 文件重命名规则
        file_path: 提交文件路径（不可重复）（文件上传题需设置，其余类型不必）
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
    collection_id = db.Column(db.Integer,
                              db.ForeignKey('collection_info.id',
                                            ondelete="CASCADE"),
                              nullable=False)  # 关联收集id
    qno = db.Column(db.Integer, nullable=False)  # 题目序号
    question_type = db.Column(
        db.Enum(FILE_UPLOAD, SINGLE_CHOICE, MULTI_CHOICE, NAME,
                SNO, SINGLE_QUESTIONNAIRE, MULTI_QUESTIONNAIRE),
        nullable=False)  # 题目类型
    question_title = db.Column(db.String(50), nullable=False)  # 问题标题
    question_description = db.Column(db.Text)  # 问题描述
    rename_rule = db.Column(db.String(20))  # 文件重命名规则，其值为题目顺序
    file_path = db.Column(db.String(50), unique=True)  # 提交文件路径


class Answer_info(db.Model):
    """ 答案表。

    记录单选题和多选题的答案。

    Attributes:
        id: 主键
        question_id: 题目id（外键：关联question_info.id）（不可为空）
        collection_id: 收集id（不可为空）
        qno: 题目序号（不可为空）
        answer_option: 答案选项（单选题格式为x，多选题格式为x-x-x-……）（不可为空）
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    question_id = db.Column(db.Integer,
                            db.ForeignKey('question_info.id',
                                          ondelete="CASCADE"),
                            nullable=False)  # 关联题目id
    collection_id = db.Column(db.Integer, nullable=False)  # 收集id
    qno = db.Column(db.Integer, nullable=False)  # 题目序号
    answer_option = db.Column(db.String(30), nullable=False)  # 答案


class Option_info(db.Model):
    """问卷题选项表

    记录问卷题的每一个选项内容。

    Attributes:
        id: 主键
        question_id: 题目id（外键：关联question_info.id）（不可为空）
        collection_id: 收集id（不可为空）
        qno: 题目序号（不可为空）
        option_sn: 选项序号（不可为空）
        option_content: 选项内容（不可为空）
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question_info.id', ondelete="CASCADE"), nullable=False)  # 关联题目id
    collection_id = db.Column(db.Integer, nullable=False)  # 收集id
    qno = db.Column(db.Integer, nullable=False)  # 题目序号
    option_sn = db.Column(db.Integer, nullable=False)  # 选项序号
    option_content = db.Column(db.Text, nullable=False)  # 选项内容


class Submission_info(db.Model):
    """收集提交记录

    记录所有收集的提交记录。

    Attributes:
        id: 主键
        collection_id: 收集id（外键：关联collection_info.id）（不可为空）
        collection_title: 收集标题（不可以为空）
        submitter_name: 提交者姓名（不可以为空）
        submit_time: 提交时间（不可以为空），默认为datetime.datetime.now()
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer,
                              db.ForeignKey('collection_info.id',
                                            ondelete="CASCADE"),
                              nullable=False)  # 关联收集id
    collection_title = db.Column(db.String(50), nullable=False)  # 收集标题
    submitter_name = db.Column(db.String(30), nullable=False)  # 提交者名称
    submit_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.datetime.now())  # 提交时间


class Submit_Content_info(db.Model):
    """ 提交内容信息表。

    记录收集每一题的填写情况。

    Attributes:
        id: 主键
        submission_id: 提交记录id（外键：关联submission_info.id）（不可为空）
        question_id: 题目id（外键：关联question_info.id）（不可为空）
        collection_id: 收集id（不可为空）
        qno: 题目序号（不可为空）
        result: 某个人对这一题的填写结果（若为文件上传题，则此字段存放上传的文件名称）（不可为空）
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    submission_id = db.Column(db.Integer,
                              db.ForeignKey('submission_info.id',
                                            ondelete="CASCADE"),
                              nullable=False)  # 关联提交记录id
    question_id = db.Column(db.Integer,
                            db.ForeignKey('question_info.id',
                                          ondelete="CASCADE"),
                            nullable=False)  # 题目id
    collection_id = db.Column(db.Integer, nullable=False)  # 收集id
    qno = db.Column(db.Integer, nullable=False)  # 问题序号
    result = db.Column(db.String(50), nullable=False)  # 填写结果
