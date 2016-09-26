# -*- coding: utf-8 -*-
import unittest                                         #支持python单元测试模块
import urllib.parse                                     #这里urllib.parse要精确到子模块,否则会报错
import urllib.request                                   #这里urllib.request要精确到子模块,否则会报错
import csv                                              #支持csv
import time                                             #支持时间戳
import hashlib                                          #支持MD5加密
import queue                                            #支持队列，python3中用小写queue
import threading                                        #支持多线程

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
            reader = csv.DictReader(csvfile,skipinitialspace=True)            #创建文件流对象,skipinitialspace忽略逗号后的空格，支持extension
            totalnum = 0                                #计算一共跑了多少条测试数据
            for row in reader:                          #这里的row对应csv表里的一行数据,第一行数据自动作为字段名,第二行数据开始作为测试实例
                totalnum += 1
                with self.subTest(row=row):             #row=i,会报错row is not defined,必须用row=row(这里用的是subTest功能)
                    print('正在执行第 %d 条测试数据'% totalnum)     #每跑一条数据,显示一次当前进度
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
                    
                    postdata = urllib.parse.urlencode(info).encode('utf-8')         #将信息编码成urllib能够识别的类型,注意的是python2.7用的ASCII编码,python3.X要UTF8转码 
                    response = urllib.request.urlopen(test_payorder.url,postdata).read()          #服务器响应的字符串消息
                    response_dict = eval(response);                                 #转换成字典后的消息
                    self.assertEqual(response_dict['code'], eval(row['code']))      #IOS内购获取订单号接口模块---您看到此信息,代表当行测试数据未通过---  

'''
Python的Queue模块中提供了同步的、线程安全的队列类

'''
class myThread(threading.Thread):           #使用Threading模块创建线程，直接从threading.Thread继承，然后重写__init__方法和run方法：
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = 'Thread-%s'%name
        self.q = q
    def run(self):
        print('Starting ' + self.name)
        process_data(self.name, self.q)
        print('Exiting ' + self.name)

'''
unittest.main(),固定格式,用于默认调用unittest模块
'''
if __name__ == '__main__':

    exitFlag = 0 

# 定义线程内部run()函数
    def process_data(threadName, q):
        while not exitFlag:
            queueLock.acquire()             #获得锁，成功获得锁定后返回True,可选的timeout参数不填时将一直阻塞直到获得锁定,否则超时后将返回False
            if not workQueue.empty():
                data = q.get()
                queueLock.release()         #释放锁
                print('%s processing %s' % (threadName, data))
            else:
                queueLock.release()
            time.sleep(1)

    threadList = list(range(1, 3))         #起多少个线程
    nameList = ["One", "Two", "Three", "Four", "Five"]
    queueLock = threading.Lock()            #创建线程锁
    workQueue = queue.Queue(30)             #创建队列
    threads = []                            #线程列表
    threadID = 1

# 创建新线程
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)   #起线程
        thread.start()
        threads.append(thread)              #将线程都加到线程列表
        threadID += 1

# 填充队列
    queueLock.acquire()
    while not workQueue.full():
        for word in nameList:
            workQueue.put(word)                 #将nameList列表里的元素放进队列
    queueLock.release()

# 等待队列清空
    while not workQueue.empty():
        pass

# 通知线程是时候退出
    exitFlag = 1

# 等待所有线程完成
    for t in threads:
        t.join()    # 等待至线程中止.这阻塞调用线程直至线程的join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生.
    print('Exiting Main Thread')















