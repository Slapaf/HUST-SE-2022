'''''
数据库接口函数：
    1、add_FC(question_list: list, user_id: int)
        Function: 添加文件收集（add FileCollection)
        
        Inputs:
        - question_list：list类型，表示问题信息列表
        - user_id：int类型，表示创建收集的用户id
        
        Returns: 
        - collection_id：int类型，表示添加的收集的id
        
    2、update_status(user_id: int)
        Function: 更新id为user_id的用户的所有收集的状态（进行中or已截止）
        
        Inputs:
        - user_id：int类型，表示用户id
        
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
        Function: 删除id为collection_id的收集在数据库中的相关数据（包括收集的文件）
        
        Inputs:
        - collection_id：int类型，表示收集id
        
        Returns: None
    
    7、get_question_Dict(collection_id: int)
        Function: 返回id为collection_id的收集的信息，包括收集标题、创建人、截止时间、收集描述、题目等信息
        
        Inputs:
        - collection_id：int类型，表示收集id
        
        Returns: 
        - question：dict类型
        
        Example：
            /* 假设要得到id为1的收集的信息 */
            >>> a = get_question_dict(1)
            >>> a  
            
    8、modify_password(user_id: int, original_pswd: str, new_pswd: str)
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
    
    9、modify_personal_info(user_id: int, new_name: str, new_email: str, authorization_code: str)
        ！未验证正确性
        Function: 修改id为user_id的用户的个人信息（昵称、邮箱、邮箱授权码）
        
        Inputs:
        - user_id：int类型，表示用户id
        - new_name：string类型，表示新昵称
        - new_email：string类型，表示新邮箱
        - authorization_code: string类型，表示邮箱授权码
        
        Returns: 
        一个整数，取值范围和含义如下：
        - 1：修改成功
        - -1：user_id错误，即该用户不存在
    
    10、submission_record(collection_id: int)
        Function: 获取id为collection_id的收集的提交信息
        
        Inputs:
        - collection_id：int类型，表示收集id
        
        Returns: 
        一个元组列表，元组按Submission.id排序，每个元组格式为（姓名：string，提交时间:datetime，文件数量:int，文件详情:list）。
        例如：
        [('计胜翔', datetime.datetime(2022, 11, 5, 20, 25, 32, 142115), 2, ['jsx1.pdf', 'jsx2.doc']), 
        ('张隽翊', datetime.datetime(2022, 11, 5, 20, 25, 32, 142115), 1, ['zjy1.pdf'])]
    
    10、submission_record_v2(collection_id: int)
        Function: 获取id为collection_id的收集的提交信息
        
        Inputs:
        - collection_id：int类型，表示收集id
        
        Returns: 
        一个元组列表，元组按Submission.id排序，每个元组格式为（提交记录id: int, 姓名: string, 提交时间: datetime, 文件数量: int, 文件详情: list）
        例如：
        [(1, '计胜翔', datetime.datetime(2022, 11, 5, 20, 25, 32, 142115), 2, ['jsx1.pdf', 'jsx2.doc']),
         (2, '张隽翊', datetime.datetime(2022, 11, 5, 20, 25, 32, 142115), 1, ['zjy1.pdf'])]
        
    11、stop_collection(collection_id: int, action_list)
        Function: 将id为collection_id的收集的状态修改为“截止”
        
        Inputs:
        - collection_id：int类型，表示收集id
        - action_list：list类型，元素类型为string
        
        Returns: None
    
    12、save_submission(submission_list: list, collection_id: int, file)
        Function: 将用户填写收集的内容submission_list存储到数据库中
        
        Inputs:
        - submission_list：list类型，元素类型为元组。格式如下：
        sample = [('question_name1', '姓名lala'),
                  ('submit_name1', '计胜翔'),
                  ('question_file2', '文件haha'),
                  ('submit_file2', '二十大观看心得.docx'),
                  ('question_sno3', '学号xixi'),
                  ('submit_sno3', 'U202015362'),
                  ('question_radio4', '单选题nie'),
                  ('submit_checked_radio4', 'C'),
                  ('question_multipleChoice5', '多选题kk'),
                  ('submit_checked_mulans5', 'A'),
                  ('submit_checked_mulans5', 'B'),
                  ('question_qnaire6', '你喜欢跑步吗？'),
                  ('submit_checked_qnaire6', '1')]
        - collection_id：int类型，表示收集id
        - file：flask表单数据，python ImmutableMultiDict类，用于获取提交的文件名
        
        Returns: 
            若提交时间超时，则输出超时提示，并返回-1；
            若提交成功，则返回submission_id：int类型，表示该提交记录在表Submission_info中的id。
        
    13、modify_collection(collection_id: int, question_list: list)
        ！未测试正确性
        Function: 修改一个已创建的收集（只能修改收集标题、创建人、截止时间、收集描述和题目描述）
        
        Inputs:
        - collection_id：int类型，表示收集id
        - question_list：list类型，表示问题信息列表
        
        Returns: None
        
    14、file_upload(collection_id: int,question_list: list,file: werkzeug.datastructures.ImmutableMultiDict)
        Function: 将提交的文件存储到题目对应的路径中，
        
        Inputs:
        - collection_id: int类型，表示收集id
        - question_list: list类型，表示问题信息列表
        - file: 网页提交表单中的文件数据
        
        Returns: 
        - file: 经过重命名后的文件数据，以便调用save_submission函数时使用
    
    15、get_submission_dict(collection_id: int, submission_id: int) -> dict
        Function: 获取id为collection_id的收集、提交记录id为submission_id的用户提交内容信息

        Args:
            collection_id: 收集id
            submission_id: 提交记录id

        Returns:
            一个字典，包含该提交记录中用户的提交内容。
            例如：
            {'1_collectionTitle': '核酸检测',
             '2_collector': '张三',
             '3_deadline': '2022-11-15 15:23:09',
             '4_description': '',
             '5_question_name1': '姓名',
             '6_detail1': '',
             '7_submit_name1': '王广凯',
             '8_question_sno2': '学号',
             '9_detail2': '',
             '10_submit_sno2': 'U202012345',
             '11_question_file3': '文件',
             '12_detail3': '',
             '13_submit_file3': '系统设计.md',
             '14_question_radio4': '单选题',
             '15_detail4': '',
             '16_checked_radio4': 'A',
             '17_submit_radio4': 'B',
             '18_question_multipleChoice5': '多选题',
             '19_detail5': '',
             '20_checked_mulans5': 'C',
             '21_checked_mulans5': 'D',
             '22_submit_mulans5': 'A',
             '23_submit_mulans5': 'B',
             '24_question_qnaire6': '问卷题目',
             '25_detail6': '是否已做核酸',
             '26_qn_option6': '是',
             '27_qn_option6': '否',
             '28_submit_qnaire6': '2'}

    
    16、collection_data_statistics(collection_id: int) -> (dict, dict):
        Function: 对收集中的选择题、问卷题的答题情况进行数据统计

        Args:
        - collection_id: 收集id
    
        Returns: choice_statistics, qnaire_statistics
        - choice_statistics: 选择题答题情况数据统计。若收集中无选择题，则返回None；否则返回一个字典，格式如下:
        { 题目标题: (答案, 正确率, {选项: [选择此选项的人员名单]}) }
        例如：
        {'单选题': ('A', 0.2, {'A': ['张庙松'], 'B': ['王梓熙', '王广凯'], 'C': ['张隽翊'], 'D': ['计胜翔']}),
         '多选题': ('A-B-C-D', 0.2, {'A': ['王梓熙', '计胜翔', '张庙松'], 'B': ['王梓熙', '王广凯', '张庙松'],'C': ['王广凯', '张隽翊', '张庙松'], 'D': ['张隽翊', '计胜翔', '张庙松']})}

        - qnaire_statistics: 问卷题答题情况数据统计。若收集中无问卷题，则返回None；否则返回一个字典，格式如下:
        { 题目标题: {选项: [选择此选项的人员名单]} }
        例如：
        {'你是否喜欢吃屎？': {'喜欢': ['王梓熙', '王广凯', '张隽翊', '张庙松'], '不喜欢': ['计胜翔']}}


'''''

