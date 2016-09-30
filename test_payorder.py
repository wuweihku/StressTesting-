# -*- coding: utf-8 -*-
import urllib.parse                                     #这里urllib.parse要精确到子模块,否则会报错
import urllib.request                                   #这里urllib.request要精确到子模块,否则会报错
import csv                                              #支持csv
import time                                             #支持时间戳
import hashlib                                          #支持MD5加密
import queue                                            #支持队列，python3中用小写queue
import threading                                        #支持多线程

'''
TestAPI类:
__init__()构造函数
assertAPI()断言函数
test_payorder()测试payorder接口的函数

'''
class TestAPI():                                        
    def __init__(self, threadName, url, data):
        self.threadName = threadName                    #用以标识当前线程
        self.url = url                                  #接口地址
        self.data = data                                #队列里的一行case
        
    def assertAPI(self, res, esp):                      
        response = res                                  #返回的json转字典
        espect = esp                                    #队列里的一行case
        global Successed                                #标记成功次数
        global Failed                                   #标记失败次数

        if int(response['code']) == int(espect['code']):                          #断言成功
            Successed += 1

        if int(response['code']) != int(espect['code']):                          #断言失败
            Failed += 1
            print('-----------------\n\n','            Failed:  responsecode-> %s and espectcode-> %s, msg: %s '%(response['code'], espect['code'], response['msg']))
            
            print('%s Processing: '%self.threadName,    #输出当前哪个线程在处理队列中的哪条数据，设计成队列数据按顺序输出处理，由于涉及服务器响应，所以返回到sys.print出的可能不是按顺序，但是取出post的时候是按顺序的.
                  'action->%s'%self.data['action'],
                  'userID-> %s' %self.data['userID'], 
                  'username-> %s'%self.data['username'],
                  'roleID-> %s'%self.data['roleID'], 
                  'roleName-> %s'%self.data['roleName'],
                  '\n' )

    def test_payorder(self):                            #执行测试功能的函数                    
        global Totalcases                               #引用全局变量
        info = {'action': self.data['action'], 
            'userID': self.data['userID'], 
            'username':self.data['username'], 
            'appID':self.data['appID'],
            'roleID':self.data['roleID'],   
            'roleName':self.data['roleName'],
            'roleLevel':self.data['roleLevel'],
            'serverID':self.data['serverID'],
            'serverName':self.data['serverName'],
            'accessToken':self.data['accessToken'],
            'payChannel':self.data['payChannel'],
            'money':self.data['money'],
            'coin':self.data['coin'],
            'currency':self.data['currency'],
            'productID':self.data['productID'],
            'productName':self.data['productName'],
            'productDesc':self.data['productDesc'],
            'sdkVersion':self.data['sdkVersion'],
            'device':self.data['device'],
            'osVersion':self.data['osVersion'],
            'imei':self.data['imei'],
            'mac':self.data['mac'],
            'sdkExtension':self.data['sdkExtension'],
            'packageVersion':self.data['packageVersion'],
            'extension':self.data['extension'],
            'cpOrderID':self.data['cpOrderID'],
            'signType':self.data['signType'],
            'signature':self.data['signature']
               }                                        #csv里的每一行测试实例，这里不用过滤空值，空值可以作为测试用例，引发异常. 注意：为了保证压测性能，这里的每一次读取，应该都是完备的数据，不需要额外处理.
                    
      
        Totalcases += 1                                                             #Totalcases计数+1
        postdata = urllib.parse.urlencode(info).encode('utf-8')                     #将信息编码成urllib能够识别的类型,注意的是python2.7用的ASCII编码,python3.X要UTF8转码 
        response = urllib.request.urlopen(self.url, postdata).read()                #服务器响应的字符串消息
        response_dict = eval(response);                                             #json转换成字典
        
        self.assertAPI(response_dict, self.data)        #断言

'''
Python的Queue模块中提供了同步的、线程安全的队列类

'''
class myThread(threading.Thread):                       #使用Threading模块创建线程，直接从threading.Thread继承，然后重写__init__方法和run方法：
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID                        #线程ID
        self.name = 'Thread-%s'%name                    #线程名
        self.q = q                                      #队列对象传入
    def run(self):
        print('Starting ' + self.name)
        process_data(self.name, self.q)                 #线程业务函数
        print('Exiting ' + self.name)


