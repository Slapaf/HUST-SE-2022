'''''
数据库接口函数：
    1、add_FC(question_list: list, user_id: int)
        Function: 添加文件收集（add FileCollection)
        
        Inputs:
        - question_list：问题信息列表
        - user_id：创建收集的用户id
        
        Returns: 
        - collection_id：添加的收集的id
        
    2、update_status(user_id: int)
        Function: 更新id为user_id的用户的所有收集的状态（进行中or已截止）
        
        Inputs:
        - user_id：用户id
        
        Returns: None
    
    3、count_submission(user_id=None, collection_id=None)
        Function: 统计提交数量
        
        Inputs:
        - user_id：int类型，表示用户id，缺省默认值为None
        - collection_id：int类型，表示收集id，缺省默认值为None
        
        Returns:
        - 若参数collection_id不为None，则返回一个int，表示id为collection_id的收集的已提交数量。
        - 若参数collection_id为None，参数user_id不为Non，则返回一个dict，表示id为user_id的用户创建的所有收集，及对应的提交数量。
        - 若参数都为None，返回None
        
        Example:
            /* 若只想统计1个收集的提交数量，则需给出参数collection_id的值 */
            >>> a=count_submission(collection_id=1)
            >>> a
            5
            
            /* 若想统计个用户创建的所有收集的提交数量，则需给出参数user_id的值 */
            /* 假设id为1的用户创建的收集的id集合为{1,2,3} */
            >>> a=count_submission(user_id=1)
            >>> a
            {1:5,2:6,3:5} # 表示id为1的收集已提交了5份…………

    4、count_filenum(user_id=None, collection_id=None, question_id=None, qno=None)
        Function: 统计已收文件数
        
        Inputs:
        - user_id：int类型，表示用户id，缺省默认值为None
        - collection_id：int类型，表示收集id，缺省默认值为None
        - question_id：int类型，表示问题id，缺省默认值为None
        - qno：int类型，表示问题序号，缺省默认值为None
        
        Returns:
        - 若参数question_id不为None，或collection_id、qno不为None，则返回一个int，表示该题的已收文件数。
        - 若参数question_id为None，collection_id不为None，则返回一个int，表示该问卷的已收文件数。
        - 若question_id为None、collection_id为None，user_id不为None，则返回一个dict，表示该用户创建的所有收集的id，及对应已收文件数。
        - 若都为None，则返回None。
        
        Example：
            /* 若只想统计1个问题的已收文件数，则需给出参数question_id的值，或参数collection_id和qno的值 */
            /* 假设id为3的问题是id为1的收集的第3题 */
            >>> a=count_filenum(question_id=3) 或 a=count_filenum(collection_id=1,qno=3)
            >>> a
            5
            
            /* 若想统计1个收集的已收文件数，则需给出参数collection_id的值 */
            >>> a=count_filenum(collection_id=1)
            >>> a
            5
            
            /* 若想统计1个用户创建的所有收集的已收文件数，则需给出参数user_id的值 */
            /* 假设id为1的用户创建的收集的id集合为{1,2,3} */
            >>> a=count_submission(user_id=1)
            >>> a
            {1:5,2:6,3:5}  # 表示id为1的收集已收文件数为5…………
            
    5、deadline_countdown(collection_id: int)
        Function: 计算一个收集的截止倒计时
        
        Inputs:
        - collection_id：int类型，表示收集id
        
        Returns:
        - 倒计时，timedelta类型
        
        Example:
            /* 假设id为1的收集截止时间为2022-11-3 1:11:0，当前时间为2022-11-1 0:0:0 */
            >>> delta=deadline_countdown(1)
            >>> delta
            2 days, 1:11:00
    
    6、delete_collection(collection_id=None)
        ！未测试正确性
        Function: 删除id为collection_id的收集在数据库中的相关数据（包括收集的文件）
        
        Inputs:
        - collection_id：int类型，表示收集id
        
        Returns: None
    
    7、get_question_MultiDict(collection_id: int)
        Function: 返回id为collection_id的收集的信息，包括收集标题、创建人、截止时间、收集描述、题目等信息
        
        Inputs:
        - collection_id：int类型，表示收集id
        
        Returns: 
        - question：defaultdict(<class 'list'>类型
        
        Example：
            /* 假设要得到id为1的收集的信息 */
            >>> a = get_question_MultiDict(1)
            >>> a  
            
    8、 modify_password(user_id: int, original_pswd: str, new_pswd: str)
        ！未验证正确性
        Function: 修改id为user_id的用户的密码
        
        Inputs:
        - user_id：int类型，表示用户id
        - original_pswd：string类型，表示原密码
        - new_pswd：string类型，表示新密码
        
        Returns: 
        一个整数，取值范围和含义如下：
        - 1：修改成功
        - 0：原密码错误
        - -1：user_id错误，即该用户不存在
    
    9、modify_personal_info(user_id: int, new_name: str, new_email: str)
        ！未验证正确性
        Function: 修改id为user_id的用户的个人信息（昵称、邮箱）
        
        Inputs:
        - user_id：int类型，表示用户id
        - new_name：string类型，表示新昵称
        - new_email：string类型，表示新邮箱
        
        Returns: 
        一个整数，取值范围和含义如下：
        - 1：修改成功
        - -1：user_id错误，即该用户不存在
    
    10、submission_record(collection_id: int)
        Function: 获取id为collection_id的收集的提交信息
        
        Inputs:
        - collection_id：int类型，表示收集id
        
        Returns: 
        一个元组列表，元组按Submission.id排序，每个元组格式为（姓名，提交时间，文件数量，文件详情）。
        例如：
        [('计胜翔', datetime.datetime(2022, 11, 5, 20, 25, 32, 142115), 2, ['jsx1.pdf', 'jsx2.doc']), 
        ('张隽翊', datetime.datetime(2022, 11, 5, 20, 25, 32, 142115), 1, ['zjy1.pdf'])]
        
    11、stop_collection(collection_id: int, action_list)
        Function: 将id为collection_id的收集的状态修改为“截止”
        
        Inputs:
        - collection_id：int类型，表示收集id
        - action_list：list类型，元素类型为string
        
        Returns: None
        
'''''

