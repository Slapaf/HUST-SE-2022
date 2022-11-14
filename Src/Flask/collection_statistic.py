from pathlib import Path

from flask import Flask, Response
import os
import zipfile
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


def dir2zip(zip_source_dir: str, zip_destination_dir: str, zip_file_name: str):
    """将指定文件夹压缩为 zip 压缩文件

    Args:
        zip_source_dir (str): 源文件夹，待压缩的文件夹
        zip_destination_dir (str): 目标文件夹，压缩文件存放的位置
        zip_file_name (str): 压缩文件名
    """
    # print("压缩函数测试")
    # with zipfile.ZipFile(zip_destination_dir + '.zip', mode='w',
    #                      compression=zipfile.ZIP_DEFLATED) as zf:
    #     parent_dir, cur_dir = os.path.split(zip_source_dir)
    #     zf.write(zip_source_dir, arcname=zip_file_name)
    #     print("压缩成功！.zip 文件位于 {} 目录下".format(zip_destination_dir))
    f_zip = zipfile.ZipFile(os.path.join(zip_destination_dir, zip_file_name + '.zip'), "w", zipfile.ZIP_DEFLATED)
    for path, dir_names, file_names in os.walk(zip_source_dir):
        fpath = path.replace(zip_source_dir, '')
        for file_name in file_names:
            f_zip.write(os.path.join(path, file_name), os.path.join(fpath, file_name))
    f_zip.close()
    print("压缩成功! .zip 文件位于 {} 目录下。".format(zip_destination_dir))
