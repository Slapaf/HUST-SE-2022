from datetime import datetime
from flask_login import current_user
from models import Collection_info, Question_info, Answer_info
from init import db


def add_FC(question_dict):
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

    # 前端传来的deadLine为string类型，在此转化为datetime类型
    deadline = question_dict['deadline']
    deadline = deadline.replace("T", " ")
    format = '%Y-%m-%d %H:%M'
    question_dict['deadline'] = datetime.strptime(deadline, format)

    # 创建一个文件收集对象,更新文件收集主表里
    collection = Collection_info(creator=question_dict['collector'], creator_id=current_user.id,
                                 collection_title=question_dict['collectionTitle'],
                                 description=question_dict['description'], end_date=question_dict['deadline'],
                                 status='1')
    db.session.add(collection)
    db.session.commit()  # 提交数据库会话，否则id为None
    collection_id = collection.id

    key = list(question_dict.keys())
    question_keylist = [v for v in key if "question" in v]  # 问题的键列表

    # 更新问题主表和答案表
    for k in question_keylist:
        # ? 若为填空题
        if "sno" in k or "name" in k:
            question = Question_info(collection_id=collection_id,
                                     num=int(k[-1]),
                                     question_type=Question_info.FILL_IN_BLANK,
                                     question_description=question_dict[k])
            db.session.add(question)
            db.session.commit()

        # ? 若为单选题
        if "radio" in k:
            question = Question_info(collection_id=collection_id,
                                     num=int(k[-1]),
                                     question_type=Question_info.SINGLE_CHOICE,
                                     question_description=question_dict[k])
            db.session.add(question)
            db.session.commit()
            # 存选择题答案
            answer = Answer_info(collection_id=collection_id,
                                 question_id=question.id,
                                 answer_content=question_dict['checked_radio' + k[-1]])
            db.session.add(answer)
            db.session.commit()

        # ? 若为文件上传题
        if "file" in k:
            # TODO 确定文件重命名规则
            rename_rule = '2'
            index = 'checked_topic' + k[-1]
            if index in key:
                if question_dict[index] == '姓名':
                    rename_rule = '0'
                elif question_dict[index] == '学号':
                    rename_rule = '1'
            ###########################
            #    Todo 设置文件存储路径   #

            ###########################
            question = Question_info(collection_id=collection_id,
                                     num=int(k[-1]),
                                     question_type='1',
                                     question_description=question_dict[k],
                                     rename_rule=rename_rule)
            db.session.add(question)
            db.session.commit()