if __name__ == '__main__':                              #如果从shell用python执行脚本

    '''
    IOS内购获取订单号接口
    接口说明：返回一个唯一订单号（奥飞生成）
    请求方式：POST
    测试地址：http://payapi.qa.15166.com/pay/order

    '''
    url = 'http://payapi.qa.15166.com/pay/order'        #所要访问的url,一个测试类对应一个url

    totalthreads = 2                                    #起多少个线程，思想就是一开始就起好所有需要的线程
    casesnum = 10                                       #思想就是一开始就将所有需要的cases准备进队列                               
    duration = 3                                        #单次并发的duration

    global Totalcases                                   #记录一共跑了多少cases
    global Successed                                    #成功cases数
    global Failed                                       #失败cases数
    Totalcases = 0
    Successed = 0
    Failed = 0
    timestart  = time.time()                            #开始时间戳

    exitFlag = 0 
    caseFlag = list(range(1,casesnum+1))                #用来标记workQueue.qsize()==(totalthreads+1）的情况

# 定义线程内部run()函数
    def process_data(threadName, q):
        while not exitFlag:
            queueLock.acquire()                         #获得锁，成功获得锁定后返回True,可选的timeout参数不填时将一直阻塞直到获得锁定,否则超时后将返回False
            if not workQueue.empty():
                print('current case: %s'%(casesnum-workQueue.qsize()+1))            #显示当前队列case进度

                if workQueue.qsize() in caseFlag[::totalthreads]:                   #控制请求节奏，每隔totalthreads个请求则暂停duration秒
                    print('current runround finished, %s seconds waiting for next new runround now.' %duration) 
                    time.sleep(duration)

                qdata = q.get()                         #qdata为一行队列数据
                queueLock.release()                     #释放锁
                
                # print('current case gotten: %s '%qdata['action'])                 #输出取得的cases，用以验证队列顺序输出

                threadtestapi = TestAPI(threadName, url, qdata)                     #构造TestAPI对象, qdata为每次传入的一行case
                threadtestapi.test_payorder()                                       #执行线程对象的测试函数
            else:
                queueLock.release()
            time.sleep(0.05)

    threadList = list(range(1, totalthreads+1))         #起多少个线程
    queueLock = threading.Lock()                        #创建线程锁
    workQueue = queue.Queue(casesnum)                   #创建队列,并设置队列长度，即所需要跑的case数
    threads = []                                        #线程列表
    threadID = 1

# 创建新线程，只负责起线程
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)                               #起线程,这里线程对象一创建，就会自动调用线程对象里的run（）函数. 所以在这里用time.sleep（）控制线程节奏，几轮，一轮多少并发.
        thread.start() 
        threads.append(thread)                                                      #将线程都加到线程列表
        threadID += 1

# 填充队列,在这里先把csv里的case都读取进队列
    queueLock.acquire()
    while not workQueue.full():                         #最终的限定是，case堆满队列
        with open('csv/payorder_data.csv') as csvfile:  #打开csv文件流
            reader = csv.DictReader(csvfile,skipinitialspace=True)            #创建文件流对象,skipinitialspace忽略逗号后的空格，支持extension
            totalnum = 0                                #计算一共加了多少条测试数据进队列
            for row in reader:                          #这里的row对应csv表里的一行数据,第一行数据自动作为字段名,第二行数据开始作为测试实例. 而且，这是一个for循环，只有当reader句柄对象都读完了，才会结束循环
                totalnum += 1                           #如果不判断队列是否已满，则此for循环与外围while循环互相作用，形成死循环，永远无法完成最后一次put
                workQueue.put(row)                      #将csv里的row放进队列
                if workQueue.full():                    #队列塞满时，跳出for循环
                    break
    print("%d Testcases Ready "%workQueue.qsize())
    queueLock.release()                                 #这里锁一旦释放，线程就开始执行各自的run（）函数了 
    
# 等待队列清空
    while not workQueue.empty():                        #当cases队列为空时，结束此循环，进入下一步
        pass

# 通知线程是时候退出
    exitFlag = 1

# 等待所有线程完成
    for t in threads:                                   #起线程的时候，把线程都加进了threads列表里
        t.join()                                        #等待至线程中止.这阻塞调用线程直至线程的join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生.
    print('Exiting Main Thread')

# 测试报告
    timefinish = time.time()                            #结束时间戳
    timecost = timefinish-timestart
    print("--------------------\nTotalcases: %d \n"%Totalcases, "Successed: %d \n"%Successed, "   Failed: %d \n"%Failed)
    print('%s seconds cost for testing'%timecost)



    '''

    for runround in range(totalround):
        print('current runround: %s '%(runround+1))

        time.sleep(sleeptime)                                                       #一秒并发一次
    '''
