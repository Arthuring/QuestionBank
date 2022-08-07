#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Note: Python大作业后端
'''
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
import argparse
from utils.data_base import db_wrap
import json

app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)
db  = db_wrap("my_question.db")

# 获取题目的总数
@app.route("/api/getQuestionNum", methods=['POST'])
def getQuestionNum():
    data = request.get_json()
    # 题库中题目的数量
    num = db.get_db_size()
    response = {
        "example_questions": num,
        "code": 'OK'
    }
    return jsonify(response)

# 获取一定数量的题目信息
@app.route("/api/getQuestionOrdered", methods=['POST'])
def getQuestionOrdered():
    data = request.get_json()
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
        # 依据前端是否需要答案，配置此项目
        question.pop('ans')
        question_list.append(question)
    response = {
        "example_questions": question_list,
        "code": 'OK'
    }
    return jsonify(response)


@app.route("/api/getQuestionOrdered", methods=['POST'])
def getQuestionRandom():
    data = request.get_json()
    # 数量，从前端请求中获取
    num = int(data['num'])
    ret = db.get_data_random(num)
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


if __name__ == "__main__":
    # 开启服务
    app.config['JSON_AS_ASCII'] = False
    port = 5001
    app.run(host='0.0.0.0', port=port, threaded=False)
