# HUST-SE 2022 Autumn

#### 介绍

华中科技大学计算机学院 2020 级软件工程项目课程设计

作业收集系统，一个帮助学委的小工具 http://writebug.pythonanywhere.com/

详细文档请查看 https://slapaf.github.io/HUST-SE-2022/

#### 软件功能

- 提交文件自动重命名
- 到期自动汇总提交信息
- 客观题自动评分

![软件流程图](./Docs/images/软件流程示意图.png)

#### 项目成员

| 登录名        | 姓名   | 学号       | 分工                                          | 贡献 |
| ------------- | ------ | ---------- | --------------------------------------------- | ---- |
| wang-guangkai | 王广凯 | U202015355 | 实现动态页面设计，协调 Flask 开发             | 25%  |
| ji-shengxiang | 计胜翔 | U202015362 | 实现数据库，提供相应接口，协调配置服务器环境  | 25%  |
| wzx323232     | 王梓熙 | U202015369 | 实现静态页面设计，协调管理用户信息和权限      | 25%  |
| Miraclezjy    | 张隽翊 | U202015374 | 实现 Flask 框架响应设计，搭建服务器并发布页面 | 25%  |

#### 注意事项

- 代码风格规范参考 [Google 开源项目风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/contents/)。PyCharm 开启 Docstring format 可通过下方路径进行设置，当前设置为 `Google`
  > `文件 -> 设置 -> 工具 -> Python 集成工具 -> Docstrings -> Docstring 格式`
- 目前加入 `.gitignore` 的文件/文件夹有：
  - `.idea/` PyCharm 配置文件
  - `*.xml` 项目配置文件

#### 文档编辑

- `Docs/` 目录存放相关文档的 markdown 文件，`mkdocs.yml` 组织项目结构，使用教程参考
  - [中文文档](https://mkdocs.zimoapps.com/)
  - [English Documentation](https://www.mkdocs.org/)
- 本地文档环境搭建

  - 安装 `MkDocs` 及主题、插件

    ```shell
    pip install mkdocs mkdocs-material mkdocstring mkdocstring[python] mkdocs-glightbox
    ```

  - 检查版本

    ```shell
    $ mkdocs --version
    mkdocs, version 1.4.2 from /.../venv/lib/python3.X/site-packages/mkdocs (Python 3.X)
    ```

  - 启动文档

    在项目的根目录输入如下命令：

    ```shell
    $ mkdocs serve
    INFO     -  Building documentation...
    INFO     -  Cleaning site directory
    INFO     -  Documentation built in 0.21 seconds
    INFO     -  [14:48:02] Watching paths for changes: 'docs', 'mkdocs.yml'
    INFO     -  [14:48:02] Serving on http://127.0.0.1:8000/
    ```

    在浏览器中打开 `http://127.0.0.1/8000`，将看到文档主页。
