# 欢迎使用嘟嘟可收件箱

详细文档请查看 [HUST-211](https://baidu.com)

## 0. 快速定位

作为老师或班委，我该如何快捷收集各种作业/文件？ [我是收集者](./user-guide/collector.md)

作为提交者，我该如何通过收集链接提交作业/文件？ [我是提交者](./user-guide/submitter.md)

## 1. 系统说明

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
