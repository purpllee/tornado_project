#coding:utf-8
import os
#Application配置参数
setting=dict(
    static_path=os.path.join(os.path.dirname(__file__),"static"),
    template_path=os.path.join(os.path.dirname(__file__),"template"),
    cookie_secret="djasjkdjaskdnaskdna",
    xsrf_token=True,
    debug= True,
)

# mysql
mysql_options=dict(
    host="127.0.0.1",
    database = "ihome",
    user= "root",
    password="123456"
)

redis_options=dict(
    host="127.0.0.1",
    port = 6379,
)

log_file = os.path.join(os.path.dirname(__file__),"logs/log.txt")
log_level = "warning"
# session数据在redis有效期
session_expier_seconds = 36400
# 存入mysql数据库加密时需要一个混淆字段
passwd_hash_key = "lhy_passwd"