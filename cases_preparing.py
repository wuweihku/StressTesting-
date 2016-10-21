# -*- coding: utf-8 -*-
import csv
import hashlib 
import threading
import time

'''
test_payorder.py用来执行cases
cases_preparing.py用来准备cases

'''
case = {
        'action': 'getOrderID',
        'userID': '',                           # 要先从http://passportapi.qa.15166.com/register-new生成make_user.csv，对应uid
        'username':'',                          # 要先从http://passportapi.qa.15166.com/register-new生成make_user.csv，对应username
        'appID':'1105260003',
        'roleID':'',                            # case['roleID']=str(num)+str(info['uid']),也是需要make_user.csv
        'roleName':'testcase',
        'roleLevel':'1',
        'serverID':'1',
        'serverName':'a',
        'accessToken':'',
        'payChannel':'ios',
        'money':'100',
        'coin':'100',
        'currency':'RMB',
        'productID':'1',
        'productName':'testproduct',
        'productDesc':'testproduct',
        'sdkVersion':'v1.1.0',
        'device':'Ali_Debian',
        'osVersion':'Debian',
        'imei':'352024071820819',
        'mac':'54:4E:90:BD:7B:8F',
        'sdkExtension':'',                      # case['sdkExtension']='{"rand":"'+str(int(time.time()))+'"}
        'packageVersion':'1.0',
        'extension':'',                         # case['extension']=extension_t
        'cpOrderID':'',                         # case['cpOrderID']=str(num)+str(info['uid'])，也是需要make_user.csv
        'signType':'RSA',
        'signature':'',                         # 本地加密
        'code':''                               # 断言码
       }

num=int(time.time())
