from flask import request, jsonify
from flask import redirect, url_for
from flask import Blueprint, render_template
from flask import flash
from config.config import ROOT
import json
import os
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from db.user import User
from db.db import db
from db.blog import Blog


BLOG_PATH = os.path.join(ROOT, 'blogs')
BLOG_IMG_DIR = os.path.join(BLOG_PATH, 'static')
BLOG_TMPLT_DIR = os.path.join(BLOG_PATH, 'templates')

blueprint = Blueprint('blog', __name__,
                      template_folder='../blogs/templates',
                      static_url_path='/static/blog',
                      static_folder='../blogs/static')


@blueprint.route('/blog', methods=['GET'])
def blog():
    blogs = Blog.query.order_by(Blog.publish_date.desc()).all()
    ## Delete the testing junk
    #db.session.query(Blog).delete()
    #db.session.commit()
    return render_template('blog.html', title='Blog', blogs=blogs)

@blueprint.route('/blog/<path>', methods=['GET'])
def blog_read_more(path):
    blog = Blog.query.filter_by(title=path).first()

    return render_template(f'{blog.title}.html', title=blog)

@blueprint.route('/blog/write', methods=['GET', 'POST'])
@login_required
def blog_write():
    if not current_user.name == 'coboaccess':
        return redirect('/blog')
    if request.method == 'POST':
        title = request.form.get('title')
        title =title.replace(' ','-')
        html = request.form.get('html')
        text = request.form.get('text')
        try:
            text = text[:300]
        except:
            pass
        if title == 'Title' or title == '':
            print('Title is invalid')
            return redirect('/blog')
        start_html = "{% extends 'blog-base.html' %} {% block inner_content %}"
        end_html = "{% endblock %}"
        dir_img_path = os.path.join(BLOG_IMG_DIR, title)
        if not os.path.exists(dir_img_path):
            os.makedirs(dir_img_path)
        try:
            for key in request.files:
                image = request.files.get(key)
                image.save(dir_img_path+'/'+image.filename)
            with open(BLOG_TMPLT_DIR + '/' + f'{title}.html', 'w') as file:
                file.write(start_html + html + end_html)
        except Exception as e:
            print(e)
        db_entry = Blog(
            title = title,
            text = text
        )
        db.session.add(db_entry)
        db.session.commit()
        flash('Blog entry submitted.', category='success')
            
    return render_template('blog-write.html', title='Blog')


