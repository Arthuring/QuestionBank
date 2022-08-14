import sqlite3
import os.path
import json
import hashlib

from soupsieve import select

class user_db_wrap:
    sql_connection = 0
    id_seq = -1

    def __init__(self,database_name = "/home/dofingert/Source/Python_project/my_question.db"):
        if(os.path.isfile(database_name) == False):
            self.sql_connection = sqlite3.connect(database_name)
            data_base_cur = self.sql_connection.cursor()
            data_base_cur.execute("CREATE TABLE USER (USER_NAME TEXT NOT NULL, PASSWORD TEXT NOT NULL, FAVOUR TEXT NOT NULL, WRONG TEXT NOT NULL, SCORE TEXT NOT NULL)")
            self.sql_connection.commit()
            self.id_seq = 0
        else:
            self.sql_connection = sqlite3.connect(database_name)
            self.id_seq = self.get_max_id()

    def get_user_info(self,user_name = 'system'):
      cur = self.sql_connection.cursor()
      cur.execute("SELECT * FROM USER WHERE USER_NAME == ?",(user_name,))
      r = cur.fetchall()
      if(len(r) != 1):
        return None
      return r[0]
    
    def encrypt(self,code):
      return hashlib.sha256(code.encode('utf-8')).hexdigest()

    def register_user(self,user_name,password):
      user_info = self.get_user_info(user_name)
      if(user_info != None):
        return 'User name not valid.'
      if(password == None):
        return 'Password not valid'
      cur = self.sql_connection.cursor()
      cur.execute("INSERT INTO USER (USER_NAME PASSWORD FAVOUR WRONG) VALUES (?,?,?,?)"(user_name,password,str([]),str([])))
      return 'OK'

    def set_user_info(self,user_name,password = None,favour = None,wrong = None):
      cur = self.sql_connection.cursor()
      if(password != None):
        cur.execute("UPDATE USER SET PASSWORD = ? WHERE USER_NAME = ?",password,user_name)
      if(favour != None):
        cur.execute("UPDATE USER SET FAVOUR   = ? WHERE USER_NAME = ?",favour,user_name)
      if(wrong != None):
        cur.execute("UPDATE USER SET WRONG    = ? WHERE USER_NAME = ?",favour,user_name)