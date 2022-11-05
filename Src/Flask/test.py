import datetime


def text(t):
    if t is not None:
        print(t)
    else:
        print("t is None")


start = datetime.datetime.strptime("2022-11-1 0:0:0", '%Y-%m-%d %H:%M:%S')
end = datetime.datetime.strptime("2022-11-3 1:11:0", '%Y-%m-%d %H:%M:%S')
print(end - start)

{'1_collectionTitle': '文件收集',
 '2_collector': '凯',
 '3_deadline': '2022-11-24 23:26',
 '4_description': '描述',
 '5_question_fill1': '姓名lala',
 '6_question_qnaire1': '姓名lala',
 '7_choose_type1': 'multiple',
 '8_detail1': '',
 '9_question_file2': '文件haha',
 '10_question_qnaire2': '文件haha',
 '11_choose_type2': 'multiple',
 '12_detail2': '请提交本次作业',
 '13_question_fill3': '学号xixi',
 '14_question_qnaire3': '学号xixi',
 '15_choose_type3': 'multiple',
 '16_detail3': '',
 '17_question_radio4': '单选题nie',
 '18_question_qnaire4': '单选题nie',
 '19_choose_type4': 'multiple',
 '20_detail4': '',
 '21_question_multipleChoice5': '多选题kk',
 '22_question_qnaire5': '多选题kk',
 '23_choose_type5': 'multiple',
 '24_detail5': '',
 '25_question_qnaire6': '你喜欢跑步吗？',
 '26_choose_type6': 'multiple',
 '27_qn_option6': '喜欢',
 '28_qn_option6': '不喜欢',
 '29_qn_option6': '还行',
 '30_detail6': '请选择一个选项'}

collectionTitle:
文件收集
collector:
张三
deadline:
2022 - 11 - 10
T23: 42:17
description:
jb
question_name1:
姓名lala
detail1:
question_file2:
文件haha
detail2:
checked_topic2:
姓名lala
checked_topic2:
学号xixi
question_sno3:
学号xixi
detail3:
question_radio4:
单选题nie
detail4:
checked_radio4:
A
question_multipleChoice5:
多选题kk
detail5:
checked_mulans5:
C
checked_mulans5:
D
question_qnaire6:
你喜欢跑步吗？
detail6:
qnmd
qn_option6:
喜欢
qn_option6:
不喜欢
qn_option6:
还行
choose_type6:
multiple

[('collectionTitle', '文件收集'),
 ('collector', '张三'),
 ('deadline', '2022-11-10T23:42:17'),
 ('description', 'jb'),
 ('question_name1', '姓名lala'),
 ('detail1', ''),
 ('question_file2', '文件haha'),
 ('detail2', ''),
 ('checked_topic2', '姓名lala'),
 ('checked_topic2', '学号xixi'),
 ('question_sno3', '学号xixi'), ('detail3', ''),
 ('question_radio4', '单选题nie'), ('detail4', ''), ('checked_radio4', 'A'), ('question_multipleChoice5', '多选题kk'),
 ('detail5', ''), ('checked_mulans5', 'C'), ('checked_mulans5', 'D'), ('question_qnaire6', '你喜欢跑步吗？'),
 ('detail6', 'qnmd'), ('qn_option6', '喜欢'), ('qn_option6', '不喜欢'), ('qn_option6', '还行'),
 ('choose_type6', 'multiple')]
