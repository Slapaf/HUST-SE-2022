# Flask 响应设计

## 1. 用户相关模块

### 1.1 账号处理

登录状态相关函数有 `register`、`login`、`logout`，分别用于[用户注册](#111)、[用户登录](#112)、[用户登出](#113)。

#### 1.1.1 用户注册

用户注册通过 `register` 实现，支持用户创建账号。

!!! note "关于创建账号"

    创建账号存在一定的限制，用户名必须唯一且未注册过，密码需要符合要求。

    账号创建成功后，会为该账号分配一个唯一的文件目录，位于 APP_FILE 下。

::: views.register

#### 1.1.2 用户登录

用户登录通过 `login` 实现，支持用户通过已注册的账号登录。

::: views.login

#### 1.1.3 用户登出

用户登出通过 `logout` 实现，支持登录态的用户退出登录。

::: views.logout

### 1.2 个人信息

个人信息相关处理通过 `personal_homepage` 实现，支持用户修改个人信息、修改密码。

!!! note "关于修改密码"

    修改密码成功或失败，系统会给出相应的提示。

::: views.personal_homepage

## 2. 收集相关模块

与收集功能相关的函数有 `generate_collection`、`file_editing`、`copy_collection`、`collection_details`，分别用于[创建收集](#21)、[编辑/重启收集](#22)、[复制收集](#23)、[查看收集详情](#24)。

### 2.1 创建收集

创建收集通过 `generate_collection` 实现，支持登录用户创建收集。

::: views.generate_collection

### 2.2 编辑/重启收集

编辑或重启收集通过 `file_editing` 实现，支持登录用户编辑进行中的收集或者重启已截止的收集。

::: views.file_editing

### 2.3 复制收集

复制收集通过 `copy_collection` 实现，支持登录用户在原有收集基础上设置新的收集。

::: views.copy_collection

### 2.4 查看收集详情

查看收集详情通过 `collection_details` 实现，支持登录用户查看收集的具体收集情况。

::: views.collection_details

## 3. 统计相关模块

与统计功能相关的函数有 `mycollection`、……，分别用于[用户收集汇总](#31)、……。

### 3.1 用户收集汇总

汇总用户创建的所有收集通过 `mycollection` 实现，支持登录用户查看收集总览。

::: views.mycollection

### 3.2 收集表格汇总

### 3.3 收集文件汇总