import string, random, os, shutil, re, werkzeug
from copy import deepcopy
from flask_login import current_user
from models import User, Collection_info, Question_info, Answer_info, Submit_Content_info, Option_info, Submission_info
from init import db, APP_ROOT
from datetime import datetime
from werkzeug.datastructures import MultiDict
from operator import itemgetter
from pathlib import Path


def id_int_to_str(id_int: int):
    """
    将 int 类型的 id 号转换为 str 类型

    Args:
        id_int(int): int 类型的 id 号

    Return:
        id_str(str): str 类型的 id 号
    """
    if 0 <= id_int <= 9:
        return str(id_int)
    id_int -= 10
    return chr(id_int + 97)


def add_FC(question_list: list, user_id: int) -> int:
    """
    将新创建的收集存入数据库，并为每个收集分配一个收集者用户目录下的子目录，总长度为 X 位，最后一位代表收集 id。

    Args:
        question_list: 题目信息列表
        user_id: 用户id

    Return:
        collection_id: 收集id
    """
    # ! 文件类型可能有多个，设置一个计数器记录是第几个文件
    file_counter = 0  # * 文件计数器

    list_of_question_dict = deepcopy(question_list)  # ! 保存元组的列表，与字典类型的区别在于是否对 key 去重
    question_multidict = MultiDict(question_list)

    # 前端传来的deadLine为string类型，在此转化为datetime类型
    deadline = question_multidict['deadline']
    # ! 解决 00 秒的问题
    if len(deadline) < 19:
        deadline += ':00'
    deadline = deadline.replace("T", " ")
    question_multidict['deadline'] = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')

    # * 生成应交名单路径
    # collection_counter = Collection_info.query.filter_by(creator_id=user_id).count()  # 获取当前用户创建的收集总数
    # namelist_path = current_user.userpath + '/' + str(collection_counter) + ''.join(
    #     random.sample(string.ascii_letters + string.digits, 8)
    # )  # * 总长度为 20 + 1 + 1 + 8 = 30 位

    # 创建一个文件收集对象,更新文件收集主表里
    collection = Collection_info(creator=question_multidict['collector'],
                                 creator_id=user_id,
                                 collection_title=question_multidict['collectionTitle'],
                                 description=question_multidict['description'],
                                 end_date=question_multidict['deadline'],
                                 # namelist_path=namelist_path,
                                 status=Collection_info.SAVED)
    db.session.add(collection)
    db.session.commit()  # 提交数据库会话，否则 id 为None
    collection_id = collection.id

    # ! 生成文件存储路径，最后一位固定为收集 id
    # ! 生成位置为：FileStorage / userpath / filepath
    # * 总长度为 20 + 5 + 4 = 29 位
    # file_path = current_user.userpath + '/file' + ''.join(
    #     random.sample(string.ascii_letters + string.digits, 4 - len(str(collection_id)))
    # ) + str(collection_id)
    file_path = os.path.join(
        current_user.userpath,
        'file' + ''.join(
            random.sample(string.ascii_letters + string.digits, 4 - len(str(collection_id)))
        ) + str(collection_id)
    )

    # ! 生成应交名单路径，与文件存储路径相同
    # ! 应交名单以 .csv 格式存放在 filepath 下
    # ! 生成位置为：FileStorage / userpath / filepath / xxx.csv
    # * 更新 Collection_info 的 namelist_path 属性
    collection = Collection_info.query.filter_by(id=collection_id)
    collection.update({'namelist_path': file_path})
    db.session.commit()

    key_list = list(question_multidict.keys())
    # 问题的键列表
    question_key_list = [question_key for question_key in key_list if "question" in question_key]
    seq = 0

    # 更新问题主表和答案表
    for question_key in question_key_list:
        seq += 1
        # ? 若为姓名题
        if "name" in question_key:
            question = Question_info(collection_id=collection_id,
                                     qno=seq,
                                     question_type=Question_info.NAME,
                                     question_title=question_multidict[question_key],
                                     question_description=question_multidict[f'detail{seq}'])
            db.session.add(question)
            db.session.commit()

        # ? 若为学号题
        if "sno" in question_key:
            question = Question_info(collection_id=collection_id,
                                     qno=seq,
                                     question_type=Question_info.SNO,
                                     question_title=question_multidict[question_key],
                                     question_description=question_multidict[f'detail{seq}'])
            db.session.add(question)
            db.session.commit()


        # ? 若为单选题
        elif "radio" in question_key:
            question = Question_info(collection_id=collection_id,
                                     qno=seq,
                                     question_type=Question_info.SINGLE_CHOICE,
                                     question_title=question_multidict[question_key],
                                     question_description=question_multidict[f'detail{seq}'])
            db.session.add(question)
            db.session.commit()
            # 存选择题答案
            answer = Answer_info(collection_id=collection_id,
                                 question_id=question.id,
                                 qno=seq,
                                 answer_option=question_multidict[f'checked_radio{seq}'])
            db.session.add(answer)
            db.session.commit()

        # ? 若为多选题
        elif "multipleChoice" in question_key:
            question = Question_info(collection_id=collection_id,
                                     qno=seq,
                                     question_type=Question_info.MULTI_CHOICE,
                                     question_title=question_multidict[question_key],
                                     question_description=question_multidict[f'detail{seq}'])
            db.session.add(question)
            db.session.commit()
            # 存选择题答案
            ano_list = question_multidict.getlist(f'checked_mulans{seq}')
            ano = '-'.join(ano_list)
            answer = Answer_info(collection_id=collection_id,
                                 question_id=question.id,
                                 qno=seq,
                                 answer_option=ano)
            db.session.add(answer)
            db.session.commit()

        # ? 若为问卷题
        elif "question_qnaire" in question_key:
            if question_multidict[f'choose_type{seq}'] == 'single':
                qn_type = Question_info.SINGLE_QUESTIONNAIRE
            else:
                qn_type = Question_info.MULTI_QUESTIONNAIRE
            question = Question_info(collection_id=collection_id,
                                     qno=seq,
                                     question_type=qn_type,
                                     question_title=question_multidict[question_key],
                                     question_description=question_multidict[f'detail{seq}'])
            db.session.add(question)
            db.session.commit()
            # 存问卷题目各选项的内容
            option_content = question_multidict.getlist(f'qn_option{seq}')
            for i in range(len(option_content)):
                option = Option_info(collection_id=collection_id,
                                     question_id=question.id,
                                     qno=seq,
                                     option_sn=i,
                                     option_content=option_content[i])
                db.session.add(option)
            db.session.commit()

        # ? 若为文件上传题
        elif "file" in question_key:
            # 确定文件重命名规则
            file_counter += 1
            rename_rule = []
            rename_rule_list = []  # * 重命名所需的题目
            question_num = str(seq)
            for elem in list_of_question_dict:
                if elem[0] == "checked_topic" + question_num:
                    rename_rule_list.append(elem[1])

            # TODO 逻辑有待优化
            cnt = 0
            for elem in list_of_question_dict:
                if elem[1] not in rename_rule_list:
                    continue
                rename_rule.append(re.findall(r"\d+", elem[0])[0])  # ! 待添加分隔符
                cnt += 1
                if cnt >= len(rename_rule_list):  # * 防止获取到文件后面的重命名规则
                    break

            rename_rule = '-'.join(rename_rule)
            if rename_rule == '':
                rename_rule = None

            question = Question_info(
                collection_id=collection_id,
                qno=seq,
                question_type=Question_info.FILE_UPLOAD,
                question_title=question_multidict[question_key],
                question_description=question_multidict[f'detail{seq}'],
                rename_rule=rename_rule,  # * 命名规则用 - 分隔，数字代表题目序号
                # file_path=file_path + "/" + id_int_to_str(
                #     file_counter
                # )  # ! 创建一个以 file_counter 命名的子目录
                file_path=os.path.join(file_path, id_int_to_str(file_counter))  # ! 创建一个以 file_counter 命名的子目录
            )
            db.session.add(question)
            db.session.commit()
            # path = './FileStorage/' + question.file_path
            path = os.path.join(APP_ROOT, 'FileStorage', question.file_path)
            print(path)  # ! 调试
            try:
                os.makedirs(path)  # 创建该题的文件存储目录
            except OSError:
                print("文件存储路径错误！")

    return collection_id