import string
from copy import deepcopy
import random
import os
from flask_login import current_user
from models import User, Collection_info, Question_info, Answer_info, Submit_Content_info, Option_info, Submission_info
from init import db
from datetime import datetime
from werkzeug.datastructures import MultiDict
import shutil
from collections import defaultdict
from operator import itemgetter
from sqlalchemy import func


def add_FC(question_list: list, user_id: int):
    """
    将问卷的信息存入数据库
    Args:
        question_list:题目信息列表
        例如：question_multidict = {'collectionTitle': '文件收集', 'collector': 'jsx', 'deadline': '2022-10-13T15:18',
                 'description': 'teset','question_name1': '姓名', 'question_file2': '文件', 'checked_topic2': '学号',
                 'question_file3': '文','checked_topic3': '学', 'question_sno4': '学', 'question_sno5': '学号',
                 'question_name6': '姓','question_radio7': '单选','checked_radio7': 'A', 'question_radio8': '单选题',
                 'checked_radio8': 'B'}
        user_id: int类型，表示用户的id。
    Return:None
    """
    # ! 文件类型可能有多个，设置一个计数器记录是第几个文件
    file_counter = 0  # * 文件计数器

    list_of_question_dict = deepcopy(question_list)  # ! 保存元组的列表，与字典类型的区别在于是否对 key 去重
    # print(list_of_question_dict)

    question_multidict = MultiDict(question_list)
    # 前端传来的deadLine为string类型，在此转化为datetime类型
    deadline = question_multidict['deadline']
    print(deadline)
    deadline = deadline.replace("T", " ")
    ddl_format = '%Y-%m-%d %H:%M:%S'
    question_multidict['deadline'] = datetime.strptime(deadline, ddl_format)

    # * 生成应交名单路径
    collection_counter = Collection_info.query.filter_by(creator_id=user_id).count()  # 获取当前用户创建的收集总数
    namelist_path = current_user.userpath + '/' + str(collection_counter) + ''.join(
        random.sample(string.ascii_letters + string.digits, 8)
    )  # * 总长度为 20 + 1 + 1 + 8 = 30 位

    # 创建一个文件收集对象,更新文件收集主表里
    collection = Collection_info(creator=question_multidict['collector'],
                                 creator_id=current_user.id,
                                 collection_title=question_multidict['collectionTitle'],
                                 description=question_multidict['description'],
                                 end_date=question_multidict['deadline'],
                                 namelist_path=namelist_path,
                                 status=Collection_info.SAVED)
    db.session.add(collection)
    db.session.commit()  # 提交数据库会话，否则 id 为None
    collection_id = collection.id

    key_list = list(question_multidict.keys())
    # 问题的键列表
    question_key_list = [question_key for question_key in key_list if "question" in question_key]

    # 更新问题主表和答案表
    for question_key in question_key_list:
        # ? 若为填空题
        if "sno" in question_key or "name" in question_key:
            question = Question_info(collection_id=collection_id,
                                     qno=int(question_key[-1]),
                                     question_type=Question_info.FILL_IN_BLANK,
                                     question_title=question_multidict[question_key],
                                     question_description=question_multidict['detail' + question_key[-1]])
            db.session.add(question)
            db.session.commit()

        # ? 若为单选题
        elif "radio" in question_key:
            question = Question_info(collection_id=collection_id,
                                     qno=int(question_key[-1]),
                                     question_type=Question_info.SINGLE_CHOICE,
                                     question_title=question_multidict[question_key],
                                     question_description=question_multidict['detail' + question_key[-1]])
            db.session.add(question)
            db.session.commit()
            # 存选择题答案
            answer = Answer_info(collection_id=collection_id,
                                 question_id=question.id,
                                 qno=int(question_key[-1]),
                                 answer_option=question_multidict['checked_radio' + question_key[-1]])
            db.session.add(answer)
            db.session.commit()

        # ? 若为多选题
        elif "multipleChoice" in question_key:
            question = Question_info(collection_id=collection_id,
                                     qno=int(question_key[-1]),
                                     question_type=Question_info.MULTI_CHOICE,
                                     question_title=question_multidict[question_key],
                                     question_description=question_multidict['detail' + question_key[-1]])
            db.session.add(question)
            db.session.commit()
            # 存选择题答案
            ano_list = question_multidict.getlist('checked_mulans' + question_key[-1])
            for ano in ano_list:
                answer = Answer_info(collection_id=collection_id,
                                     question_id=question.id,
                                     qno=int(question_key[-1]),
                                     answer_option=ano)
                db.session.add(answer)
            db.session.commit()

        # ? 若为问卷题
        elif "question_qnaire" in question_key:
            if question_multidict['choose_type' + question_key[-1]] == 'single':
                qn_type = Question_info.SINGLE_QUESTIONNAIRE
            else:
                qn_type = Question_info.MULTI_QUESTIONNAIRE
            question = Question_info(collection_id=collection_id,
                                     qno=int(question_key[-1]),
                                     question_type=qn_type,
                                     question_title=question_multidict[question_key],
                                     question_description=question_multidict['detail' + question_key[-1]])
            db.session.add(question)
            db.session.commit()
            # 存问卷题目各选项的内容
            option_content = question_multidict.getlist('qn_option' + question_key[-1])
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
                                     question_title=question_multidict[question_key],
                                     question_description=question_multidict['detail' + question_key[-1]],
                                     rename_rule='-'.join(rename_rule),  # * 命名规则用 - 分隔，数字代表题目序号
                                     file_path=file_path)
            db.session.add(question)
            db.session.commit()
            path = './FileStorage/' + question.file_path
            # print(path)
            os.mkdir(path)  # 创建该题的文件存储目录

    return collection_id


