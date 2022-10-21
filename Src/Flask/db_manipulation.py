import string
from copy import deepcopy
from datetime import datetime
import random
import os
from flask_login import current_user
from models import Collection_info, Question_info, Answer_info, Submit_Content_info, Option_info, Submission_info
from init import db
from datetime import datetime
from werkzeug.datastructures import MultiDict
import shutil


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

    list_of_question_dict = deepcopy(question_dict)  # ! 保存元组的列表，与字典类型的区别在于是否对 key 去重
    # print(list_of_question_dict)

    question_dict = MultiDict(question_dict)
    # 前端传来的deadLine为string类型，在此转化为datetime类型
    deadline = question_dict['deadline']
    deadline = deadline.replace("T", " ")
    ddl_format = '%Y-%m-%d %H:%M'
    question_dict['deadline'] = datetime.strptime(deadline, ddl_format)

    # 创建一个文件收集对象,更新文件收集主表里
    collection = Collection_info(creator=question_dict['collector'],
                                 creator_id=current_user.id,
                                 collection_title=question_dict['collectionTitle'],
                                 description=question_dict['description'],
                                 end_date=question_dict['deadline'],
                                 status=Collection_info.SAVED)
    db.session.add(collection)
    db.session.commit()  # 提交数据库会话，否则 id 为None
    collection_id = collection.id

    key_list = list(question_dict.keys())
    # 问题的键列表
    question_key_list = [question_key for question_key in key_list if "question" in question_key]

    # 更新问题主表和答案表
    for question_key in question_key_list:
        # ? 若为填空题
        if "sno" in question_key or "name" in question_key:
            question = Question_info(collection_id=collection_id,
                                     qno=int(question_key[-1]),
                                     question_type=Question_info.FILL_IN_BLANK,
                                     question_title=question_dict[question_key],
                                     question_description=question_dict['detail' + question_key[-1]])
            db.session.add(question)
            db.session.commit()

        # ? 若为单选题
        elif "radio" in question_key:
            question = Question_info(collection_id=collection_id,
                                     qno=int(question_key[-1]),
                                     question_type=Question_info.SINGLE_CHOICE,
                                     question_title=question_dict[question_key],
                                     question_description=question_dict['detail' + question_key[-1]])
            db.session.add(question)
            db.session.commit()
            # 存选择题答案
            answer = Answer_info(collection_id=collection_id,
                                 question_id=question.id,
                                 qno=int(question_key[-1]),
                                 answer_option=question_dict['question_radio' + question_key[-1]])
            db.session.add(answer)
            db.session.commit()

        # ? 若为多选题
        elif "multipleChoice" in question_key:
            question = Question_info(collection_id=collection_id,
                                     qno=int(question_key[-1]),
                                     question_type=Question_info.MULTI_CHOICE,
                                     question_title=question_dict[question_key],
                                     question_description=question_dict['detail' + question_key[-1]])
            db.session.add(question)
            db.session.commit()
            # 存选择题答案
            ano_list = question_dict.getlist('checked_mulans' + question_key[-1])
            for ano in ano_list:
                answer = Answer_info(collection_id=collection_id,
                                     question_id=question.id,
                                     qno=int(question_key[-1]),
                                     answer_option=ano)
                db.session.add(answer)
            db.session.commit()

        # ? 若为问卷题
        elif "question_qnaire" in question_key:
            if question_dict['choose_type' + question_key[-1]] == 'single':
                qn_type = Question_info.SINGLE_QUESTIONNAIRE
            else:
                qn_type = Question_info.MULTI_QUESTIONNAIRE
            question = Question_info(collection_id=collection_id,
                                     qno=int(question_key[-1]),
                                     question_type=qn_type,
                                     question_title=question_dict[question_key],
                                     question_description=question_dict['detail' + question_key[-1]])
            db.session.add(question)
            db.session.commit()
            # 存问卷题目各选项的内容
            option_content = question_dict.getlist('qn_option' + question_key[-1])
            for i in range(len(option_content)):
                option = Option_info(collection_id=collection_id,
                                     question_id=question.id,
                                     qno=int(question_key[-1]),
                                     option_sn=i,
                                     option_content=option_content[i])
                db.session.add(option)
            db.session.commit()

        # ? 若为文件上传题
        elif "file" in question_key:
            # TODO 确定文件重命名规则
            file_counter += 1
            rename_rule = []
            rename_rule_list = []  # * 重命名所需的题目
            question_num = question_key[-1]
            for elem in list_of_question_dict:
                if elem[0] == "checked_topic" + question_num:
                    rename_rule_list.append(elem[1])
            # print(rename_rule_list)

            # TODO 逻辑有待优化
            cnt = 0
            for elem in list_of_question_dict:
                if elem[1] not in rename_rule_list:
                    continue
                rename_rule.append(elem[0][-1])  # ! 待添加分隔符
                cnt += 1
                if cnt >= len(rename_rule_list):  # * 防止获取到文件后面的重命名规则
                    break
            # print(rename_rule)

            # * 生成文件存储路径，将文件存储路径放在用户所属的路径下，引入随机数（需使用 file_counter）
            # print(current_user.userpath)
            file_path = current_user.userpath + '/' + str(file_counter) + ''.join(
                random.sample(string.ascii_letters + string.digits, 8)
            )  # * 总长度为 20 + 1 + 1 + 8 = 30 位
            question = Question_info(collection_id=collection_id,
                                     qno=int(question_key[-1]),
                                     question_type=Question_info.FILE_UPLOAD,
                                     question_title=question_dict[question_key],
                                     question_description=question_dict['detail' + question_key[-1]],
                                     rename_rule='-'.join(rename_rule),  # * 命名规则用 - 分隔，数字代表题目序号
                                     file_path=file_path)
            db.session.add(question)
            db.session.commit()
            path = './FileStorage/' + question.file_path
            os.mkdir(path)  # 创建该题的文件存储目录


