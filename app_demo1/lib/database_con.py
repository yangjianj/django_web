# -*-coding:UTF-8 -*-
import sqlite3
import app_demo1.config.config as config


class DataManager():
    def __init__(self):
        dbpath= config.DATABASE
        self._conn = sqlite3.connect(dbpath,check_same_thread=False)
        self._cursor = self._conn.cursor()

    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,"_instance"):
            cls._instance = super().__new__(cls,*args,**kwargs)
        return cls._instance

    def exec_by_sql(self,sql):
        self._cursor.execute(sql)
        self._conn.commit()
        return True

    def close_conn(self):
        self._conn.close()

    def query_users(self):
        table=self._cursor.execute("select * from Users")
        self._conn.commit()
        return table

    def update_user(self,name,workid,role,project,telephone):
        try:
            table=self._cursor.execute("update Users set workid='%s', role='%s',project='%s',telephone='%s'  \
            where name='%s'"%(workid,role,project,telephone,name))
            self._conn.commit()
            return True
        except Exception as e:
            print(e)
            return e

    def add_user(self,name,workid,role,project,telephone):
        pass

    def delete_user(self,name):
        pass

    def save_api_case(self,apiresult):
        if ("re" in apiresult) and ("response" in apiresult["re"]):
            _caseid=apiresult["case"][1]
            _version = apiresult["case"][2]
            _apilink = apiresult["case"][6]
            _request_data = apiresult["case"][10]
            _response = apiresult["re"]["response"]
            _result = apiresult["re"]["test_result"]
            _spend = apiresult["spend"]
            _start_time = apiresult["start-time"]
            _end_time = apiresult["end-time"]
            try:
                table = self._cursor.execute("insert into api_case_result (caseid,version,api_link,request_data,response,result,spend,start_time,end_time) \
	            values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(_caseid,_version,_apilink,_request_data,_response,_result,_spend,_start_time,_end_time))
                self._conn.commit()
                return True
            except Exception as e:
                print("sql error----------------------")
                print(e)
                return e
        elif  ("re" in apiresult) and ("error" in apiresult["re"]):
            _caseid = apiresult["case"][1]
            _version = apiresult["case"][2]
            _apilink = apiresult["case"][6]
            _request_data = apiresult["case"][10]
            _response = apiresult["re"]["error"]
            _result = "error"
            _spend = apiresult["spend"]
            _start_time = apiresult["start-time"]
            _end_time = apiresult["end-time"]
            try:
                table = self._cursor.execute("insert into api_case_result (caseid,version,api_link,request_data,response,result,spend,start_time,end_time) \
                	            values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                _caseid, _version, _apilink, _request_data, _response, _result, _spend, _start_time, _end_time))
                self._conn.commit()
                return True
            except Exception as e:
                print("sql error----------------------")
                print(e)
                return e
        elif  ("error" in apiresult):
            _caseid = apiresult["case"][1]
            _version = apiresult["case"][2]
            _apilink = apiresult["case"][6]
            _request_data = apiresult["case"][10]
            _response = apiresult["error"]
            _result = "error"
            try:
                table = self._cursor.execute("insert into api_case_result (caseid,version,api_link,request_data,response,result) \
                	            values('%s','%s','%s','%s','%s'')" %(_caseid, _version, _apilink, _request_data, _response, _result))
                self._conn.commit()
                return True
            except Exception as e:
                print("sql error----------------------")
                print(e)
                return e


    def save_api_result(self):
        pass
    
    def create_ui_task(self,params):
        #创建task
        taskid = params['taskid']
        version = params['version']
        table = self._cursor.execute("insert into ui_task (taskid,version) values('{1}','{2}')".format(taskid,version))
        self._conn.commit()
    
    def add_case_to_task(self,params):
        #向task批量添加case
        taskid = params['taskid']
        caselist = params['caselist']
        for caseid in caselist:
            table = self._cursor.execute("insert into ui_task_case_table (taskid,caseid) values('{1}','{2}')".format(taskid, caseid))
            self._conn.commit()
        


if __name__ == '__main__':
    dd=DataManager()
    re=dd.query_Users()
    for i in re:
        print(i)