def update_status(user_id: int):
    """
    更新用户各个收集的状态

    Args:
        user_id: int类型，表示用户id。
    """
    collection_list = Collection_info.query.filter_by(creator_id=user_id).all()
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


def delete_collection(collection_id: int):
    Submit_Content_info.query.filter_by(collection_id=collection_id).delete()
    Submission_info.query.filter_by(collection_id=collection_id).delete()
    Option_info.query.filter_by(collection_id=collection_id).delete()
    Answer_info.query.filter_by(collection_id=collection_id).delete()

    # 删除该收集中所有文件上传题的文件存储路径下的文件
    file_path = Question_info.query. \
        filter_by(collection_id=collection_id, question_type=Question_info.FILE_UPLOAD). \
        with_entities(Question_info.file_path). \
        all()
    file_path = list(map(itemgetter(0), file_path))
    for fp in file_path:
        print(fp)
        path = './FileStorage/' + fp
        shutil.rmtree(path)

    Question_info.query.filter_by(collection_id=collection_id).delete()
    Collection_info.query.filter_by(id=collection_id).delete()
    db.session.commit()


def get_question_Dict(collection_id: int):
    seq = 0
    question = {}
    collection = Collection_info.query.get(collection_id)
    seq += 1
    question[f'{seq}_collectionTitle'] = collection.collection_title
    seq += 1
    question[f'{seq}_collector'] = collection.creator
    seq += 1
    question[f'{seq}_deadline'] = collection.end_date.strftime("%Y-%m-%d %H:%M")
    seq += 1
    question[f'{seq}_description'] = collection.description
    question_list = Question_info.query.filter_by(collection_id=collection_id).order_by("qno").all()
    print(question_list)
    for q in question_list:
        # 若是填空题
        if q.question_type == Question_info.FILL_IN_BLANK:
            seq += 1
            question[f'{seq}_question_fill{q.qno}'] = q.question_title
            seq += 1
            question[f'{seq}_detail{q.qno}'] = q.question_description

        # 若是文件上传题
        if q.question_type == Question_info.FILE_UPLOAD:
            seq += 1
            question[f'{seq}_question_file{q.qno}'] = q.question_title
            seq += 1
            question[f'{seq}_detail{q.qno}'] = q.question_description
            # 重命名规则
            qno_list = list(map(int, q.rename_rule.split('-')))
            for qno in qno_list:
                seq += 1
                question[f'{seq}_checked_topic{q.qno}'] = Question_info.query. \
                    filter_by(collection_id=collection_id, qno=qno).first().question_title

        # 若是单选题
        if q.question_type == Question_info.SINGLE_CHOICE:
            seq += 1
            question[f'{seq}_question_radio{q.qno}'] = q.question_title
            seq += 1
            question[f'{seq}_detail{q.qno}'] = q.question_description
            # 单选题答案
            seq += 1
            question[f'{seq}_checked_radio{q.qno}'] = Answer_info.query. \
                filter_by(question_id=q.id).first().answer_option

        # 若是多选题
        if q.question_type == Question_info.MULTI_CHOICE:
            seq += 1
            question[f'{seq}_question_multipleChoice{q.qno}'] = q.question_title
            seq += 1
            question[f'{seq}_detail{q.qno}'] = q.question_description
            # 多选题答案
            answer_list = Answer_info.query.filter_by(question_id=q.id).with_entities(Answer_info.answer_option).all()
            answer_list = list(map(itemgetter(0), answer_list))
            print(answer_list)
            for answer in answer_list:
                seq += 1
                question[f'{seq}_checked_mulans{q.qno}'] = answer

        # 若是问卷题
        if q.question_type == Question_info.SINGLE_QUESTIONNAIRE or \
                q.question_type == Question_info.MULTI_QUESTIONNAIRE:
            seq += 1
            question[f'{seq}_question_qnaire{q.qno}'] = q.question_title
            seq += 1
            question[f'{seq}_detail{q.qno}'] = q.question_description
            option_list = Option_info.query.filter_by(question_id=q.id).order_by("option_sn").all()
            for option in option_list:
                seq += 1
                question[f'{seq}_qn_option{q.qno}'] = option.option_content
            if q.question_type == Question_info.SINGLE_QUESTIONNAIRE:
                seq += 1
                question[f'{seq}_choose_type{q.qno}'] = "single"
            else:
                seq += 1
                question[f'{seq}_choose_type{q.qno}'] = "multiple"

    return question


