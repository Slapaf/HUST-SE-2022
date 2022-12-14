# 数据库 DB 设计

## 1. 数据库表结构设计

数据库包含以下表项：[用户信息表](#11)、[收集信息表](#12)、[题目信息表](#13)、[选项信息表](#14)、[答案信息表](#15)、[提交信息表](#16)、[内容信息表](#17)

### 1.1 用户信息表

用户信息表项代码设计如下。

::: models.User

### 1.2 收集信息表

收集信息表项代码设计如下。

::: models.Collection_info

### 1.3 题目信息表

题目信息表项代码设计如下。

::: models.Question_info

### 1.4 选项信息表

选项信息表项代码设计如下。

::: models.Option_info

### 1.5 答案信息表

答案信息表项代码设计如下。

::: models.Answer_info

### 1.6 提交信息表

提交信息表项代码设计如下。

::: models.Submission_info

### 1.7 内容信息表

提交内容信息表项代码设计如下。

::: models.Submit_Content_info

## 2. 数据库 API 设计

数据库提供了一系列操作接口方便 Flask 视图函数处理数据。

### 2.1 帐号信息相关

#### 2.1.1 修改密码

修改密码通过 `modify_password` 实现。

:::db_manipulation.modify_password

#### 2.1.2 修改个人信息

修改个人信息通过 `modify_personal_info` 实现。

:::db_manipulation.modify_personal_info

### 2.2 收集信息相关

#### 2.2.1 添加收集问卷

添加收集通过 `add_FC` 实现。

:::db_manipulation.add_FC

#### 2.2.2 删除收集问卷

删除收集通过 `delete_collection` 实现。

:::db_manipulation.delete_collection

#### 2.2.3 查看收集信息

查看收集信息通过 `get_question_dict` 实现。

:::db_manipulation.get_question_dict

#### 2.2.4 修改收集信息

修改已创建收集的信息通过 `modify_collection` 实现。

:::db_manipulation.modify_collection

#### 2.2.5 获取提交信息

获取某个收集的提交信息通过 `submission_record` 实现。

:::db_manipulation.submission_record

对应的另一个版本是 `submission_record_v2`，相比 `submission_record` 多返回了提交 id。

:::db_manipulation.submission_record_v2

#### 2.2.6 添加提交信息

向数据库中添加用户填写的内容通过 `save_submission` 实现。

:::db_manipulation.save_submission

#### 2.2.7 提交文件存储

将提交者上传的文件存储到正确的位置通过 `file_upload` 实现。

:::db_manipulation.file_upload

### 2.3 状态更新相关

#### 2.3.1 计算收集截止倒计时

计算某个收集还有多长时间截止的倒计时通过 `deadline_countdown` 实现。

:::db_manipulation.deadline_countdown

#### 2.3.4 修改收集状态为截止

将收集的状态修改为“已截止”通过 `stop_collection` 实现。

:::db_manipulation.stop_collection

### 2.4 统计汇总相关

#### 2.4.1 统计提交数量

统计提交数量通过 `count_submission` 实现。

:::db_manipulation.count_submission

#### 2.4.2 统计已收文件数

统计已收文件数通过 `count_filenum` 实现。

:::db_manipulation.count_filenum

#### 2.4.3 获取收集信息和提交记录

获取收集信息和指定 id 的用户提交内容通过 `get_submission_dict` 实现。

:::db_manipulation.get_submission_dict

#### 2.4.4 统计答题情况

统计选择题、问卷题答题情况通过 `collection_data_statistics` 实现。

:::db_manipulation.collection_data_statistics
