#coding:utf-8
import logging
import constant
import random
import re
from .BaseHandler import BaseHandlers
from utils.captcha.captcha import captcha
from utils.response_code import RET
from libs.yuntongxun.SendTemplateSMS import ccp

class ImageCodeHAndler(BaseHandlers):
    def get(self):
        pre_code_id = self.get_argument("pre","")
        code_id = self.get_argument("cur","")
        if pre_code_id:
            try:
                self.redis.delete("image_code_%s"%pre_code_id)
            except Exception as e:
                logging.error(e)
        name,text,image = captcha.generate_captcha()
        try:
            self.redis.setex("image_code_%s"%code_id,constant.IMAGE_CODE_EXPIRE_SECOND,text)
        except Exception as e:
            logging.error(e)
            self.set_header("Content-Type","image/jpg")
        self.write(image)

class PhoneCodeHandler(BaseHandlers):
    """手机验证码"""
    def post(self):
        # 获取参数
        mobile = self.json_args.get("mobile")
        piccode = self.json_args.get("piccode")
        piccode_id = self.json_args.get("piccode_id")
        if not all((mobile,piccode,piccode_id)):
            return self.write(dict(errcode=RET.PARAMERR,errmsg="参数不完整"))
        if not re.match(r"1\d{10}",mobile):
            return self.write(dict(errcode=RET.PARAMERR,errmsg="手机号错误"))
        # 判断图片验证码
        # try部分是查询是否存在这个验证码，若存在但是已过期，查询结果是None而不是错误
        try:
            real_image_code_text = self.redis.get("image_code_%s"%piccode_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR,errmsg="查询数据库错误"))
        if not real_image_code_text:
            return self.write(dict(errcode=RET.NODATA,errmsg="数据已过期"))
        if real_image_code_text.lower() != piccode.lower():
            return self.write(dict(errcode= RET.DATAERR,errmsg="验证码错误"))
        # 若验证通过则发送验证码,先随机生成验证码
        sms_code = "%04d"%random.randint(0,9999)
        try:
            self.redis.setex("sms_code_%s"%mobile,constant.SMS_CODE_EXPIRES_SECONDS,sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR,errmsg="生成验证码错误"))
        # 发短信
        try:
            ccp.sendTemplateSMS(mobile,[sms_code,constant.SMS_CODE_EXPIRES_SECONDS//60],1)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.THIRDERR,errmsg="发送失败"))
        self.write(dict(errcode=RET.OK,errmsg="ok"))
        # 不通过返回出错信息

