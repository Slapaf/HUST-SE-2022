# 欢迎使用嘟嘟可收件箱

## 0. 快速定位

- 我是用户

作为老师或班委，我该如何快捷收集各种作业/文件？ [我是收集者](./user-guide/collector.md)

作为提交者，我该如何通过收集链接提交作业/文件？ [我是提交者](./user-guide/submitter.md)

- 我是开发者

作为开源爱好者，我可以从哪里了解项目的详细结构？ [我是开发者](./developer/dev-pro.md)

## 1. 项目说明
### 作业收集系统，一个帮助学委的小工具
### 基于flask的Web开发，主要功能：
- 注册用户创建收集后，分享收集链接，供他人填写提交
- 选择题自动批改
- 选择题、问卷题数据统计
- 可设置应交名单，并邮件催交
- 下载提交文件
## 2. 文档结构（完成后删除）

    mkdocs.yml                  # The configuration file.
    docs/
        about/
            about-us.md         # Who we are.
            release-notes.md    # Release notes about project.
        user-guide/
            collector.md        # How to use if you are a collector.
            submitter.md        # How to use if you are a submitter.
        index.md                # The documentation homepage.
        ...                     # Other markdown pages, images and other files.

    mkdocs.yml                  # 配置文件
    doc/
        about/
            about-us.md         # 关于我们
            release_notes.md    # 发行注记
        developer/
            web.md              # 前端网页设计
            flask.md            # Flask 响应设计
            database.md         # 数据库设计
        user-guide/
            collector.md        # 收集者使用指南
            submitter.md        # 提交者使用指南
        index.md                # 文档主页
    src/
        Flask/
            static/
            templates/
        ...
    ...
