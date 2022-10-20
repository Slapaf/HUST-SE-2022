import random
import string

from init import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    """ 用户信息

    Description:
        记录已注册用户的相关信息。

    Attributes:
        1. id: 主键
        2. name: 名字（用户昵称）
        3. username: 用户名
        4. password_hash: 密码散列值
        TODO 5. userpath: 用户空间路径
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字（用户昵称）
    username = db.Column(db.String(20), unique=True)  # 用户名（不可重复）
    password_hash = db.Column(db.String(128))  # 密码散列值
    userpath = db.Column(db.String(20), unique=True)  # 用户空间路径
    email = db.Column(db.String(20), nullable=False, unique=True)  # 用户邮箱

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

    def set_filepath(self):
        """
        用于设置用户空间路径的方法

        Returns:
            None
        """
        # * 将 "用户名" + 随机字符串 作为用户空间路径，总长度为 20 位
        self.userpath = self.username + ''.join(
            random.sample(string.ascii_letters + string.digits, 20 - len(self.username))
        )


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
        TODO 9. namelist_path: 应交名单路径
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
    namelist_path = db.Column(db.String(20))  # 应交名单路径

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
        5. question_description: 问题描述（不可为空）
        TODO 6. required_flag: 是否为必填项（暂定）
        TODO 7. rename_rule: 文件重命名规则
        8. file_path: 提交文件路径
    """
    # * 问题类型常量
    FILE_UPLOAD, SINGLE_CHOICE, MULTI_CHOICE, FILL_IN_BLANK = '0', '1', '2', '3'  # ? 解答题，单选，多选，填空

    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer)  # 关联文件收集主表id
    qno = db.Column(db.Integer)  # 问题序号
    question_type = db.Column(db.CHAR)  # 问题类型：0 解答题（需上传文件）;1 单选;2 多选;3 填空
    question_description = db.Column(db.Text, nullable=False)  # 问题描述（不可以为空）
    # required_flag = db.Column(db.BOOLEAN, nullable=False)  # （暂定） 0 必填;1 非必填
    # rename_rule = db.Column(db.CHAR, default='2')  # 若为解答题（需上传文件）,表示文件重命名规则：0 姓名;1 学号;2 无需重命名或其他类型题目
    rename_rule = db.Column(db.String(20))  # 文件重命名规则，其值为题目顺序
    file_path = db.Column(db.String(30))  # 提交文件路径（文件上传题需设置，其余类型不必）


class Answer_info(db.Model):
    """ 答案表

    Description:
        记录已创建收集的相关信息。

    Attributes:
        1. id: 主键
        2. collection_id: 关联文件收集主表 id
        3. question_id: 关联问题主表 id
        TODO 4. option_id: 关联选项主表 id
        5. answer_option: 答案不可为空
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer)  # 关联文件收集主表id
    question_id = db.Column(db.Integer)  # 关联问题主表id
    # option_id = db.Column(db.Integer)  # 关联选项主表id
    answer_option = db.Column(db.CHAR)  # 答案不可为空


class CollectionResult_info(db.Model):
    """问卷填写结果表

    Description:
        记录问卷填写情况。

    Attributes:
        1. id: 主键
        2. collection_id: 关联文件收集主表id（不可为空）
        3. question_id: 关联问题主表id（不可为空）
        4. result: 某个人对这一题的填写结果（若为文件上传题，则此字段存放上传的文件名称）（不可为空）
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer, nullable=False)  # 关联文件收集主表id（不可为空）
    # question_id = db.Column(db.Integer, nullable=False)  # 关联问题主表id（不可为空）
    qno = db.Column(db.Integer)  # 问题序号
    result = db.Column(db.String(30), nullable=False)  # 某个人对这一题的填写结果（若为文件上传题，则此字段存放上传的文件名称）（不可为空）

# # 选项表
# class option_info(db.Model):
#     id = db.Column(db.Integer, primary_key=True)  # 主键
#     collection_id = db.Column(db.Integer)  # 关联文件收集主表id
#     question_id = db.Column(db.Integer)  # 关联问题主表id
#     option_name = db.Column(db.CHAR)  # 选项名称
#     option_content = db.Column(db.Text, nullable=True)  # 选项内容（不可以为空）


# class FileCollection(db.Model):
#     """ TODO 文件收集 （功能待完善）
#
#     Description:
#         记录管理者创建的文件收集的相关信息。
#
#     Attributes:
#         id: 主键
#         collection_title: 收集名称
#         start_date: 收集开始时间
#         end_date: 收集结束时间
#         namelist_path: 应交名单路径
#         file_path: 提交文件路径
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     collection_title = db.Column(db.String(20))  # 收集名称
#     start_date = db.Column(db.DateTime)  # 收集开始时间
#     end_date = db.Column(db.DateTime)  # 收集结束时间
#     namelist_path = db.Column(db.String(20))  # 应交名单路径
#     file_path = db.Column(db.String(20))  # 提交文件路径
#
#     def set_collection_date(self, deadline: datetime.datetime):
#         """
#         设置收集的开始和结束时间
#
#         Args:
#             deadline: 截止时间
#
#         Returns:
#             None
#         """
#         self.start_date = datetime.datetime.now()  # 开始时间设置为创建收集的时间
#         self.end_date = deadline  # 结束时间设置
#
#     def collection_valid(self):
#         """
#         判断收集是否截止
#
#         Returns:
#             (bool): 截止情况
#         """
#         current_date = datetime.datetime.now()
#         return current_date < self.end_date  # 当前时间小于截止时间时收集有效
