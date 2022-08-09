#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Note: Python大作业后端
'''
from urllib import response
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.data_base import db_wrap
import json
import uuid
import os
from ocr import img2String
from question_parser import get_parsered_question

app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)
db  = db_wrap("my_question.db")

# 获取题目的总数
@app.route("/api/getQuestionNum", methods=['POST'])
def getQuestionNum():
    data = request.get_json()
    uploader_uid = int(data['uuid']) # 如果uuid为-1, 就不限制题目的uuid
    get_status = data['status'] # 如果状态为'temp',则获取等待提交的题目， 如果状态为'all', 则获取已经提交的题目
    print(get_status)
    # 题库中题目的数量
    num = db.get_db_size()
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
    ret = db.get_data_range(offset,num)
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

@app.route("/api/getQuestionOrdered", methods=['POST'])
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
        question = elem[1]
        question['id'] = id
        # 依据前端是否需要答案，配置此项目
        question.pop('ans')
        question_list.append(question)
    response = {
        "example_questions": question_list,
        "code": 'OK'
    }
    return jsonify(response)

def random_filename(filename):
    ext = os.path.splitext(filename)[-1]
    return uuid.uuid4().hex + ext

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

if __name__ == "__main__":
    # 开启服务
    app.config['JSON_AS_ASCII'] = False
    port = 5001
    app.run(host='0.0.0.0', port=port, threaded=False)
