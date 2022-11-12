# 数据库 DB 设计

## 1. 数据库表结构设计

数据库包含以下表项：[用户信息表](#11)、[收集信息表](#12)、[题目信息表](#13)、[选项信息表](#14)、[答案信息表](#15)、[提交信息表](#16)、[内容信息表](#17)

### 1.1 用户信息表

用户信息表项代码设计如下。

::: Src.Flask.models.User

### 1.2 收集信息表

收集信息表项代码设计如下。

::: Src.Flask.models.Collection_info

### 1.3 题目信息表

题目信息表项代码设计如下。

::: Src.Flask.models.Question_info

### 1.4 选项信息表

选项信息表项代码设计如下。

::: Src.Flask.models.Option_info

### 1.5 答案信息表

答案信息表项代码设计如下。

::: Src.Flask.models.Answer_info

### 1.6 提交信息表

提交信息表项代码设计如下。

::: Src.Flask.models.Submission_info

### 1.7 内容信息表

提交内容信息表项代码设计如下。

::: Src.Flask.models.Submit_Content_info

## 2. 数据库 API 设计

数据库提供了一系列操作接口方便 Flask 视图函数处理数据。
