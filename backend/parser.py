# 输出Json格式
# {
#     'id' ：integer,
#     'type' : 'filling',
#     'question' : 'Beihang University的英文简写是______',
#     'ans' : 'BUAA'
# }
# {
#     'id' ：integer,
#     'type' : 'single choice',
#     'question' : '下列哪个xxxx不是？',
#     'choice' : {
#         'A': '...',
#         'B': '...',
#         'C': '...',
#         'D': '...'
#     },      
#     'ans' : 'A'
# }
# {
#     'id' ：integer,
#     'type' : 'multiple choice',
#     'question' : '下列哪些xxxx不是？',
#     'choice' : {
#         'A': '...',
#         'B': '...',
#         'C': '...',
#         'D': '...'
#     }, 
#     'ans' : 'ABC'
# }

import re
def get_parsered_question(question:str):
    question = question.replace(' ','')
    print(question)
    controlling_flag = re.findall(r"\[(.+?)\]",question)
    question_str = re.findall(r"\](.+?)\[",question)
    ans_str = re.findall(r"\[Ans\]:(.+)",question)
    ans_str = [l.strip() for l in ans_str]
    question_str = [l.strip() for l in question_str]
    controlling_flag = [l.strip() for l in controlling_flag]
    type_str = controlling_flag[0]
    ending_str = controlling_flag[-1]
    result = {'type':None,'question':None,'ans':None}
    result['ans'] = ' '.join(ans_str)
    assert(ending_str == 'Ans')
    if(type_str == '填空题'):
        result['type'] = 'filling'
        result['question'] = ' '.join(question_str)
    elif(type_str == '单选'):
        if(len(question_str) != len(controlling_flag) - 1 or len(question_str) == 1):
            print("Unexpected single choice question!")
            return None
            # assert(1)
        result['type'] = 'single choice'
        result['question'] = question_str[0]
        choice = {}
        for i in range(1,len(question_str)):
            choice[controlling_flag[i]] = question_str[i]
        result['choice'] = choice
    elif(type_str == '多选'):
        if(len(question_str) != len(controlling_flag) - 1 or len(question_str) == 1):
            print("Unexpected single choice question!")
            return None
            # assert(1)
        result['type'] = 'multiple choice'
        result['question'] = question_str[0]
        choice = {}
        for i in range(1,len(question_str)):
            choice[controlling_flag[i]] = question_str[i]
        result['choice'] = choice
    else:
        print('Unexpected question type')
        return None
        # assert(1)
    return result