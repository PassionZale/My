from flask import render_template, session, redirect, url_for, request, jsonify
from flask_login import login_required
from . import main
from ..models import FlaskyArticles


@main.route('/', methods=['GET'])
def index():
    page = request.args.get('page', type=int, default=1)
    limit = request.args.get('limit', type=int, default=5)
    pagination = FlaskyArticles.query.order_by(
        FlaskyArticles.published_at.desc()).filter_by(drafted=False).paginate(
            page, limit, False)
    articles = pagination.items
    return render_template('main/index.html', articles=articles, pagination=pagination)


@main.route('/article/<int:id>', methods=['GET'])
def article(id):
    article = FlaskyArticles.query.get_or_404(id)
    return render_template('main/article.html', article=article)
