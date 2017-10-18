import json
import os
import time
import hashlib
from datetime import datetime
from flask import render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import console
from .. import photos, db
from config import Config
from ..models import FlaskyArticles, FlaskyConfigs


# 后台首页
@console.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('console/index.html')


# 文章列表页
@console.route('/article', methods=['GET'])
@login_required
def article_index():
    return render_template('console/article/index.html')


# 文章列表数据接口
@console.route('/article/list', methods=['GET'])
@login_required
def article_list():
    page = request.args.get('page', type=int, default=1)
    limit = request.args.get('limit', type=int, default=10)
    articles = FlaskyArticles.query.filter_by(drafted=False).paginate(
        page, limit, False).items
    count = FlaskyArticles.query.count()
    return jsonify({
        'code': 0,
        'msg': 'success',
        'count': count,
        'data': [article.to_json() for article in articles]
    })


# 文章图片素材上传接口
@console.route('/article/upload', methods=['POST'])
@login_required
def article_upload():
    data = []
    folder = datetime.now().strftime('%Y-%m-%d')
    dest_folder = Config.UPLOADED_PHOTOS_DEST + folder
    if 'photos' in request.files:
        for filename in request.files.getlist('photos'):
            hash_name = hashlib.md5(
                current_user.username.encode('utf-8') +
                str(time.time()).encode('utf-8')).hexdigest()[:15]
            if not os.path.isdir(dest_folder):
                os.makedirs(dest_folder)
            dest_name = photos.save(
                filename, folder=folder, name=hash_name + '.')
            data.append(photos.url(dest_name))
        return json.dumps({'errno': 0, 'data': data})
    return json.dumps({'errno': -1, 'data': data})


# 文章新增视图
@console.route('/article/new', methods=['GET', 'POST'])
@login_required
def article_create():
    if request.method == 'GET':
        return render_template('console/article/create.html')
    else:
        param = request.form.get('param', type=str, default=None)
        if param == 'publish':
            article = FlaskyArticles(
                title=request.form.get('title'),
                content=request.form.get('content').encode('utf-8'),
                published_at=datetime.utcnow())
        else:
            article = FlaskyArticles(
                title=request.form.get('title'),
                content=request.form.get('content'))
        db.session.add(article)
        db.session.commit()
        flash('文章创建成功')
        return json.dumps({'ret_code': 0, 'ret_msg': 'success'})


# 文章修改视图
@console.route('/article/show/<int:id>', methods=['GET'])
@login_required
def article_show(id):
    article = FlaskyArticles.query.get_or_404(id)
    return render_template('console/article/show.html', article=article)


# 文章更新接口
@console.route('/article/update', methods=['POST'])
@login_required
def article_update():
    id = request.form.get('id', type=int, default=None)
    article = FlaskyArticles.query.get_or_404(id)
    if article is None:
        return json.dumps({'ret_code': -1, 'ret_msg': 'fail'})
    param = request.form.get('param', type=str, default=None)
    article.title = request.form.get('title')
    article.content = request.form.get('content').encode('utf-8')
    article.updated_at = datetime.utcnow()
    if param == 'publish':
        article.published_at = datetime.utcnow()
    db.session.add(article)
    db.session.commit()
    flash('文章修改成功')
    return json.dumps({'ret_code': 0, 'ret_msg': 'success'})


# 文章删除接口
@console.route('/article/delete', methods=['POST'])
@login_required
def article_delete():
    id = request.form.get('id')
    article = FlaskyArticles.query.filter_by(id=id).first()
    if article is None:
        return jsonify({'ret_code': -1, 'ret_msg': 'faield'})
    article.drafted = True
    article.updated_at = datetime.utcnow()
    db.session.add(article)
    db.session.commit()
    return jsonify({'ret_code': 0, 'ret_msg': 'success'})


# 素材首页
@console.route('/material')
@login_required
def material_index():
    return render_template('console/material/index.html')


# 个人中心首页
@console.route('/my', methods=['GET', 'POST'])
@login_required
def my():
    if request.method == 'GET':
        return render_template('console/my/index.html')
    else:
        return json.dumps({'ret_code':0, 'ret_msg': 'success'})
