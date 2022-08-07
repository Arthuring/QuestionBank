import imp
from utils.data_base import db_wrap

db = db_wrap("my_question.db")

from parser import get_parsered_question

# 要求格式示例（理论上修改正则就能改变）
test_str_filling = '[填空题] Beihang University的英文简写是______ [Ans]:...'
test_str_single_choice = '[单选] 下列哪个xxxx不是？ [A]:... [B]:... [C]:... [D]:... [Ans]:A/B/C/D'
test_str_multiple_choice = '[多选] 下列哪些xxxx不是？ [A]:... [B]:... [C]:... [D]:... [Ans]:ACD'

q = [get_parsered_question(test_str_filling),get_parsered_question(test_str_single_choice),get_parsered_question(test_str_multiple_choice)]

id = db.insert_data(q[0])
id = db.insert_data(q[1])
id = db.insert_data(q[2])

for i in range(db.get_db_size()):
    print(i,': ', db.get_data_byindex(i))