# -*- coding:utf8 -*-

from utils.tool import logger, mysql, today
from flask import request
from flask_restful import Resource

class Misc(Resource):

    def post(self):
        res    = {"url": request.url, "msg": None, "success": False, "code": 0}
        blogId = request.args.get("blogId")
        action = request.args.get("action")
        value  = request.args.get("value", "true")
        logger.info("blogId: %s, action: %s, value: %s" %(blogId, action, value) )

        #check params
        if not value in ("true", "True", True, "false", "False", False):
            res.update(msg="illegal parameter value", code=-1)
        try:
            blogId = int(blogId)
        except:
            res.update(msg="illegal parameter blogId", code=-1)
        if not action in ("recommend", "top"):
            res.update(msg="illegal parameter action", code=-1)
        if res['msg']:
            logger.info(res)
            return res

        try:
            sql = "UPDATE blog SET update_time='%s',%s='%s' WHERE id=%d" %(today(), action, value, blogId)
            logger.info(sql)
            mysql.update(sql)
        except Exception,e:
            logger.error(e, exc_info=True)
            res.update(success=False)
        else:
            res.update(success=True)

        logger.info(res)
        return res