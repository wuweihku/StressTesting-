# -*- coding: utf8 -*-
import urllib.parse                                                    # 这里urllib.parse要精确到子模块,否则会报错
import urllib.request                                                  # 这里urllib.request要精确到子模块,否则会报错
import csv                                                             # 支持csv
import time                                                            # 支持时间戳
import hashlib                                                         # 支持MD5加密

'''
MakeUser类:
makeuser()函数用于请求register-new接口，批量获取用户帐号

'''
class MakeUser():
    url='http://passportapi.qa.15166.com/register-new'                 # 通用注册接口
    info = {                                                           # register-new接口参数表
            'action':'generalRegister',
            'appId':'1105260003',
            'username':'',
            'password':'89ccb9722cde003d4021bc52314337f7',
            'channel':'1003',
            'signature':''
           }
    appKey = 'ab48563cf0e3dca2239dc69ed763726a'

    def makeuser(self,normal_case = True):
        global Totalcounts                                             # 记录一共获取了多少用户帐号
        Totalcounts += 1
        count = Totalcounts                 
        data = self.info                                               # 传入参数字典default_info
        username = 'test'+str(int(time.time()))+'count'+str(count)     # 生成用户名

        if normal_case:                                                # 正常情况生成用户帐号
            data['username'] = username                                # 补全当条请求字典

        sign = hashlib.md5()                                           # 生成signature
        sign_data = data['appId']+data['username']+data['password']+data['channel']+self.appKey    # 按文档要求加密
        sign.update(sign_data.encode('utf-8'))
        sign_md5_data = sign.hexdigest()
        data['signature'] = sign_md5_data                              # 补全当条请求字典

        postdata = urllib.parse.urlencode(data).encode('utf-8')        # 将信息编码成urllib能够识别的类型,注意的是python2.7用的ASCII编码,python3.X要UTF8转码 
        response = urllib.request.urlopen(self.url, postdata).read()   # 服务器响应的字符串消息
        response_dict = eval(response);                                # json转换成字典
        print(response_dict)

        extension=''
        extension='{"uid":'+str(response_dict['data']['uid'])+',"acessToken":"'+response_dict['data']['accessToken']+'"}'

        f=open('csv/make_user.csv','a+')                               # 写入csv
        f.write(str(response_dict['data']),'\n')
        f.close()
    
        f=open('csv/make_extension.csv','a+')                          # 写入csv
        f.write(str(extension),'\n')
        f.close()

if __name__ == '__main__':                                             # 如果从shell用python执行脚本
    usernum = 2000                                                     # 需要多少帐号
    producer = MakeUser()
    global Totalcounts
    Totalcounts = 0

    for i in range(usernum):
        producer.makeuser()
        print('正在生成第 %d 条用户帐号' %i)

