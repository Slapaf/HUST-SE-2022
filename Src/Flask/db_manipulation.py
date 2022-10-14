from copy import deepcopy
from datetime import datetime
from flask_login import current_user
from models import Collection_info, Question_info, Answer_info
from init import db


def add_FC(question_dict: list):
    """
    将问卷的信息存入数据库
    Args:
        question_dict:字典类型
        例如：question_dict = {'collectionTitle': '文件收集', 'collector': 'jsx', 'deadline': '2022-10-13T15:18',
                 'description': 'teset','question_name1': '姓名', 'question_file2': '文件', 'checked_topic2': '学号',
                 'question_file3': '文','checked_topic3': '学', 'question_sno4': '学', 'question_sno5': '学号',
                 'question_name6': '姓','question_radio7': '单选','checked_radio7': 'A', 'question_radio8': '单选题',
                 'checked_radio8': 'B'}
    Return:None
    """
    # ! 文件类型可能有多个，设置一个计数器记录是第几个文件
    file_counter = 0  # * 文件计数器

    # 前端传来的deadLine为string类型，在此转化为datetime类型
    list_of_question_dict = deepcopy(question_dict)  # ! 保存元组的列表，与字典类型的区别在于是否对 key 去重
    print(list_of_question_dict)

    question_dict = dict(question_dict)
    deadline = question_dict['deadline']
    deadline = deadline.replace("T", " ")
    format = '%Y-%m-%d %H:%M'
    question_dict['deadline'] = datetime.strptime(deadline, format)

    # ! 调试用，使用完毕删除
    print(question_dict)
    # ! finish

    # 创建一个文件收集对象,更新文件收集主表里
    collection = Collection_info(creator=question_dict['collector'], creator_id=current_user.id,
                                 collection_title=question_dict['collectionTitle'],
                                 description=question_dict['description'],
                                 end_date=question_dict['deadline'],
                                 status=Collection_info.SAVED)
    db.session.add(collection)
    db.session.commit()  # 提交数据库会话，否则id为None
    collection_id = collection.id

    key_list = list(question_dict.keys())
    # 问题的键列表
    question_key_list = [question_key for question_key in key_list if "question" in question_key]

    # 更新问题主表和答案表
    for question_key in question_key_list:
        # ? 若为填空题
        if "sno" in question_key or "name" in question_key:
            question = Question_info(collection_id=collection_id,
                                     num=int(question_key[-1]),
                                     question_type=Question_info.FILL_IN_BLANK,
                                     question_description=question_dict[question_key])
            db.session.add(question)
            db.session.commit()

        # ? 若为单选题
        elif "radio" in question_key:
            question = Question_info(collection_id=collection_id,
                                     num=int(question_key[-1]),
                                     question_type=Question_info.SINGLE_CHOICE,
                                     question_description=question_dict[question_key])
            db.session.add(question)
            db.session.commit()
            # 存选择题答案
            answer = Answer_info(collection_id=collection_id,
                                 question_id=question.id,
                                 answer_content=question_dict['checked_radio' + question_key[-1]])
            db.session.add(answer)
            db.session.commit()

        # ? 若为文件上传题
        elif "file" in question_key:
            # TODO 确定文件重命名规则
            file_counter += 1
            rename_rule = ""
            rename_rule_list = []  # * 重命名所需的题目
            question_num = question_key[-1]
            for elem in list_of_question_dict:
                if elem[0] == "checked_topic" + question_num:
                    rename_rule_list.append(elem[1])
            print(rename_rule_list)

            # TODO 逻辑有待优化，且 rename_rule 未添加分隔符

            cnt = 0
            # for idx in range(len(tmp)):
            #     if tmp[idx][1] not in rename_rule_list:
            #         continue
            #     rename_rule += tmp[idx][0][-1]
            for elem in list_of_question_dict:
                if elem[1] not in rename_rule_list:
                    continue
                rename_rule += elem[0]  # ! 待添加分隔符
                cnt += 1
                if cnt >= len(rename_rule_list):  # * 防止获取到文件后面的重命名规则
                    break
            print(rename_rule)
            # return
            #
            # rename_rule = '2'
            # index = 'checked_topic' + question_key[-1]
            # if index in key_list:
            #     if question_dict[index] == '姓名':
            #         rename_rule = '0'
            #     elif question_dict[index] == '学号':
            #         rename_rule = '1'
            ###########################
            # TODO 生成文件存储路径，将文件存储路径放在用户所属的路径下，引入随机数（需使用 file_counter）
            ###########################
            question = Question_info(collection_id=collection_id,
                                     num=int(question_key[-1]),
                                     question_type=Question_info.FILE_UPLOAD,
                                     question_description=question_dict[question_key],
                                     rename_rule=rename_rule)
            db.session.add(question)
            db.session.commit()
