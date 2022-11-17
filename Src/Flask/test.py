from operator import itemgetter

l1 = [1, 2, 3, 4, 5]
l2 = [11, 22, 33, 44, 55]
print(1 in l1)
# d = {'单选1':{'A':['jsx','zjy'],'B':['wgk','wzx']}
#      '你喜欢跑步吗?':{'喜欢'}}

[('question_name1', '姓名lala'),
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

# [('张隽翊', datetime.datetime(2022, 11, 7, 16, 1, 19, 235046), 1, ['张隽翊', '二十大观看心得.docx', 'U202015362', 'C', 'A-B', '1']),
#  ('王广凯', datetime.datetime(2022, 11, 7, 16, 1, 19, 235046), 1,['王广凯', '王广凯dsb.pdf', 'U202015323', 'C', 'A-B', '1']),
#  ('计胜翔', datetime.datetime(2022, 11, 6, 15, 49, 27, 985976), 1,['计胜翔', '二十大观看心得.docx', 'U202015362', 'C', 'A-B', '1'])]

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

# 选择题数据统计：
choice_data = {'question_1': {
    'questionName': '单选题',
    'correctAnswer': 'A',
    'accuracy': 0.25,
    'A': ['王梓熙'],
    'B': ['张隽翊'],
    'C': ['王广凯'],
    'D': ['计胜翔']
},
    'question_2': {
        'questionName': '多选题',
        'correctAnswer': 'C-D',
        'accuracy': 0.25,
        'A': ['王梓熙', '计胜翔'],
        'B': ['王梓熙', '张隽翊'],
        'C': ['张隽翊', '王广凯'],
        'D': ['王广凯', '计胜翔']
    }
}

# 问卷题数据统计：
qnaire_data = {'question_1': {
    'questionName': '你喜欢吃屎吗？',
    'optionNumber': 2,
    'option_1': {
        'optionName': '喜欢',
        'peopleNumber': 3,
        'people': ['王梓熙', '张隽翊', '王广凯']
    },
    'option_2': {
        'optionName': '不喜欢',
        'peopleNumber': 1,
        'people': ['计胜翔']
    }
}
}

# kdulehxbxcpcebce
