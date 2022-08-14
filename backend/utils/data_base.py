import sqlite3
import os.path
import json

class db_wrap:
    
    sql_connection = 0
    id_seq = -1

    def __init__(self,database_name = "/home/dofingert/Source/Python_project/my_question.db"):
        if(os.path.isfile(database_name) == False):
            self.sql_connection = sqlite3.connect(database_name)
            data_base_cur = self.sql_connection.cursor()
            data_base_cur.execute("CREATE TABLE QUESTION_TABLE(ID INT KEY NOT NULL, QUESTION_JSON TEXT NOT NULL, UPLOADER TEXT NOT NULL, STATUS TEXT NOT NULL)")
            data_base_cur.execute("INSERT INTO QUESTION_TABLE (ID,QUESTION_JSON,UPLOADER,STATUS) VALUES (?,?,\"SYSTEM\",\"READ_ONLY\")",(-1,'0',))
            self.sql_connection.commit()
            self.id_seq = 0
        else:
            self.sql_connection = sqlite3.connect(database_name)
            self.id_seq = self.get_max_id()

    def __del__(self):
        self.db_close()

    def get_db_size(self,uploader = 'system',status = 'all'): # 如果状态为'temp',则获取等待提交的题目， 如果状态为'all', 则获取已经提交的题目
        cur = self.sql_connection.cursor()
        try :
            cur.execute("DROP TABLE TEMP")
        except:
            print()
        cur.execute("CREATE TABLE TEMP AS SELECT * FROM QUESTION_TABLE")
        if(uploader != 'system'):
            cur.execute("DELETE FROM TEMP WHERE UPLOADER != ?",(uploader,))
        if(status != 'all'):
            cur.execute("DELETE FROM TEMP WHERE STATUS != ?",(status,))
        cur.execute("SELECT count(*) FROM TEMP")
        result = cur.fetchone()
        try :
            cur.execute("DROP TABLE TEMP")
        except:
            print()
        return result[0] - 1

    def insert_data(self,data:str,uploader = 'system',status = 'ready'): #prefix: data is string
        if(type(data) != str):
            if(type(data) == dict):
                data = json.dumps(data)
            else:
                print('data_base: Error datatype !')
                return -1
        id = self.alloc_id()
        cur = self.sql_connection.cursor()
        cur.execute("INSERT INTO QUESTION_TABLE (ID,QUESTION_JSON,UPLOADER,STATUS) VALUES (?,?,?,?)",(id,data,uploader,status,))
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
    
    def get_data_range(self,index_begin:int,num:int,uploader = 'system',status = 'all'):
        cur = self.sql_connection.cursor()
        try :
            cur.execute("DROP TABLE TEMP")
        except:
            print()
        cur.execute("CREATE TABLE TEMP AS SELECT * FROM QUESTION_TABLE")
        if(uploader != 'system'):
            cur.execute("DELETE FROM TEMP WHERE UPLOADER != ?",(uploader,))
        if(status != 'all'):
            cur.execute("DELETE FROM TEMP WHERE STATUS != ?",(status,))
        cur.execute("SELECT * FROM TEMP LIMIT ? Offset ?", (num,index_begin + 1,))
        data = cur.fetchall()
        try :
            cur.execute("DROP TABLE TEMP")
        except:
            print()
        return data

    def get_data_random(self,num:int,uploader = 'system',status = 'all'):
        cur = self.sql_connection.cursor()
        try :
            cur.execute("DROP TABLE TEMP")
        except:
            print()
        cur.execute("CREATE TABLE TEMP AS SELECT * FROM QUESTION_TABLE")
        if(uploader != 'system'):
            cur.execute("DELETE FROM TEMP WHERE UPLOADER != ?",(uploader,))
        if(status != 'all'):
            cur.execute("DELETE FROM TEMP WHERE STATUS != ?",(status,))
        cur.execute("SELECT * FROM TEMP WHERE ID != -1 ORDER BY RANDOM() LIMIT ?", (num,))
        data = cur.fetchall()
        try :
            cur.execute("DROP TABLE TEMP")
        except:
            print()
        return data

    def get_data_byindex(self,data_index:int):
        cur = self.sql_connection.cursor()
        cur.execute("SELECT * FROM QUESTION_TABLE LIMIT 1 Offset ?", (data_index + 1,))
        data = cur.fetchone()
        return data

    def update_data_byid(self,data_id:int,data:str,uploader = 'system',status = 'temp'):
        old_data = self.get_data_byid(data_id)
        if(type(data) != str):
            if(type(data) == dict):
                data = json.dumps(data)
            else:
                print('data_base: Error datatype !')
                return -1
        if(old_data == None):
            id = data_id
            cur = self.sql_connection.cursor()
            cur.execute("INSERT INTO QUESTION_TABLE (ID,QUESTION_JSON,UPLOADER,STATUS) VALUES (?,?,?,?)",(id,data,uploader,status))
        else:
            cur = self.sql_connection.cursor()
            cur.execute("UPDATE QUESTION_TABLE SET QUESTION_JSON = ? WHERE ID == ?",(data,data_id))
            cur.execute("UPDATE QUESTION_TABLE SET STATUS = ? WHERE ID == ?",(status,data_id))
        return data

    def submit_data(self,data_id):
        old_data = self.get_data_byid(data_id)
        if(old_data != None):
            cur = self.sql_connection.cursor()
            cur.execute("UPDATE QUESTION_TABLE SET STATUS = ? WHERE ID == ?",('ready',data_id))
        data = self.get_data_byid(data_id)
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