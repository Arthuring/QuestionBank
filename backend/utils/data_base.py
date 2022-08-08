import sqlite3
import os.path
import json

from sympy import false

class db_wrap:
    
    sql_connection = 0
    id_seq = -1

    def __init__(self,database_name = "/home/dofingert/Source/Python_project/my_question.db"):
        if(os.path.isfile(database_name) == false):
            self.sql_connection = sqlite3.connect(database_name)
            data_base_cur = self.sql_connection.cursor()
            data_base_cur.execute("CREATE TABLE QUESTION_TABLE(ID INT KEY NOT NULL, QUESTION_JSON TEXT NOT NULL)")
            data_base_cur.execute("INSERT INTO QUESTION_TABLE (ID,QUESTION_JSON) VALUES (?,?)",(-1,'0',))
            self.sql_connection.commit()
            self.id_seq = 0
        else:
            self.sql_connection = sqlite3.connect(database_name)
            self.id_seq = self.get_max_id()

    def __del__(self):
        self.db_close()

    def get_db_size(self):
        cur = self.sql_connection.cursor()
        cur.execute("SELECT count(*) FROM QUESTION_TABLE")
        result = cur.fetchone()
        return result[0] - 1

    def insert_data(self,data:str): #prefix: data is string
        if(type(data) != str):
            if(type(data) == dict):
                data = json.dumps(data)
            else:
                print('data_base: Error datatype !')
                return -1
        id = self.alloc_id()
        cur = self.sql_connection.cursor()
        cur.execute("INSERT INTO QUESTION_TABLE (ID,QUESTION_JSON) VALUES (?,?)",(id,data,))
        return id

    def delete_data(self,data_id:int):
        if(data_id < 0):
            return -1
        cur = self.sql_connection.cursor()
        cur.execute("DELETE FROM QUESTION_TABLE WHERE ID == ?", (data_id,))
        return self.get_db_size()

    def get_data_byid(self,data_id:int):
        cur = self.sql_connection.cursor()
        cur.execute("SELECT * FROM QUESTION_TABLE WHERE ID == ?", (data_id,))
        data = cur.fetchone()
        return data
    
    def get_data_range(self,index_begin:int,num:int):
        cur = self.sql_connection.cursor()
        cur.execute("SELECT * FROM QUESTION_TABLE LIMIT ? Offset ?", (num,index_begin + 1,))
        data = cur.fetchall()
        return data

    def get_data_random(self,num:int):
        cur = self.sql_connection.cursor()
        cur.execute("SELECT * FROM QUESTION_TABLE WHERE ID != -1 ORDER BY RANDOM() LIMIT ?", (num,))
        data = cur.fetchall()
        return data

    def get_data_byindex(self,data_index:int):
        cur = self.sql_connection.cursor()
        cur.execute("SELECT * FROM QUESTION_TABLE LIMIT 1 Offset ?", (data_index + 1,))
        data = cur.fetchone()
        return data

    def update_data_byid(self,data_id:int,data:str):
        old_data = self.get_data_byid(data_id)
        if(old_data == None):
            id = data_id
            cur = self.sql_connection.cursor()
            cur.execute("INSERT INTO QUESTION_TABLE (ID,QUESTION_JSON) VALUES (?,?)",(id,data,))
        else:
            cur = self.sql_connection.cursor()
            cur.execute("UPDATE QUESTION_TABLE SET QUESTION_JSON = ? WHERE ID == ?",(data,data_id,))
        return data

    def get_max_id(self):
        if(self.id_seq != -1):
            return self.id_seq
        cur = self.sql_connection.cursor()
        cur.execute("SELECT * FROM QUESTION_TABLE WHERE ID == ?", (-1,))
        data = cur.fetchone()
        return int(data[1])

    def alloc_id(self):
        ret = self.id_seq
        self.id_seq += 1
        return ret

    def sync_id(self):
        data_base_cur = self.sql_connection.cursor()
        data_base_cur.execute("UPDATE QUESTION_TABLE SET QUESTION_JSON = ? WHERE ID == ?",(str(self.id_seq),-1,))

    def db_close(self):
        self.sync_id()
        self.sql_connection.commit()
        self.sql_connection.close()