from init import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


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
    username = db.Column(db.String(20), unique=True)  # 用户名
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


# 文件收集主表
class Collection_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    creator_id = db.Column(db.Integer)  # 创建人员ID
    collection_title = db.Column(db.String(20), nullable=False)  # 收集名称（不可以为空）
    description = db.Column(db.Text, nullable=False)  # 收集描述（可以为空）
    start_date = db.Column(db.DateTime, default=datetime.datetime.now())  # 开始时间自动设置为创建收集的时间
    end_date = db.Column(db.DateTime, nullable=True)  # 收集结束时间（不可以为空）
    status = db.Column(db.CHAR)  # 当前状态：0 发布;1 暂存;2 已结束;3 已失效


# 问题主表
class question_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer)  # 关联文件收集主表id
    question_type = db.Column(db.CHAR)  # 问题类型：0 解答题（需上传文件）;1 单选;2 多选;3 填空
    question_description = db.Column(db.Text, nullable=True)  # 收集描述（不可以为空）
    required_flag = db.Column(db.BOOLEAN, nullable=False)  # （暂定） 0 必填;1 非必填


# 选项表
class option_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer)  # 关联文件收集主表id
    question_id = db.Column(db.Integer)  # 关联问题主表id
    option_name = db.Column(db.CHAR)  # 选项名称
    option_content = db.Column(db.Text, nullable=True)  # 选项内容（不可以为空）

# 答案表
class answer_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    collection_id = db.Column(db.Integer)  # 关联文件收集主表id
    question_id = db.Column(db.Integer)  # 关联问题主表id
    option_id = db.Column(db.Integer)  # 关联问题主表id
    answer_content = db.Column(db.Text)  # 答案不可为空
