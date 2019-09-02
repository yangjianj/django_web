# -*- coding: utf-8 -*-
import re,random
from app_demo1.lib.tool import *
import app_demo1.config.config

class Testcase():
    def __init__(self,steps,operate):
        self.steps = steps
        self.id = steps[0][config.EXCELMAPPING["用例编号"]]
        self.result = {"result":"passed","steps":[]}
        self.operate = operate
        self.suite_dir = ''
        self.case_dir = ''
        self.variable={}   #case变量存放，优先级大于suite变量
        self.suite_variable={} #suite变量存放地

    @record_time
    def run(self):
        self.case_dir =create_case_dir(self.suite_dir,self.id)
        self.setup()
        self.runstep()
        self.teardown()
        return self.result

    def runstep(self):
        for step in self.steps:
            if self.result["result"] == "failed" :
                block_result = {"result":"block","message":None}
                self._record_step_result(step,block_result)
                continue
            msg={"action":step[config.EXCELMAPPING["操作"]],"page":step[config.EXCELMAPPING["PageName"]],"element":step[config.EXCELMAPPING["元素名称"]]}
            try:
                msg["value"]=json.loads(step[config.EXCELMAPPING["value"]])
            except Exception as  error:
                msg["value"] = step[config.EXCELMAPPING["value"]]
            result = self.execute(msg)
            self._record_step_result(step,result)

    def execute(self,msg):
        #执行方法在不属于case实例方法则使用operate执行
        msg["value"] = self._data_identify(msg["value"])
        try:
            emeth = getattr(self, msg['action'])
            message = emeth(msg)
            re = {"result": "passed", "message": message}
        except Exception as error:
            message=self.operate.execute(msg)
            re = message
        return re

    def setup(self):
        pass

    def teardown(self):
        filepath=os.path.join(self.case_dir,"ending_screen.png")
        self.operate.handler.browser.get_screenshot_as_file(filepath)

    def log(self):
        pass

    def get_variable(self,msg):
        var = ''
        if 'value' in msg:
            key = msg["value"]['value']
            if key in self.variable:
                var = self.variable[key]
            elif key in self.suite_variable:
                var = self.suite_variable[key]
        else:
            var = {"variable":self.variable,"suite_variable":self.suite_variable}
        return var
    '''
    def _data_identify(self,data):
        # type(data) = dict识别输入数据中引用的变量，变量格式<val>
        for item in data:
            if '<' in str(data[item]):  #此行可去除，为减小运算度而保留
                try:
                    val = re.match("^<(\S*)>$", data[item]).group(1)
                    if val in self.variable:
                        data[item] = self.variable[val]
                    elif val in self.suite_variable:
                        data[item] = self.suite_variable[val]
                    else:
                        data[item] = eval(val)
                except Exception as error:
                    pass
        return data
    '''

    def _find_variable(self,val):
        if val in self.variable:
            re = self.variable[val]
        elif val in self.suite_variable:
            re = self.suite_variable[val]
        else:
            re = eval(val)
        return re

    def _data_identify(self,data):
        for item in data:
            if type(data[item]) == str:
                #pattern = re.compile(r'<[()_,\.a-zA-Z0-9]+>')
                pattern = re.compile(r'<[^\s<>]+>')
                result1 = pattern.findall(data[item])
                if len(result1) != 0:
                    for i in result1:
                        key=i.replace('<', '').replace('>', '')
                        data[item]=data[item].replace(i,'self._find_variable("%s")'%key)
                    data[item] = eval(data[item])
        return data

    def _record_step_result(self,step,result):
        step[config.EXCELMAPPING["执行结果"]] = result["result"]
        step[config.EXCELMAPPING["执行信息"]] = str(result["message"])
        if result["result"] == "failed":
            self._error_handler(step[config.EXCELMAPPING["PageName"]])
            self.result["result"] = "failed"
        else:
            if step[config.EXCELMAPPING["输出数据"]] != '':
                result_key = step[config.EXCELMAPPING["输出数据"]]
                self.variable[result_key]=step[config.EXCELMAPPING["执行信息"]]
        self.result["steps"].append(step)

    def _error_handler(self,curr_action):
        timestr = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        filepath= os.path.join(self.case_dir,curr_action+timestr+".png")
        self.operate.handler.browser.get_screenshot_as_file(filepath)