from flask import render_template
from init import app


@app.errorhandler(404)
def page_not_found(e):
    """404 错误处理函数

    Args:
        e (str): 异常对象
    """
    return render_template('404.html'), 404
