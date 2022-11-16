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

```

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

`templates/` 目录下存放所有 html 网页文件（交代一下网页文件夹的分类，后期处理）

## 2.3 Python 文件

`Flask/` 目录下还有很多 Python 文件：

```

```

重要的有以下这些文件：

- `init.py`: 初始化 Flask 程序
- `views.py`: 视图函数
- `models.py`: 数据库类定义
- `errors.py`: 错误处理
- `db_manipulation.py`: 数据库 API 定义
- `collection_statistic.py`: 统计函数

## 3. 配置文件

除去上面已经介绍过的部分，`Src/` 目录下还有几个比较重要的配置文件。

### 3.1 requirements.txt

`requirements.txt` 文件记录了项目所依赖的全部 Python 包以及版本要求，配置环境时可以使用以下命令快速检查和补充所需要的包。

```shell
pip install -r requirements.txt
```

### 3.2 mkdocs.yml

`mkdocs.yml` 文件记录了该项目文档的配置信息，自定义配置可以参考

- [mkdocs-material](https://squidfunk.github.io/mkdocs-material/reference/)
- [mkdocstrings-python](https://mkdocstrings.github.io/python/)
