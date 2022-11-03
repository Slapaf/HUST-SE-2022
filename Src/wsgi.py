# -*- coding: utf-8 -*-
# @Time    : 2022/11/3 下午4:28
# @Author  : Nobody
# @File    : wsgi.py
# @Software: PyCharm
# @Description: 手动设置环境变量并导入程序实例

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from Flask import app
