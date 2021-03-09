# coding:utf-8
import os
from handlers import VerifyCode,Passport
from handlers.BaseHandler import StaticFileHandler


handlers = [
    (r"/api/check_login", Passport.CheckLoginHandler), # 判断用户是否登录
    (r"/api/login", Passport.LoginHandler),
    (r"/api/register",Passport.RegisterHandler),
    (r"/api/imagecode", VerifyCode.ImageCodeHAndler),
    (r"/api/smscode", VerifyCode.PhoneCodeHandler),
    (r"/(.*)", StaticFileHandler,
     dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html")),
]
