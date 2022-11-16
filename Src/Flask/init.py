from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import sys

app = Flask(__name__)

# ! 设置应用根目录
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# ! 设置文件存储根目录
APP_FILE = os.path.join(APP_ROOT, 'FileStorage')
# ! 设置错误信息根目录
APP_LOG = os.path.join(APP_ROOT, 'LOGS')

# app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
# ? 读取系统环境变量 SECRET_KEY 的值，如果没有读取到，则使用默认值 dev
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
prefix = 'sqlite:///' if sys.platform.startswith('win') else 'sqlite:////'
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')  # 设置数据库连接地址URI
# ? 设置数据库连接地址URI
# * 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# * 以便把文件定位到项目根目录
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),
                                                              os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

""" 数据库配置 """
db = SQLAlchemy(app)  # 在扩展类实例化前加载配置
login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """
    创建用户加载回调函数
    Args:
        user_id: 用户 id

    Returns:
        user: 用户对象
    """
    from models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


"以下引用不能移动"
# from Src.Flask import views, commands
import views, commands, errors
