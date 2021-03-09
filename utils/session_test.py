#coding:utf-8

import uuid
import logging
import json
import config
class Session(object):
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.session_id = self.request_handler.get_secure_cookie("session_id")
        if not self.session_id:
            # 用户第一次访问
            self.session_id = uuid.uuid4().get_hex()
            self.data = {

            }
        else:
            # 拿到了session——id.去redis取数据
            try:
                data = self.redis.get("sess_%s"%self.session_id)
            except Exception as e:
                # 没有这条数据会报错并将data置为空
                logging.error(e)
                self.data = {}
            # 这里是查处的数据过期了，也将其置为空
            if not self.data:
                self.data = {}
            else:
                self.data = json.loads(data)
    # 将数据保存在redis中
    def save(self):
        json_data = json.dumps(self.data)
        try:
            self.redis.setex("sess_%s"%self.session_id,config.session_expier_seconds,json_data)
        except Exception as e:
            logging.error(e)
            raise Exception("save session failed")
        else:
            self.request_handler.set_secure_cookie("session_id",self.session_id)

    # 当注销时，将数据清除
    def clear(self):
        self.request_handler.clear_cookie("session_id")
        try:
            self.redis.delete("sess_%s"%self.session_id)
        except Exception as e:
            logging.error(e)


