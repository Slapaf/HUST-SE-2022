from init import db
from flask import flash
from datetime import datetime
from flask_login import current_user
from models import Collection_info, Question_info, Answer_info

question_dict = {'collectionTitle': '文件收集', 'collector': 'jsx', 'deadline': '2022-10-13T15:18',
                 'description': 'teset',
                 'question_name1': '姓名', 'question_file2': '文件', 'checked_topic2': '学号', 'question_file3': '文',
                 'checked_topic3': '学', 'question_sno4': '学', 'question_sno5': '学号', 'question_name6': '姓',
                 'question_radio7': '单选',
                 'checked_radio7': 'A', 'question_radio8': '单选题', 'checked_radio8': 'B'}

deadline = question_dict['deadline']
deadline = deadline.replace("T", " ")
format = '%Y-%m-%d %H:%M'
question_dict['deadline'] = datetime.strptime(deadline, format)
collection = Collection_info(creator=question_dict['collector'], creator_id=current_user.id,
                             collection_title=question_dict['collectionTitle'],
                             description=question_dict['description'], end_date=question_dict['deadline'],
                             status='1')
print(collection.id)

question_dict = [('collectionTitle', '文件收集'), ('collector', 'jsx'), ('deadline', '2022-10-20T16:43'),
                 ('description', 'wwf'),
                 ('question_name1', '姓名'), ('detail1', '123'), ('question_file2', '文件'), ('detail2', '456'),
                 ('question_qnaire3', '问卷题目'), ('detail3', '123'), ('qn_option3', 'a'), ('qn_option3', 'b'),
                 ('choose_type3', 'single'), ('question_multipleChoice4', '多选题'), ('detail4', '12312'),
                 ('checked_mulans4', 'A'),
                 ('checked_mulans4', 'C'), ('question_qnaire5', '问卷题'), ('detail5', 'erg'), ('qn_option5', ''),
                 ('qn_option5', ''),
                 ('choose_type6', 'multiple')]
