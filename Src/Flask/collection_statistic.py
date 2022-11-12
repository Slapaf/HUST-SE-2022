from flask import Flask, Response
import os
import mimetypes

from init import app


@app.route('/download/<path:filename>')
def download_file(filename):
    """下载文件

    Args:
        filename (str): 文件名

    """
    base_dir = os.getcwd()  # ! 目前代表该 py 文件所在目录，需要修改为收集所在目录
    path_name = os.path.join(base_dir, filename)
    f = open(path_name, "rb")
    response = Response(f.readlines())
    mime_type = mimetypes.guess_type(filename)[0]
    response.headers['Content-Type'] = mime_type
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(
        filename.encode().decode('latin-1')
    )
    return response
