# -*-coding:utf-8-*- 
# 作者：   29511
# 文件名:  get_hash.py
# 当前系统日期时间：2019/12/7，10:02 
import hashlib


# 密码加密
def get_hash(str):
    # 取一个字符串的hash值
    sh = hashlib.sha1()  # 40位16进制
    # sh = hashlib.md5()  # 32位16进制
    sh.update(str.encode('utf8'))
    return sh.hexdigest()
