import re

str = "fsdfs12"
t = int(re.findall(r"\d+", str)[0])
print(t)

for i in range(1, 5):
    print(i)

# [('question_name1', '姓名lala'),
#  ('submit_name1', '计胜翔'),
#  ('question_file2', '文件haha'),
#  ('submit_file2', '二十大观看心得.docx'),
#  ('question_sno3', '学号xixi'),
#  ('submit_sno3', 'U202015362'),
#  ('question_radio4', '单选题nie'),
#  ('submit_checked_radio4', 'C'),
#  ('question_multipleChoice5', '多选题kk'),
#  ('submit_checked_mulans5', 'A'),
#  ('submit_checked_mulans5', 'B'),
#  ('question_qnaire6', '你喜欢跑步吗？'),
#  ('submit_checked_qnaire6', '1')]

# [('张隽翊', datetime.datetime(2022, 11, 7, 16, 1, 19, 235046), 1, ['张隽翊', '二十大观看心得.docx', 'U202015362', 'C', 'A-B', '1']),
#  ('王广凯', datetime.datetime(2022, 11, 7, 16, 1, 19, 235046), 1,['王广凯', '王广凯dsb.pdf', 'U202015323', 'C', 'A-B', '1']),
#  ('计胜翔', datetime.datetime(2022, 11, 6, 15, 49, 27, 985976), 1,['计胜翔', '二十大观看心得.docx', 'U202015362', 'C', 'A-B', '1'])]