def modify_password(user_id: int, original_pswd: str, new_pswd: str):
    user = User.query.filter_by(id=user_id).first()  # 在数据库中查询用户

    # 该用户id不存在
    if user is None:
        return -1

    # 验证原密码
    if not user.validate_password(original_pswd):
        return 0

    # 修改密码
    user.set_password(new_pswd)
    db.session.commit()
    return 1  # 修改成功


def modify_personal_info(user_id: int, new_name: str, new_email: str):
    user = User.query.filter_by(id=user_id).first()

    # 该用户id不存在
    if user is None:
        return -1

    # 修改个人信息
    user.name = new_name
    user.email = new_email
    db.session.commit()
    return 1  # 修改成功


def submission_record(collection_id: int):
    # 获取提交名单列表
    name_list = Submission_info.query. \
        filter_by(collection_id=collection_id). \
        order_by("id"). \
        with_entities(Submission_info.submitter_name). \
        all()
    name_list = list(map(itemgetter(0), name_list))

    # 获取提交时间列表
    time_list = Submission_info.query. \
        filter_by(collection_id=collection_id). \
        order_by("id"). \
        with_entities(Submission_info.submit_time). \
        all()
    time_list = list(map(itemgetter(0), time_list))

    # 获取提交信息id列表
    submission_id_list = Submission_info.query. \
        filter_by(collection_id=collection_id). \
        order_by("submit_time"). \
        with_entities(Submission_info.id). \
        all()
    submission_id_list = list(map(itemgetter(0), submission_id_list))

    # 获取文件上传题的问题id列表
    question_id_list = Question_info.query. \
        filter_by(collection_id=collection_id, question_type=Question_info.FILE_UPLOAD). \
        with_entities(Question_info.id).all()
    question_id_list = list(map(itemgetter(0), question_id_list))

    file_num_list = []
    for id in submission_id_list:
        num = Submit_Content_info.query. \
            filter(Submit_Content_info.submission_id == id,
                   Submit_Content_info.question_id.in_(question_id_list)).count()
        file_num_list.append(num)

    # 构建文件详情列表
    file_list = []
    for id in submission_id_list:
        file = Submit_Content_info.query.filter_by(Submission_id=id). \
            with_entities(Submit_Content_info.result). \
            all()
        file = list(map(itemgetter(0), file))
        file_list.append(file)

    return list(zip(name_list, time_list, file_num_list, file_list))


def stop_collection(collection_id: int, action_list):
    collection = Collection_info.query.filter_by(id=collection_id)
    collection.update({'status': Collection_info.FINISHED})  # 状态标记为已截止
    new_ddl = action_list[2]
    new_ddl = datetime.strptime(new_ddl, '%Y-%m-%d %H:%M:%S')
    collection.update({'end_date': new_ddl})
    db.session.commit()
