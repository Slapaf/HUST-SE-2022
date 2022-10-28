# -*- coding: utf-8 -*-
# @Time    : 2022/10/28 下午4:24
# @Author  : Nobody
# @File    : mail_related.py
# @Software: PyCharm
# @Description: 邮件相关功能的实现
import re
import time
import yagmail

user_email = 'miraclejunyi@sina.com'
user_pwd = 'f92a6b73f334be6c'
user_host = 'smtp.sina.com'

# yag = yagmail.SMTP(user='miraclejunyi@sina.com', password='f92a6b73f334be6c', host='smtp.sina.com')

message_to_send = '<a href="https://pypi.python.org/pypi/sky/">Click me!</a>'


class EmailUser:

    def __init__(self):
        self.yag = None

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


if __name__ == "__main__":
    user_demo = EmailUser()
    user_demo.user_authentication(user_email=user_email, user_pwd=user_pwd, host=user_host)
    email_destination = ['729695343@qq.com', '3104746045@qq.com']
    if user_demo.send_email(email_destination, 'Test Email', message_to_send):
        print("发送成功")
    else:
        print("发送失败，目标邮箱地址错误")
