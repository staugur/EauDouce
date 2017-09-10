# -*- coding: utf-8 -*-
"""
    EauDouce.views.upload
    ~~~~~~~~~~~~~~

    File upload view.

    :copyright: (c) 2017 by Mr.tao.
    :license: MIT, see LICENSE for more details.
"""

import os, base64
from utils.tool import logger, gen_rnd_filename, UploadImage2Upyun
from flask import Blueprint, request, Response, url_for, redirect, g, jsonify
from werkzeug import secure_filename
from config import PLUGINS
from thirds.binbase64 import base64str

upload_blueprint = Blueprint("upload", __name__)
#文件上传文件夹, 相对于项目根目录, 请勿改动static/部分
IMAGE_FOLDER     = 'static/img/upload/'
UPLOAD_FOLDER    = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), IMAGE_FOLDER)

#文件名合法性验证
allowed_file = lambda filename: '.' in filename and filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg', 'gif'])

#对博客图片上传进行响应
@upload_blueprint.route("/BlogImage/", methods=["POST",])
def UploadBlogImage():
    editorType = request.args.get("editorType", "wangEditor")
    logger.sys.debug(request.files)
    f = request.files.get("WriteBlogImage") or request.files.get("editormd-image-file")
    if f and allowed_file(f.filename):
        filename = secure_filename(gen_rnd_filename() + "." + f.filename.split('.')[-1]) #随机命名
        if PLUGINS['UpYunStorage']['enable'] in ('true', 'True', True):
            imgUrl = "/EauDouce/blog/" + filename
            upres  = UploadImage2Upyun(imgUrl, f.stream.read())
            imgUrl = PLUGINS['UpYunStorage']['dn'].strip("/") + imgUrl
            logger.sys.info("Blog to Upyun file saved, its url is %s, result is %s" %(imgUrl, upres))
        else:
            if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            imgUrl = request.url_root + IMAGE_FOLDER + filename
            logger.sys.info("Blog to local file saved in %s, its url is %s" %(UPLOAD_FOLDER, imgUrl))
        #返回数据加上自定义头
        if editorType == "wangEditor":
            res = Response(imgUrl)
            res.headers["ContentType"] = "text/html"
        else:
            res = jsonify(url=imgUrl, message=None, success=1)
            res.headers["ContentType"] = "application/json"
    else:
        result = r"error|未成功获取文件或格式不允许，上传失败"
        if editorType == "wangEditor":
            res = Response(result)
            res.headers["ContentType"] = "text/html"
        else:
            res = jsonify(message=result, success=0)
            res.headers["ContentType"] = "application/json"
    res.headers["Charset"] = "utf-8"
    return res

#对头像图片上传进行响应
@upload_blueprint.route('/avatar/', methods=['POST','OPTIONS'])
def UploadAvatarImage():
    logger.sys.debug(request.files)
    f = request.files.get('file')
    # Check if the file is one of the allowed types/extensions
    if f and allowed_file(f.filename):
        filename = secure_filename(gen_rnd_filename() + "." + f.filename.split('.')[-1]) #随机命名
        if PLUGINS['UpYunStorage']['enable'] in ('true', 'True', True):
            imgUrl = "/EauDouce/avatar/" + filename
            upres  = UploadImage2Upyun(imgUrl, f.stream.read())
            imgUrl = PLUGINS['UpYunStorage']['dn'].strip("/") + imgUrl
            logger.sys.info("Avatar to Upyun file saved, its url is %s, result is %s" %(imgUrl, upres))
        else:
            if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            imgUrl = "/" + IMAGE_FOLDER + filename
            logger.sys.info("Avatar to local file saved in %s, its url is %s" %(UPLOAD_FOLDER, imgUrl))
        # return user home and write avatar url into mysql db.
        res = g.api.user_update_avatar(g.username, imgUrl)
    else:
        res = {"success": False, "msg": u"上传失败: 未成功获取文件或格式不允许"}

    logger.sys.info(res)
    return jsonify(res)

#对封面图片上传进行响应
@upload_blueprint.route('/cover/', methods=['POST','OPTIONS'])
def UploadCoverImage():
    logger.sys.debug(request.files)
    f = request.files.get('file')
    # Check if the file is one of the allowed types/extensions
    if f and allowed_file(f.filename):
        filename = secure_filename(gen_rnd_filename() + "." + f.filename.split('.')[-1]) #随机命名
        if PLUGINS['UpYunStorage']['enable'] in ('true', 'True', True):
            imgUrl = "/EauDouce/cover/" + filename
            upres  = UploadImage2Upyun(imgUrl, f.stream.read())
            imgUrl = PLUGINS['UpYunStorage']['dn'].strip("/") + imgUrl
            logger.sys.info("Cover to Upyun file saved, its url is %s, result is %s" %(imgUrl, upres))
        else:
            if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            imgUrl = "/" + IMAGE_FOLDER + filename
            logger.sys.info("Cover to local file saved in %s, its url is %s" %(UPLOAD_FOLDER, imgUrl))
        # return user home and write avatar url into mysql db.
        res = g.api.user_update_cover(g.username, imgUrl)
    else:
        res = {"success": False, "msg": u"上传失败: 未成功获取文件或格式不允许"}

    logger.sys.info(res)
    return jsonify(res)

#对头像图片裁剪后上传进行响应
@upload_blueprint.route('/clipper/', methods=['POST','OPTIONS'])
def UploadClipperAvatar():
    if request.form.get("action") == "add":
        data     = request.form.get("picStr")
        imgdata  = base64.b64decode(data)
        filename = gen_rnd_filename() + ".png" #随机命名
        if PLUGINS['UpYunStorage']['enable'] in ('true', 'True', True):
            imgUrl = "/EauDouce/avatar/" + filename
            upres  = UploadImage2Upyun(imgUrl, base64str(data))
            imgUrl = PLUGINS['UpYunStorage']['dn'].strip("/") + imgUrl
            logger.sys.info("Avatar to Upyun file saved, its url is %s, result is %s" %(imgUrl, upres))
        else:
            if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
            file=open(os.path.join(UPLOAD_FOLDER, filename), 'wb')
            file.write(imgdata)
            file.close()
            imgUrl = "/" + IMAGE_FOLDER + filename
            logger.sys.info("Avatar to local file saved in %s, its url is %s" %(UPLOAD_FOLDER, imgUrl))
        # return user home and write avatar url into mysql db.
        res = g.api.user_update_avatar(g.username, imgUrl)
    else:
        res = {"success": False, "msg": u"不支持的action"}

    logger.sys.info(res)
    return jsonify(res)
