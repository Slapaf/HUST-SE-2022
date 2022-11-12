from flask import Flask, Response
import os
import mimetypes
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

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


def generate_excel(due_list: list,
                   submitted_list: list,
                   excel_name: str = 'demo',
                   excel_path: str = './'):
    """生成汇总 Excel 表格

    Args:
        due_list (list): 应交名单列表
        submitted_list (list): 已交名单列表
        excel_name (str, optional): 汇总表格名称，默认 'demo'
        excel_path (str, optional): 汇总表格地址. 默认 './'.
    """
    submit_status = [
        '已提交' if name in submitted_list else '未提交' for name in due_list
    ]
    excel_path += excel_name + '.xlsx'
    df = pd.DataFrame({'成员名单': due_list, '提交状态': submit_status})
    df.to_excel(excel_path, sheet_name='提交情况', index=False)
    # 设置样式
    red_fill = PatternFill('solid', start_color='ff9198')
    green_fill = PatternFill("solid", start_color='a1ddaa')
    # 应用样式
    wb = load_workbook(excel_path)
    ws = wb.active
    cells = ws.iter_rows(min_row=2, min_col=2)
    for cell in cells:
        cell[0].fill = green_fill if cell[0].value == '已提交' else red_fill
    # 保存表格
    wb.save("demo.xlsx")
    wb.close()
