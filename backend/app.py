#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Note: Python大作业后端
'''
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.data_base import db_wrap
from utils.user_data_base import user_db_wrap
import json
import uuid
import os
from ocr import img2String
from question_parser import get_parsered_question

import time
import datetime

app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)
db  = db_wrap("my_question.db")
user_db = user_db_wrap("my_users.db")

max_login_retry_pre_day = 3
max_login_time          = 2 * 60 * 60 # second
# 当超过max login time限制的时间后，登陆失效。

# {uuid:{user_name:'str',last_see:'time'}}
login_lut = {}

# {user_name:{retry_times:'times',last_retry_time:'time'}}
retry_lut = {}

# TODO
# 副作用， 每一次check status, 登陆的用户都会刷新一下last seen time，保持在线。 前端可以通过定期发送一个包，来保证在浏览网页的人不会被退出登陆
def check_status(uuid : str):
    if(uuid not in login_lut.keys):
        return False
    last_login_info = login_lut[uuid]
    last_time = int(last_login_info['last_see'])
    now_time = int(time.time())
    if(now_time - last_time > max_login_time):
        login_lut.pop(uuid)
        return False
    last_login_info['last_see'] = now_time
    login_lut[uuid] = last_login_info
    return True

def get_user_name(uuid : str):
    check_res = check_status(uuid)
    if(check_res == False):
        return None
    return login_lut[uuid]['user_name']

def login_wrong(user_name):
    if(user_name not in retry_lut):
        retry_lut[user_name] = {'retry_times' : 0, 'last_retry_time' : 0}
    retry_info = retry_lut[user_name]
    retry_info['retry_times'] += 1
    retry_info['last_retry_time'] = int(time.time())
    retry_lut[user_name] = retry_info
    return

# TODO
# 副作用， 已经登陆的用户再一次登陆时，会更新token，使旧Token失效
def login(user_name : str,password : str):
    user_info = user_db.get_user_info(user_name)
    if(user_name in retry_lut):
        if(retry_lut[user_name]['retry_times'] >= max_login_retry_pre_day and (time.time() - retry_lut[user_name]['last_retry_time']) < 24 * 60 * 60):
            retry_lut[user_name]['last_retry_time'] = time.time()
            return {'code':'Max retry_time limit !'}
    if(user_info == None):
        login_wrong(user_name)
        print('NO USER FOUND')
        return {'code':'Wrong username or password !'}
    if(password != str(user_info[1])):
        print('ERROR PASSWD ' + password + ' | ' + str(user_info[1]))
        login_wrong(user_name)
        return {'code':'Wrong username or password !'}
    user_token_open = user_name + str(time.time()) + password + str('tHiS Is S@lt') + str(len(login_lut))
    user_token = hashlib.sha256(user_token_open.encode('utf-8')).hexdigest()
    login_lut[user_token] = {'user_name':user_name,'last_see':time.time()}
    return user_token
    
# 副作用，效果等同于直接调用check status
def get_user_name(uuid:str):
    if(check_status(uuid) == False):
        return None
    return login_lut[uuid]['user_name']

# 获取题目的总数
@app.route("/api/getQuestionNum", methods=['POST'])
def getQuestionNum():
    data = request.get_json()
    uploader_uid = int(data['uuid']) # 如果uuid为-1, 就不限制题目的uuid
    get_status = data['status'] # 如果状态为'temp',则获取等待提交的题目， 如果状态为'all', 则获取已经提交的题目
    print(get_status)
    # 题库中题目的数量
    num = db.get_db_size(status=get_status)
    response = {
        "num": num,
        "code": 'OK'
    }
    return jsonify(response)

# 获取一定数量的题目信息(已经确认提交的)
@app.route("/api/getQuestionOrdered", methods=['POST'])
def getQuestionOrdered():
    data = request.get_json()
    uploader_uid = int(data['uuid']) # 如果uuid为-1, 就不限制题目的uuid
    get_status = data['status'] # 如果状态为'temp',则获取等待提交的题目， 如果状态为'all', 则获取已经提交的题目
    # 数量，从前端请求中获取
    num = int(data['num'])
    # 开始的索引
    offset = int(data['offset'])
    ret = db.get_data_range(offset,num,status=get_status)
    question_list = []
    for elem in ret:
        id = elem[0]
        question = json.loads(elem[1])
        question['ID'] = id
        # if(question['type'] != 'filling'):
        #     question['description'] = question['question'] + '\n' + ' '.join([elem + question['choice'][elem] for elem in question['choice']])
        # else:
        #     question['description'] = question['question']
        # 依据前端是否需要答案，配置此项目
        # question.pop('ans')
        question_list.append(question)
    response = {
        "example_questions": question_list,
        "code": 'OK'
    }
    return jsonify(response)

@app.route("/api/getQuestionRandom", methods=['POST'])
def getQuestionRandom():
    data = request.get_json()
    uploader_uid = int(data['uuid']) # 如果uuid为-1, 就不限制题目的uuid
    get_status = data['status'] # 如果状态为'temp',则获取等待提交的题目， 如果状态为'all', 则获取已经提交的题目
    # 数量，从前端请求中获取
    num = int(data['num'])
    ret = db.get_data_random(num,status=get_status)
    question_list = []
    for elem in ret:
        id = elem[0]
        question = json.loads(elem[1])
        question['ID'] = id
        # 依据前端是否需要答案，配置此项目
       #  question.pop('ans')
        question_list.append(question)
    response = {
        "example_questions": question_list,
        "code": 'OK'
    }
    return jsonify(response)

def random_filename(filename):
    ext = os.path.splitext(filename)[-1]
    return uuid.uuid4().hex + ext

@app.route("/api/addQuestion", methods=['POST'])
def addQuestion():
    data = request.get_json()
    print(data)
    question_json = data['question_info']
    db.insert_data(question_json, status='temp')
    response = {
        'code': 'OK'
    }
    return jsonify(response)

@app.route("/api/uploadFile", methods=['POST'])
def uploadFile():
    file = request.files.get('file')
    print(file.filename)

    filename = random_filename(file.filename)
    filepath = os.path.join('uploads_tmp', filename)
    filepath = os.path.join(app.root_path, filepath)
    file.save(filepath)
    try:
        text = img2String(filepath)
        print(text)
        question_list = [get_parsered_question(question) for question in text]
        print(question_list)
        for question in question_list:
            db.insert_data(question,status='temp')
    except:
        return jsonify({'code' : 'ERROR IN PARSING'})

    return jsonify({'code' : 'OK'})

# 前端请求添加题目（传过来图片，和提交者名称，返回题目列表）
# 流程 获取图片文件 -> (optional) 对图片进行转码 -> OCR -> parser -> 加入提交者名称 -> database -> 返回
@app.route("/api/delQuestion", methods=['POST'])
def delQuestion():
    data = request.get_json()
    print(data)
    delete_id = int(data['ID'])
    db.delete_data(delete_id)
    response = {
        'code': 'OK'
    }
    return jsonify(response)

# 前端请求对题目信息进行变更（传过来题目id，变更后的题目json,后端进行保存）
@app.route("/api/setQuestion", methods=['POST'])
def setQuestion():
    data = request.get_json()
    print(data)
    data_id = int(data['ID'])
    question_json = data['question_info']
    db.update_data_byid(data_id,question_json)
    response = {
        'code': 'OK'
    }
    return jsonify(response)


@app.route("/api/handleSubmit", methods=['POST'])
def handleSubmit():
    data = request.get_json()
    submit_id = data['submit_ids']
    for id in submit_id:
        db.submit_data(id['ID'])
    response = {
        'code': 'OK'
    }
    return jsonify(response)

@app.route("/api/login", methods=['POST'])
def handleLogin():
    login_requests = request.get_json()
    print(login_requests)
    return_uuid = login(user_name=login_requests['user_name'],password=login_requests['password'])
    if(type(return_uuid) == dict):
        response = {
            'code': return_uuid['code'],
            'uuid': -1
        }
    else:
        response = {
            'code': 'OK',
            'uuid': return_uuid
        }
    print(response)
    return jsonify(response)

@app.route("/api/registration", methods=['POST'])
def handleRegistration():
    reg_requests = request.get_json()
    user_name = reg_requests['user_name']
    password  = reg_requests['password']
    info = user_db.register_user(user_name,password)
    return jsonify({'code':info})
    #备注，只有返回OK才可以完成注册，否之返回Code即为错误原因

@app.route("/api/recordResult", methods=['POST'])
def recordTestResult():
    req = request.get_json()
    user_name = get_user_name(req['uuid'])
    table = req['table_data']
    print(req)
    if(user_name == None):
        return jsonify({'code':'Not valid UUID'})
    old_info = user_db.get_user_info(user_name)
    correct_cnt = 0
    wrong_cnt = 0
    wrong_list = []
    for elem in table:
        if(elem['result'] == 'accepted'):
            correct_cnt += 1
        else:
            wrong_cnt   += 1
            wrong_list.append(elem['ID'])
    new_record = {
        'time' : datetime.date.today(),
        'wrong': wrong_cnt, 
        'total': correct_cnt + wrong_cnt,
        'wrong_id' : wrong_list,
        'accuracy' : (wrong_cnt) / (correct_cnt + wrong_cnt)
    }
    #{time: y - m - d in string, wrong : int, total : int, wrong_id : list, accuracy : cal}
    old_record = json.loads(old_info[3])
    old_record.append(new_record)
    print(old_record)
    user_db.set_user_info(user_name,history=old_record)

if __name__ == "__main__":
    # 开启服务
    app.config['JSON_AS_ASCII'] = False
    port = 5001
    app.run(host='0.0.0.0', port=port, threaded=False)
