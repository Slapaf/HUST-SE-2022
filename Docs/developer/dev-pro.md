# 项目结构

整个项目的结构如下图所示。

```
SE2022-Code/
├── Docs
│   ├── about
│   ├── developer
│   ├── images
│   └── user-guide
└── Src
    └── Flask
        ├── static
        ├── stopwords
        └── templates
```

## 1. 文档部分

`Docs/` 目录下存放所有项目文档的 `.md` 文件以及其他一些资源。

## 2. 代码部分

`Src/` 目录下存放所有项目代码资源。其中最重要的是 `Flask/` 目录。

`Src/` 目录结构如下。

```shell
Src/
├── data.db
├── Flask
│   ├── app.py
│   ├── collection_statistic.py
│   ├── commands.py
│   ├── db_manipulation.py
│   ├── EaD.py
│   ├── errors.py
│   ├── init.py
│   ├── models.py
│   ├── static
│   │   ├── alert.css
│   │   ├── css
│   │   │   ├── all.css
│   │   │   ├── collect_details.css
│   │   │   ├── create_link.css
│   │   │   ├── file_collecting.css
│   │   │   ├── file_preview.css
│   │   │   ├── file_submitting.css
│   │   │   ├── index.css
│   │   │   ├── login.css
│   │   │   ├── mycollection_1.css
│   │   │   ├── mycollection.css
│   │   │   ├── personal_homepage.css
│   │   │   └── register.css
│   │   ├── favicon.ico
│   │   ├── iconfont
│   │   │   ├── demo.css
│   │   │   ├── demo_index.html
│   │   │   ├── iconfont.css
│   │   │   ├── iconfont.js
│   │   │   ├── iconfont.json
│   │   │   ├── iconfont.ttf
│   │   │   ├── iconfont.woff
│   │   │   └── iconfont.woff2
│   │   ├── images
│   │   │   ├── 1.svg
│   │   │   ├── collectioncard_1.png
│   │   │   ├── collectioncard_2.png
│   │   │   ├── collectioncard_m.png
│   │   │   ├── collectioncard.png
│   │   │   ├── collectiondetailcard_1.png
│   │   │   ├── collectiondetailcard.png
│   │   │   ├── Dodoco.png
│   │   │   ├── favicon-16.png
│   │   │   ├── favicon-32.png
│   │   │   ├── keli.gif
│   │   │   ├── left-bottom.png
│   │   │   ├── left-top.png
│   │   │   ├── mycollectioncard_1.png
│   │   │   ├── mycollectioncard.png
│   │   │   ├── portrait.png
│   │   │   ├── right-bottom.png
│   │   │   ├── right-top.png
│   │   │   ├── round1.png
│   │   │   ├── round2.png
│   │   │   ├── test.png
│   │   │   └── touxiang.png
│   │   ├── js
│   │   │   ├── collect_detail_chart.js
│   │   │   ├── collect_details.js
│   │   │   ├── file_collecting.js
│   │   │   ├── file_editing.js
│   │   │   ├── file_preview.js
│   │   │   ├── file_submitting.js
│   │   │   ├── mycollection.js
│   │   │   └── personal_homepage.js
│   │   └── js_not_compressed
│   │       ├── collect_detail_chart.js
│   │       ├── file_collecting.js
│   │       ├── file_editing.js
│   │       ├── file_preview.js
│   │       ├── file_submitting.js
│   │       ├── mycollection.js
│   │       └── personal_homepage.js
│   ├── templates
│   │   ├── 404.html
│   │   ├── collection_details.html
│   │   ├── create_link.html
│   │   ├── file_collecting.html
│   │   ├── file_editing.html
│   │   ├── file_preview.html
│   │   ├── file_submitting.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── mycollection.html
│   │   ├── personal_homepage.html
│   │   ├── register.html
│   │   └── submit_successfully.html
│   ├── test.py
│   └── views.py
└── wsgi.py
```

## 2.1 static 目录

`static/` 目录下存放网页相关的文件，包括 `css/`、`iconfont/`、`images/`、`js/` 文件夹。

`static/` 目录结构如下。

```
static/
├── css
├── iconfont
├── images
└── js
```

## 2.2 templates 目录

`templates/` 目录下存放所有 html 网页文件。

```shell
templates/
├── 404.html
├── collection_details.html
├── create_link.html
├── file_collecting.html
├── file_editing.html
├── file_preview.html
├── file_submitting.html
├── index.html
├── login.html
├── mycollection.html
├── personal_homepage.html
├── register.html
└── submit_successfully.html

```

## 2.3 Python 文件

`Flask/` 目录下，重要的有这些 Python 文件：

- `init.py`: 初始化 Flask 程序
- `views.py`: 视图函数
- `models.py`: 数据库类定义
- `errors.py`: 错误处理
- `db_manipulation.py`: 数据库 API 定义
- `collection_statistic.py`: 统计函数

## 3. 配置文件

除去上面已经介绍过的部分，`Src/` 目录下还有几个比较重要的配置文件，这里简单介绍一下 `requirements.txt` 和 `mkdocs.yml`。

### 3.1 requirements.txt

`requirements.txt` 文件记录了项目所依赖的全部 Python 包以及版本要求，配置环境时可以使用以下命令快速检查和补充所需要的包。

```shell
pip install -r requirements.txt
```

### 3.2 mkdocs.yml

`mkdocs.yml` 文件记录了该项目文档的配置信息，自定义配置可以参考

- [mkdocs-material](https://squidfunk.github.io/mkdocs-material/reference/)
- [mkdocstrings-python](https://mkdocstrings.github.io/python/)