def update_status(user_id=None):
    """
    更新用户各个收集的状态

    Args:
        user_id: int类型，表示用户id。
    """
    if user_id is not None:
        collection_list = Collection_info.query.filter_by(creator_id=current_user.id).all()
        # ? 根据当前时间更新各个收集的状态
        for collection in collection_list:
            if collection.end_date <= datetime.now():
                new_status = Collection_info.FINISHED  # * 标记为已截止
            else:
                new_status = Collection_info.RELEASE  # * 标记为进行中
            Collection_info.query.filter_by(id=collection.id).update({'status': new_status})
        db.session.commit()


def count_submission(user_id=None, collection_id=None):
    """统计问卷提交数量

    Args:
        user_id（可选参数）: int类型，表示用户的id。
        collection_id（可选参数）: int类型，表示问卷的id。

    Return:
        若collection_id不为None， 则返回该问卷的提交数量，是一个整数。
        若collection_id为None，user_id不为None，则返回该用户创建的每一个问卷的提交数量，是一个字典，键为问卷id，值为该问卷的提交数量。
        若2个参数都为None，则返回None。
    """

    # 先看是否给了参数collection_id
    if collection_id is not None:
        return Submission_info.query.filter_by(collection_id=collection_id).count()

    # 若没给参数collection_id，但给了参数user_id
    if user_id is not None:
        collection_id_list = Collection_info.query.filter_by(creator_id=user_id).with_entities(Collection_info.id).all()
        submission_dict = {}
        for collection_id in collection_id_list:
            submission_dict[collection_id] = Submission_info.query.filter_by(collection_id=collection_id).count()
        return submission_dict

    return None


def count_filenum(user_id=None, collection_id=None, question_id=None, qno=None):
    """统计一个收集（collection_id）的第qno题的已收文件数

    Args:
        user_id（可选参数）: int类型，表示用户的id。
        collection_id（可选参数）: int类型，表示问卷的id。
        qno（可选参数）: int类型，表示题目序号。

    Return:
        若question_id不为None，或collection_id、qno不为None，则返回该题的已收文件数，是一个整数。
        若question_id为None，collection_id不为None，则返回该问卷的已收文件数，是一个整数。
        若question_id为None、collection_id为None，user_id不为None，则返回该用户所有问卷的已收文件数，是一个字典，键为问卷id，值为该问卷的已收文件数。
        若都为None，则返回None。
    """

    # 若给了参数question_id
    if question_id is not None:
        path = './FileStorage/' + Question_info.query.filter_by(id=question_id).first().file_path
        files = os.listdir(path)
        file_num = len(files)
        return file_num

    # 若给了collection_id和qno
    if collection_id is not None and qno is not None:
        path = './FileStorage/' + Question_info.query.filter_by(id=question_id).first().file_path
        files = os.listdir(path)
        file_num = len(files)
        return file_num

    # 若没给参数question_id，但给了参数collection_id
    if collection_id is not None:
        # 查询收集中所有文件上传题的id
        question_id_list = Question_info.query.filter_by(
            collection_id=collection_id, question_type=Question_info.FILE_UPLOAD
        ).with_entities(Question_info.id).all()
        file_num = 0
        # 遍历该收集中所有文件上传题，统计已收文件总数
        for q_id in question_id_list:
            path = './FileStorage/' + Question_info.query.filter_by(id=q_id).first().file_path
            files = os.listdir(path)
            file_num += len(files)
        return file_num

    # 若没给参数question_id、collection_id，但给了参数user_id
    if user_id is not None:
        collection_id_list = Collection_info.query.filter_by(creator_id=user_id).with_entities(Collection_info.id).all()
        file_num_dict = {}
        # 遍历该用户的所有收集
        for id1 in collection_id_list:
            # 查询收集中所有文件上传题
            question_id_list = Question_info.query.filter_by(
                collection_id=id1, question_type=Question_info.FILE_UPLOAD
            ).with_entities(Question_info.id).all()
            file_num = 0
            for id2 in question_id_list:
                path = './FileStorage/' + Question_info.query.filter_by(id=id2).first().file_path
                files = os.listdir(path)
                file_num += len(files)
            file_num_dict[id1] = file_num
        return file_num_dict

    return None


def deadline_countdown(collection_id: int):
    """
    截止倒计时
    Args:
        collection_id: int. 问卷的id

    Return:
        Datetime对象，表示截止倒计时。
    """
    current_time = datetime.now()  # 获取当前时间
    deadline = Collection_info.query.get(collection_id).end_date  # 查询问卷截止时间
    return deadline - current_time  # 返回倒计时


def delete_collection(collection_id=None):
    if collection_id != None:
        Submit_Content_info.query.filter_by(collection_id=collection_id).delete()
        Submission_info.query.filter_by(collection_id=collection_id).delete()
        Option_info.query.filter_by(collection_id=collection_id).delete()
        Answer_info.query.filter_by(collection_id=collection_id).delete()

        # 删除该收集中所有文件上传题的文件存储路径下的文件
        file_path = Question_info.query.filter_by(collection_id=collection_id,
                                                  question_type=Question_info.FILE_UPLOAD).with_entities(
            Question_info.file_path).all()
        for fp in file_path:
            path = './FileStorage/' + fp
            shutil.rmtree(path)

        Question_info.query.filter_by(collection_id=collection_id).delete()
        Collection_info.query.filter_by(collection_id=collection_id).delete()
        db.session.commit()