def update_status(user_id: int) -> None:
    """
    更新用户各个收集的状态

    Args:
        user_id: 用户id。
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


def count_submission(collection_id: int = None) -> int:
    """统计一个收集的提交数量

    Args:
        collection_id: 收集id

    Returns:
        若collection_id不为None， 则返回该问卷的提交数量，是一个整数;
        # 若collection_id为None，user_id不为None，则返回该用户创建的每一个问卷的提交数量，是一个字典，键为问卷id，值为该问卷的提交数量;
        # 若2个参数都为None，则返回None。
    """

    # 先看是否给了参数collection_id
    if collection_id is not None:
        return Submission_info.query.filter_by(collection_id=collection_id).count()

    # # 若没给参数collection_id，但给了参数user_id
    # if user_id is not None:
    #     collection_id_list = Collection_info.query.filter_by(creator_id=user_id).with_entities(Collection_info.id).all()
    #     collection_id_list = list(map(itemgetter(0), collection_id_list))
    #     submission_dict = {}
    #     for collection_id in collection_id_list:
    #         submission_dict[collection_id] = Submission_info.query.filter_by(collection_id=collection_id).count()
    #     return submission_dict

    return None


def count_filenum(collection_id: int = None) -> int:
    """统计一个收集的已收文件数

    Args:
        collection_id: 收集id

    Return:
        若collection_id不为None，则返回该问卷的已收文件数，是一个整数。
        # 若question_id不为None，或collection_id、qno不为None，则返回该题的已收文件数，是一个整数。
        # 若question_id为None，
        # 若question_id为None、collection_id为None，user_id不为None，则返回该用户所有问卷的已收文件数，是一个字典，键为问卷id，值为该问卷的已收文件数。
        # 若都为None，则返回None。
    """

    # # 若给了参数question_id
    # if question_id is not None:
    #     # path = './FileStorage/' + Question_info.query.filter_by(id=question_id).first().file_path
    #     path = os.path.join(APP_ROOT, 'FileStorage', Question_info.query.filter_by(id=question_id).first().file_path)
    #     files = os.listdir(path)
    #     file_num = len(files)
    #     return file_num

    # # 若给了collection_id和qno
    # if collection_id is not None and qno is not None:
    #     # path = './FileStorage/' + Question_info.query.filter_by(id=question_id).first().file_path
    #     path = os.path.join(APP_ROOT, 'FileStorage', Question_info.query.filter_by(id=question_id).first().file_path)
    #     files = os.listdir(path)
    #     file_num = len(files)
    #     return file_num

    # 若没给参数question_id，但给了参数collection_id
    if collection_id is not None:
        # 查询收集中所有文件上传题的id
        question_id_list = Question_info.query.filter_by(
            collection_id=collection_id, question_type=Question_info.FILE_UPLOAD
        ).with_entities(Question_info.id).all()
        question_id_list = list(map(itemgetter(0), question_id_list))
        file_num = 0
        # 遍历该收集中所有文件上传题，统计已收文件总数
        for q_id in question_id_list:
            # path = './FileStorage/' + Question_info.query.filter_by(id=q_id).first().file_path
            path = os.path.join(APP_ROOT, 'FileStorage', Question_info.query.filter_by(id=q_id).first().file_path)
            files = os.listdir(path)
            file_num += len(files)
        return file_num

    # # 若没给参数question_id、collection_id，但给了参数user_id
    # if user_id is not None:
    #     collection_id_list = Collection_info.query.filter_by(creator_id=user_id).with_entities(Collection_info.id).all()
    #     collection_id_list = list(map(itemgetter(0), collection_id_list))
    #     file_num_dict = {}
    #     # 遍历该用户的所有收集
    #     for id1 in collection_id_list:
    #         # 查询收集中所有文件上传题
    #         question_id_list = Question_info.query.filter_by(
    #             collection_id=id1, question_type=Question_info.FILE_UPLOAD
    #         ).with_entities(Question_info.id).all()
    #         question_id_list = list(map(itemgetter(0), question_id_list))
    #         file_num = 0
    #         for id2 in question_id_list:
    #             # path = './FileStorage/' + Question_info.query.filter_by(id=id2).first().file_path
    #             path = os.path.join(APP_ROOT, 'FileStorage', Question_info.query.filter_by(id=id2).first().file_path)
    #             files = os.listdir(path)
    #             file_num += len(files)
    #         file_num_dict[id1] = file_num
    #     return file_num_dict

    return None


def deadline_countdown(collection_id: int):
    """ 截止倒计时

    Args:
        collection_id: 收集id

    Return:
        Datetime对象，表示截止倒计时。
    """
    current_time = datetime.now()  # 获取当前时间
    deadline = Collection_info.query.get(collection_id).end_date  # 查询问卷截止时间
    return deadline - current_time  # 返回倒计时


def delete_collection(collection_id: int) -> None:
    """删除id为collection_id的收集在数据库中的所有相关信息

    Args:
        collection_id: 收集id

    """
    Submit_Content_info.query.filter_by(collection_id=collection_id).delete()
    Submission_info.query.filter_by(collection_id=collection_id).delete()
    Option_info.query.filter_by(collection_id=collection_id).delete()
    Answer_info.query.filter_by(collection_id=collection_id).delete()

    # 删除该收集中所有文件上传题的文件存储路径下的文件
    question = Question_info.query. \
        filter_by(collection_id=collection_id, question_type=Question_info.FILE_UPLOAD).first()
    # file_path = Path('./FileStorage/' + question.file_path).parent
    file_path = Path(os.path.join(APP_ROOT, 'FileStorage', question.file_path)).parent
    shutil.rmtree(file_path)

    Question_info.query.filter_by(collection_id=collection_id).delete()
    Collection_info.query.filter_by(id=collection_id).delete()
    db.session.commit()


def get_question_dict(collection_id: int) -> dict:
    """获取id为collection_id的收集的相关信息

    Args:
        collection_id: 收集id

    Returns:
        一个字典，包含该收集的相关信息（收集标题、收集描述、创建者、截止时间、题目等等）。
        格式如下：
        [('collectionTitle', 'ceshi'),
         ('collector', '凯'),
         ('deadline', '2022-11-18T22:31:49'),
         ('description', ''),
         ('question_name1', '姓名'),
         ('detail1', ''),
         ('question_sno2', '学号'),
         ('detail2', ''),
         ('question_file3', '文件'),
         ('detail3', ''),
         ('question_radio4', '单选题'),
         ('detail4', ''),
         ('checked_radio4', 'A'),
         ('question_multipleChoice5', '多选题'),
         ('detail5', ''),
         ('checked_mulans5', 'B'),
         ('checked_mulans5', 'C'),
         ('question_qnaire6', '问卷题目'),
         ('detail6', ''),
         ('qn_option6', 'asdf'),
         ('qn_option6', 'adff'),
         ('choose_type6', 'single')]
    """
    seq = 0
    question = {}
    collection = Collection_info.query.get(collection_id)
    if collection is None:
        return None
    seq += 1
    question[f'{seq}_collectionTitle'] = collection.collection_title
    seq += 1
    question[f'{seq}_collector'] = collection.creator
    seq += 1
    question[f'{seq}_deadline'] = collection.end_date.strftime("%Y-%m-%d %H:%M:%S")
    seq += 1
    question[f'{seq}_description'] = collection.description
    question_list = Question_info.query.filter_by(collection_id=collection_id).order_by("qno").all()
    for q in question_list:
        # 若是姓名题
        if q.question_type == Question_info.NAME:
            seq += 1
            question[f'{seq}_question_name{q.qno}'] = q.question_title
            seq += 1
            question[f'{seq}_detail{q.qno}'] = q.question_description

        # 若是姓名题
        if q.question_type == Question_info.SNO:
            seq += 1
            question[f'{seq}_question_sno{q.qno}'] = q.question_title
            seq += 1
            question[f'{seq}_detail{q.qno}'] = q.question_description

        # 若是文件上传题
        if q.question_type == Question_info.FILE_UPLOAD:
            seq += 1
            question[f'{seq}_question_file{q.qno}'] = q.question_title
            seq += 1
            question[f'{seq}_detail{q.qno}'] = q.question_description
            # 重命名规则
            if q.rename_rule is None:
                seq += 1
                question[f'{seq}_checked_topic{q.qno}'] = ''
            else:
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
            answer_list = Answer_info.query.filter_by(question_id=q.id).first().answer_option.split('-')
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


def modify_password(user_id: int, original_pswd: str, new_pswd: str) -> int:
    """修改密码

    Args:
        user_id: 用户id
        original_pswd: 原始密码
        new_pswd: 新密码

    Returns:
        若为-1，则用户id不存在；若为0，则原密码错误；若为1，则修改成功。

    """
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


def modify_personal_info(user_id: int, new_name: str, new_email: str, authorization_code: str) -> int:
    """修改个人信息（昵称、邮箱、邮箱授权码）

    Args:
        user_id: 用户id
        new_name: 新昵称
        new_email: 新邮箱
        authorization_code: 邮箱授权码

    Returns:
        若为-1，则用户id不存在；若为1，则修改成功。

    """
    user = User.query.filter_by(id=user_id).first()

    # 该用户id不存在
    if user is None:
        return -1

    # 修改个人信息
    user.name = new_name
    user.email = new_email
    user.authorization_code = authorization_code
    db.session.commit()
    return 1  # 修改成功


def submission_record(collection_id: int) -> list:
    """获取id为collection_id的收集的提交记录（姓名，提交时间，文件数量，文件详情）

    Args:
        collection_id: 收集id

    Returns:
        一个元组列表，每个元组表示一条提交信息。
        For example:
        [('计胜翔', datetime.datetime(2022, 11, 5, 20, 25, 32, 142115), 2, ['jsx1.pdf', 'jsx2.doc']),
        ('张隽翊', datetime.datetime(2022, 11, 5, 20, 25, 32, 142115), 1, ['zjy1.pdf'])]
    """
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
        order_by('id'). \
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
        file = Submit_Content_info.query.filter(Submit_Content_info.submission_id == id,
                                                Submit_Content_info.question_id.in_(question_id_list)). \
            with_entities(Submit_Content_info.result). \
            all()
        file = list(map(itemgetter(0), file))
        file_list.append(file)

    record = list(zip(name_list, time_list, file_num_list, file_list))
    # 对元组列表根据submit_time进行降序排序
    record = list(reversed(sorted(record, key=lambda x: (x[1].timestamp(), x[0]))))
    return record


def submission_record_v2(collection_id: int) -> list:
    """获取id为collection_id的收集的提交记录（姓名，提交时间，文件数量，文件详情）

    Args:
        collection_id: 收集id

    Returns:
        一个元组列表，每个元组表示一条提交信息，元组按Submission.id排序。
        每个元组格式为（提交记录id: int, 姓名: string, 提交时间: datetime, 文件数量: int, 文件详情: list）
        例如:
        [(1, '计胜翔', datetime.datetime(2022, 11, 5, 20, 25, 32, 142115), 2, ['jsx1.pdf', 'jsx2.doc']),
        (2, '张隽翊', datetime.datetime(2022, 11, 5, 20, 25, 32, 142115), 1, ['zjy1.pdf'])]
    """
    # 获取提交记录id
    id_list = Submission_info.query. \
        filter_by(collection_id=collection_id). \
        order_by("id"). \
        with_entities(Submission_info.id). \
        all()
    id_list = list(map(itemgetter(0), id_list))

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
        order_by('id'). \
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
        file = Submit_Content_info.query.filter(Submit_Content_info.submission_id == id,
                                                Submit_Content_info.question_id.in_(question_id_list)). \
            with_entities(Submit_Content_info.result). \
            all()
        file = list(map(itemgetter(0), file))
        file_list.append(file)

    record = list(zip(id_list, name_list, time_list, file_num_list, file_list))
    # 对元组列表根据submit_time进行降序排序
    record = list(reversed(sorted(record, key=lambda x: (x[2].timestamp(), x[0]))))
    return record


def stop_collection(collection_id: int, action_list) -> None:
    """停止收集

    Args:
        collection_id: 收集id
        action_list:
    """
    collection = Collection_info.query.filter_by(id=collection_id)
    collection.update({'status': Collection_info.FINISHED})  # 状态标记为已截止
    new_ddl = action_list[2]
    new_ddl = datetime.strptime(new_ddl, '%Y-%m-%d %H:%M:%S')
    collection.update({'end_date': new_ddl})
    db.session.commit()


def save_submission(submission_list: list, collection_id: int, file: werkzeug.datastructures.ImmutableMultiDict) -> int:
    """保存收集提交内容

    Args:
        submission_list: 提交信息列表
        collection_id: 收集id
        file: 网页提交表单中的文件数据

    Returns:
        若提交时间超过收集截止时间，则返回-1；
        若未超时，则返回提交记录id。
    """
    submission_multidict = MultiDict(submission_list)
    key_list = list(submission_multidict.keys())  # 提取问题的键值列表
    name_key_list = list(filter(lambda x: x.find("name") >= 0, key_list))
    if len(name_key_list) != 0:
        name_key = name_key_list[0]
        qno = re.findall(r"\d+", name_key)[0]
        # 创建一个提交记录，并加入数据库
        submission = Submission_info(collection_id=collection_id,
                                     submitter_name=submission_multidict['submit_name' + qno],
                                     submit_time=datetime.now())
    else:
        submission = Submission_info(collection_id=collection_id,
                                     submitter_name='',
                                     submit_time=datetime.now())

    # ! 判断提交时间是否超过截止时间
    deadline = Collection_info.query.get(collection_id).end_date
    diff = (submission.submit_time - deadline).total_seconds()
    if diff > 0:
        print('提交时间超时！')
        return -1

    # 若未超时
    submission.collection_title = Collection_info.query.get(collection_id).collection_title
    db.session.add(submission)
    db.session.commit()
    submission_id = submission.id  # 获得该提交记录的id

    key_list = [key for key in key_list if "question" in key]
    seq = 0
    for key in key_list:
        seq += 1
        submit_content = Submit_Content_info(submission_id=submission_id,
                                             collection_id=collection_id,
                                             qno=seq)
        question_id = Question_info.query.filter_by(collection_id=collection_id, qno=seq).first().id
        submit_content.question_id = question_id

        # 若为姓名题
        if "name" in key:
            submit_content.result = submission_multidict[f'submit_name{seq}']

        # 若为学号题
        elif "sno" in key:
            submit_content.result = submission_multidict[f'submit_sno{seq}']

        # 若为文件上传题
        elif "file" in key:
            filename = file.get(f'submit_file{seq}').filename
            submit_content.result = filename

        # 若为单选题
        elif "radio" in key:
            submit_content.result = submission_multidict[f'submit_checked_radio{seq}']

        # 若为多选题
        elif "multipleChoice" in key:
            result = submission_multidict.getlist(f"submit_checked_mulans{seq}")
            result = '-'.join(result)
            submit_content.result = result

        elif "qnaire" in key:
            result = submission_multidict.getlist(f"submit_checked_qnaire{seq}")
            result = '-'.join(result)
            submit_content.result = result

        db.session.add(submit_content)

    db.session.commit()
    return submission_id


def modify_collection(collection_id: int, question_list: list) -> None:
    """修改已创建的收集

    Args:
        collection_id: 收集id
        question_list: 问题信息列表
    """
    question_multidict = MultiDict(question_list)

    # 前端传来的deadLine为string类型，在此转化为datetime类型
    deadline = question_multidict['deadline']
    # ! 解决 00 秒的问题
    if len(deadline) < 19:
        deadline += ':00'
    deadline = deadline.replace("T", " ")
    question_multidict['deadline'] = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')

    # 更新Collection_info表中的信息
    collection = Collection_info.query.filter_by(id=collection_id)
    collection.update({'start_date': datetime.now(),
                       'collection_title': question_multidict['collectionTitle'],
                       'creator': question_multidict['collector'],
                       'description': question_multidict['description'],
                       'end_date': question_multidict['deadline']})
    db.session.commit()

    # 问题的键列表
    key_list = list(question_multidict.keys())
    question_key_list = [question_key for question_key in key_list if "question" in question_key]
    seq = 0
    for question_key in question_key_list:
        seq += 1
        question = Question_info.query.filter_by(collection_id=collection_id, qno=seq)

        if 'name' in question_key:
            question.update({'question_title': question_multidict[f'question_name{seq}'],
                             'question_description': question_multidict[f'detail{seq}']})

        elif 'sno' in question_key:
            question.update({'question_title': question_multidict[f'question_sno{seq}'],
                             'question_description': question_multidict[f'detail{seq}']})

        elif 'file' in question_key:
            # 确定文件重命名规则
            rename_rule = []
            rename_rule_list = []  # * 重命名所需的题目
            question_num = str(seq)
            for elem in question_list:
                if elem[0] == "checked_topic" + question_num:
                    rename_rule_list.append(elem[1])
            cnt = 0
            for elem in question_list:
                if elem[1] not in rename_rule_list:
                    continue
                rename_rule.append(re.findall(r"\d+", elem[0])[0])  # ! 待添加分隔符
                cnt += 1
                if cnt >= len(rename_rule_list):  # * 防止获取到文件后面的重命名规则
                    break

            rename_rule = '-'.join(rename_rule)
            if rename_rule == '':
                rename_rule = None

            question.update({'question_title': question_multidict[f'question_file{seq}'],
                             'question_description': question_multidict[f'detail{seq}'],
                             'rename_rule': rename_rule})

        elif 'radio' in question_key:
            question.update({'question_title': question_multidict[f'question_radio{seq}'],
                             'question_description': question_multidict[f'detail{seq}']})
            # 更新答案
            answer = Answer_info.query.filter_by(collection_id=collection_id, qno=seq)
            answer.update({'answer_option': question_multidict[f'checked_radio{seq}']})

        elif 'multipleChoice' in question_key:
            question.update({'question_title': question_multidict[f'question_multipleChoice{seq}'],
                             'question_description': question_multidict[f'detail{seq}']})

            # 更新答案
            ano_list = question_multidict.getlist(f'checked_mulans{seq}')
            ano = '-'.join(ano_list)
            answer = Answer_info.query.filter_by(collection_id=collection_id, qno=seq)
            answer.update({'answer_option': ano})

        elif 'qnaire' in question_key:
            question.update({'question_title': question_multidict[f'question_qnaire{seq}'],
                             'question_description': question_multidict[f'detail{seq}']})

            if question_multidict[f'choose_type{seq}'] == 'single':
                question.update({'question_type': Question_info.SINGLE_QUESTIONNAIRE})
            else:
                question.update({'question_type': Question_info.MULTI_QUESTIONNAIRE})

            # 先删除原来的选项内容，在创建新的
            Option_info.query.filter_by(question_id=question.first().id).delete()

            # 更新选项
            option_content = question_multidict.getlist(f'qn_option{seq}')
            for index, value in enumerate(option_content):
                option = Option_info(collection_id=collection_id,
                                     question_id=question.first().id,
                                     qno=seq,
                                     option_sn=index,
                                     option_content=value)
                db.session.add(option)

        db.session.commit()


def file_upload(collection_id: int,
                question_list: list,
                file: werkzeug.datastructures.ImmutableMultiDict) -> werkzeug.datastructures.ImmutableMultiDict:
    """将提交的文件重命名后，存储到题目相应的路径中

    Args:
        collection_id: 收集id
        question_list: 问题信息列表
        file: 网页提交表单中的文件数据

    Returns:
        返回重命名后的表单中的文件数据，以便调用save_submission函数时使用
    """
    question_multidict = MultiDict(question_list)
    key_list = list(question_multidict.keys())
    file_key_list = list(filter(lambda x: 'file' in x, key_list))
    submit_key_list = list(filter(lambda x: 'submit' in x, key_list))
    for file_key in file_key_list:
        qno_str = re.findall(r"\d+", file_key)[0]
        question = Question_info.query.filter_by(collection_id=collection_id, qno=int(qno_str)).first()
        f = file['submit_file' + qno_str]

        # 确定文件存储路径
        # path = './FileStorage/' + question.file_path
        path = os.path.join(APP_ROOT, 'FileStorage', question.file_path)

        # 重命名文件
        rename_rule = question.rename_rule
        if rename_rule is not None:  # 若重命名规则不为空
            filename_list = f.filename.split('.')  # 将文件名分为名称和后缀两部分，便于后面修改名称
            new_filename = ''
            rename_qno_list = rename_rule.split('-')  # 重命名依赖的题目序号列表
            for index, qno in enumerate(rename_qno_list):
                key = list(filter(lambda x: qno in x, submit_key_list))[0]
                new_filename += question_multidict[key]
                if index != len(rename_qno_list) - 1:
                    new_filename += '_'
            filename_list[0] = new_filename
            f.filename = '.'.join(filename_list)  # 修改文件名

        # print("重命名后文件名为：", f.filename)
        # 保存文件到指定路径
        f.save(os.path.join(path, f.filename))

    return file


def get_submission_dict(collection_id: int, submission_id: int) -> dict:
    """获取id为collection_id的收集、提交记录id为submission_id的用户提交内容信息

    Args:
        collection_id: 收集id
        submission_id: 提交记录id

    Returns:
        一个字典，包含该提交记录中用户的提交内容。
        格式如下：
        {'1_collectionTitle': '核酸检测',
         '2_collector': '张三',
         '3_deadline': '2022-11-15 15:23:09',
         '4_description': '',
         '5_question_name1': '姓名',
         '6_detail1': '',
         '7_submit_name1': '王广凯',
         '8_question_sno2': '学号',
         '9_detail2': '',
         '10_submit_sno2': 'U202012345',
         '11_question_file3': '文件',
         '12_detail3': '',
         '13_submit_file3': '系统设计.md',
         '14_question_radio4': '单选题',
         '15_detail4': '',
         '16_checked_radio4': 'A',
         '17_submit_radio4': 'B',
         '18_question_multipleChoice5': '多选题',
         '19_detail5': '',
         '20_checked_mulans5': 'C',
         '21_checked_mulans5': 'D',
         '22_submit_mulans5': 'A',
         '23_submit_mulans5': 'B',
         '24_question_qnaire6': '问卷题目',
         '25_detail6': '是否已做核酸',
         '26_qn_option6': '是',
         '27_qn_option6': '否',
         '28_submit_qnaire6': '2'}
    """
    seq = 0
    submission = {}
    collection = Collection_info.query.get(collection_id)
    if collection is None:
        return None
    seq += 1
    submission[f'{seq}_collectionTitle'] = collection.collection_title
    seq += 1
    submission[f'{seq}_collector'] = collection.creator
    seq += 1
    submission[f'{seq}_deadline'] = collection.end_date.strftime("%Y-%m-%d %H:%M:%S")
    seq += 1
    submission[f'{seq}_description'] = collection.description
    question_list = Question_info.query.filter_by(collection_id=collection_id).order_by("qno").all()
    submission_content_list = Submit_Content_info.query.filter_by(submission_id=submission_id).order_by("qno").all()
    for q, s in list(zip(question_list, submission_content_list)):
        # 若是姓名题
        if q.question_type == Question_info.NAME:
            seq += 1
            submission[f'{seq}_question_name{q.qno}'] = q.question_title
            seq += 1
            submission[f'{seq}_detail{q.qno}'] = q.question_description
            seq += 1
            submission[f'{seq}_submit_name{q.qno}'] = s.result

        # 若是姓名题
        if q.question_type == Question_info.SNO:
            seq += 1
            submission[f'{seq}_question_sno{q.qno}'] = q.question_title
            seq += 1
            submission[f'{seq}_detail{q.qno}'] = q.question_description
            seq += 1
            submission[f'{seq}_submit_sno{q.qno}'] = s.result

        # 若是文件上传题
        if q.question_type == Question_info.FILE_UPLOAD:
            seq += 1
            submission[f'{seq}_question_file{q.qno}'] = q.question_title
            seq += 1
            submission[f'{seq}_detail{q.qno}'] = q.question_description
            # # 重命名规则
            # if q.rename_rule is None:
            #     seq += 1
            #     submission[f'{seq}_checked_topic{q.qno}'] = ''
            # else:
            #     qno_list = list(map(int, q.rename_rule.split('-')))
            #     for qno in qno_list:
            #         seq += 1
            #         submission[f'{seq}_checked_topic{q.qno}'] = Question_info.query. \
            #             filter_by(collection_id=collection_id, qno=qno).first().question_title
            seq += 1
            submission[f'{seq}_submit_file{q.qno}'] = s.result

        # 若是单选题
        if q.question_type == Question_info.SINGLE_CHOICE:
            seq += 1
            submission[f'{seq}_question_radio{q.qno}'] = q.question_title
            seq += 1
            submission[f'{seq}_detail{q.qno}'] = q.question_description
            # 单选题答案
            seq += 1
            submission[f'{seq}_checked_radio{q.qno}'] = Answer_info.query. \
                filter_by(question_id=q.id).first().answer_option
            # 用户提交答案
            seq += 1
            submission[f'{seq}_submit_radio{q.qno}'] = s.result

        # 若是多选题
        if q.question_type == Question_info.MULTI_CHOICE:
            seq += 1
            submission[f'{seq}_question_multipleChoice{q.qno}'] = q.question_title
            seq += 1
            submission[f'{seq}_detail{q.qno}'] = q.question_description
            # 多选题答案
            answer_list = Answer_info.query.filter_by(question_id=q.id).first().answer_option.split('-')
            for answer in answer_list:
                seq += 1
                submission[f'{seq}_checked_mulans{q.qno}'] = answer
            # 用户提交答案
            submit_option_list = s.result.split('-')
            for submit_option in submit_option_list:
                seq += 1
                submission[f'{seq}_submit_mulans{q.qno}'] = submit_option

        # 若是问卷题
        if q.question_type == Question_info.SINGLE_QUESTIONNAIRE or \
                q.question_type == Question_info.MULTI_QUESTIONNAIRE:
            seq += 1
            submission[f'{seq}_question_qnaire{q.qno}'] = q.question_title
            seq += 1
            submission[f'{seq}_detail{q.qno}'] = q.question_description
            # 选项内容
            option_list = Option_info.query.filter_by(question_id=q.id).order_by("option_sn").all()
            for option in option_list:
                seq += 1
                submission[f'{seq}_qn_option{q.qno}'] = option.option_content
            # if q.question_type == Question_info.SINGLE_QUESTIONNAIRE:
            #     seq += 1
            #     submission[f'{seq}_choose_type{q.qno}'] = "single"
            # else:
            #     seq += 1
            #     submission[f'{seq}_choose_type{q.qno}'] = "multiple"

            # 用户提交选项
            submit_option_list = s.result.split('-')
            for submit_option in submit_option_list:
                seq += 1
                submission[f'{seq}_submit_qnaire{q.qno}'] = submit_option

    print(submission)
    return submission


def collection_data_statistics(collection_id: int) -> (dict, dict):
    """对收集中的选择题、问卷题的答题情况进行数据统计

    Args:
        collection_id: 收集id

    Returns:
        choice_statistics: 选择题答题情况数据统计。若收集中无选择题，则返回None；否则返回一个字典，格式如下:
        { 题目标题: (答案, 正确率, {选项: [选择此选项的人员名单]}) }
        例如：
{'单选题': ('A', 0.2, {'A': ['张庙松'], 'B': ['王梓熙', '王广凯'], 'C': ['张隽翊'], 'D': ['计胜翔']}),
 '多选题': ('A-B-C-D', 0.2, {'A': ['王梓熙', '计胜翔', '张庙松'], 'B': ['王梓熙', '王广凯', '张庙松'],'C': ['王广凯', '张隽翊', '张庙松'], 'D': ['张隽翊', '计胜翔', '张庙松']})}

        qnaire_statistics: 问卷题答题情况数据统计。若收集中无问卷题，则返回None；否则返回一个字典，格式如下:
        { 题目标题: {选项: [选择此选项的人员名单]} }
        例如：
        {'你是否喜欢吃屎？': {'喜欢': ['王梓熙', '王广凯', '张隽翊', '张庙松'], '不喜欢': ['计胜翔']}}
    """
    choice_qtype = [Question_info.SINGLE_CHOICE, Question_info.MULTI_CHOICE]
    qnaire_qtype = [Question_info.SINGLE_QUESTIONNAIRE, Question_info.MULTI_QUESTIONNAIRE]

    # 查找选择题
    choice_qlist = Question_info.query.filter(Question_info.collection_id == collection_id,
                                              Question_info.question_type.in_(choice_qtype)). \
        with_entities(Question_info.id, Question_info.question_title).all()
    # 判断是否存在选择题
    if len(choice_qlist) == 0:
        choice_statistics = None
    else:
        choice_statistics = {}
        for id, title in choice_qlist:
            answer = Answer_info.query.filter_by(question_id=id).first().answer_option
            submit_content_list = Submit_Content_info.query.filter_by(question_id=id). \
                with_entities(Submit_Content_info.submission_id, Submit_Content_info.result). \
                all()
            id_list, result_list = zip(*submit_content_list)
            id_list, result_list = list(id_list), list(result_list)
            accuracy = result_list.count(answer) / len(result_list)  # 计算此题正确率

            # 将submission_id根据选择的选项进行分类
            A_list = list(filter(lambda x: 'A' in x[1], submit_content_list))
            A_id_list = list(map(itemgetter(0), A_list))
            B_list = list(filter(lambda x: 'B' in x[1], submit_content_list))
            B_id_list = list(map(itemgetter(0), B_list))
            C_list = list(filter(lambda x: 'C' in x[1], submit_content_list))
            C_id_list = list(map(itemgetter(0), C_list))
            D_list = list(filter(lambda x: 'D' in x[1], submit_content_list))
            D_id_list = list(map(itemgetter(0), D_list))
            detail = {}
            name_list = Submission_info.query.filter(Submission_info.id.in_(A_id_list)). \
                with_entities(Submission_info.submitter_name). \
                all()
            name_list = list(map(itemgetter(0), name_list))
            detail['A'] = name_list
            name_list = Submission_info.query.filter(Submission_info.id.in_(B_id_list)). \
                with_entities(Submission_info.submitter_name). \
                all()
            name_list = list(map(itemgetter(0), name_list))
            detail['B'] = name_list
            name_list = Submission_info.query.filter(Submission_info.id.in_(C_id_list)). \
                with_entities(Submission_info.submitter_name). \
                all()
            name_list = list(map(itemgetter(0), name_list))
            detail['C'] = name_list
            name_list = Submission_info.query.filter(Submission_info.id.in_(D_id_list)). \
                with_entities(Submission_info.submitter_name). \
                all()
            name_list = list(map(itemgetter(0), name_list))
            detail['D'] = name_list

            choice_statistics[title] = (answer, accuracy, detail)

    # 查找问卷题
    qnaire_qlist = Question_info.query.filter(Question_info.collection_id == collection_id,
                                              Question_info.question_type.in_(qnaire_qtype)). \
        with_entities(Question_info.id, Question_info.question_title).all()
    # 判断是否存在问卷题
    if len(qnaire_qlist) == 0:
        qnaire_statistics = None
    else:
        qnaire_statistics = {}
        for id, title in qnaire_qlist:
            option_list = Option_info.query.filter_by(question_id=id). \
                with_entities(Option_info.option_sn, Option_info.option_content). \
                all()
            submit_content_list = Submit_Content_info.query.filter_by(question_id=id). \
                with_entities(Submit_Content_info.submission_id, Submit_Content_info.result). \
                all()
            detail = {}
            for sn, content in option_list:
                submission_list = list(filter(lambda x: str(sn + 1) in x[1], submit_content_list))
                submission_id_list = list(map(itemgetter(0), submission_list))
                name_list = Submission_info.query.filter(Submission_info.id.in_(submission_id_list)). \
                    with_entities(Submission_info.submitter_name). \
                    all()
                name_list = list(map(itemgetter(0), name_list))
                detail[content] = name_list

            qnaire_statistics[title] = detail

    print("选择题数据统计：", choice_statistics)
    print("问卷题数据统计：", qnaire_statistics)
    return choice_statistics, qnaire_statistics
