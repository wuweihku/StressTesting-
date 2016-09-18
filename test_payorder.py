# -*- coding: utf-8 -*-
import unittest                                         #支持Python单元测试模块
import urllib.parse                                     #这里urllib.parse要精确到子模块,否则会报错
import urllib.request                                   #这里urllib.request要精确到子模块,否则会报错
import csv                                              #支持csv自动化导表
import sys                                              #支持log
import time                                             #支持时间戳
import hashlib                                          #支持MD5加密


'''
IOS内购获取订单号接口
接口说明：返回一个唯一订单号（奥飞生成）
请求方式：POST
测试地址：http://payapi.qa.15166.com/pay/order

'''

class test_payorder(unittest.TestCase):
    url = 'http://payapi.qa.15166.com/pay/order'        #所要访问的url,一个测试类对应一个url

    def setUp(self):                                    #基境建立
        pass        
    def tearDown(self):                                 #基境清理
        pass
    def test_payorder_cases(self):                      #执行测试功能的函数
        with open('csv/payorder_data.csv') as csvfile:  #打开csv文件流
            reader = csv.DictReader(csvfile)            #创建文件流对象
            totalnum = 0                                  #计算一共跑了多少条测试数据
            for row in reader:                          #这里的row对应csv表里的一行数据,第一行数据自动作为字段名,第二行数据开始作为测试实例
                totalnum += 1
                with self.subTest(row=row):             #row=i,会报错row is not defined,必须用row=row(这里用的是subTest功能)
                    print("正在执行第 %d 条测试数据"% totalnum)     #每跑一条数据,显示一次当前进度
                    info = {'action': row['action'], 
                            'userID': row['userID'], 
                            'username':row['username'], 
                            'appID':row['appID'],
                            'roleID':row['roleID'],
                            'roleName':row['roleName'],
                            'roleLevel':row['roleLevel'],
                            'serverID':row['serverID'],
                            'serverName':row['serverName'],
                            'accessToken':row['accessToken'],
                            'payChannel':row['payChannel'],
                            'money':row['money'],
                            'coin':row['coin'],
                            'currency':row['currency'],
                            'productID':row['productID'],
                            'productName':row['productName'],
                            'productDesc':row['productDesc'],
                            'sdkVersion':row['sdkVersion'],
                            'device':row['device'],
                            'osVersion':row['osVersion'],
                            'imei':row['imei'],
                            'mac':row['mac'],
                            'sdkExtension':row['sdkExtension'],
                            'packageVersion':row['packageVersion'],
                            'extension':row['extension'],
                            'cpOrderID':row['cpOrderID'],
                            'signType':row['signType'],
                            'signature':row['signature']
                            } #csv里的每一行测试实例，这里不用过滤空值，空值可以作为测试用例，引发异常. 注意：为了保证压测性能，这里的每一次读取，应该都是完备的数据，不需要额外处理.
                    info['extension'] = {'acessToken': 'Xy8HVpI8LnJfxywHjy_oWIKzdvx4WvbQ', 'uid': 1303829}
                    print(info)
                    postdata = urllib.parse.urlencode(info).encode('utf-8')         #将信息编码成urllib能够识别的类型,注意的是python2.7用的ASCII编码,python3.X要UTF8转码 
                    response = urllib.request.urlopen(test_payorder.url,postdata).read()          #服务器响应的字符串消息
                    response_dict = eval(response);                                 #转换成字典后的消息
                    print(response_dict);
                    self.assertEqual(response_dict['code'], eval(row['code']))      #IOS内购获取订单号接口模块---您看到此信息,代表当行测试数据未通过---  
        print("----------------------------------------------------------------------------------------------------------------------")
        print(response_dict['data'])
        print("----------------------------------------------------------------------------------------------------------------------")
'''
unittest.main(),固定格式,用于默认调用unittest模块
'''
if __name__ == '__main__':
    log_file = 'log/log_%s.txt'%time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime())#定义log路径及文件名
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)
    f.close()
