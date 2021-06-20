from flask import (render_template, request, redirect, url_for, abort)
from . import main
from ..models import User, Comment, Blog, Subscriber
from flask_login import login_required, current_user
from .forms import (UpdateProfile, BlogForm, CommentForm, UpdateBlogForm)
from datetime import datetime
from .. import db
from ..requests import get_quote
from ..email import mail_message

@main.route("/", methods = ["GET", "POST"])
def index():
    blogs = Blog.get_all_blogs()
    quote = get_quote()

    if request.method == "POST":
        new_subscriber = Subscriber(email = request.form.get("subscriber"))
        db.session.add(new_subscriber)
        db.session.commit()
        mail_message("Thank you for subscribing to BLOG IT!", "email/welcome", new_subscriber.email)
    return render_template("index.html",blogs= blogs,quote = quote)


@main.route("/blog/<int:id>", methods = ["POST", "GET"])
def make_comment(id):
    blog = Blog.query.filter_by(id = id).first()
    comments = Comment.query.filter_by(blog_id = id).all()
    comment_form = CommentForm()
    comment_count = len(comments)

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        comment_form.comment.data = ""
        comment_nicname = comment_form.nicname.data
        comment_form.nicname.data = ""
        if current_user.is_authenticated:
            comment_nicname = current_user.username
        new_comment = Comment(comment = comment, comment_at = datetime.now(),comment_by = comment_nicname, blog_id = id)
        new_comment.save_comment()
        return redirect(url_for("main.blog", id = blog.id))

    return render_template("blog.html",blog = blog,comments = comments,comment_form = comment_form,comment_count = comment_count)


@main.route("/blog/<int:id>/<int:comment_id>/delete")
def delete_comment(id, comment_id):
    blog = Blog.query.filter_by(id = id).first()
    comment = Comment.query.filter_by(id = comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("main.blog", id = blog.id))


@main.route("/blog/<int:id>/update", methods = ["POST", "GET"])
@login_required
def change_blog(id):
    blog = Blog.query.filter_by(id = id).first()
    edit_form = UpdateBlogForm()

    if edit_form.validate_on_submit():
        blog.blog_title = edit_form.title.data
        edit_form.title.data = ""
        blog.blog_content = edit_form.blog.data
        edit_form.blog.data = ""

        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("main.blog", id = blog.id))

    return render_template("change_blog.html", blog = blog,edit_form = edit_form)


@main.route("/blog/new", methods = ["POST", "GET"])
@login_required
def new_blog():
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        blog_title = blog_form.title.data
        blog_form.title.data = ""
        blog_content= blog_form.blog.data
        blog_form.blog.data = ""
        new_blog = Blog(blog_title = blog_title,blog_content = blog_content,posted_at = datetime.now(),blog_by = current_user.username,user_id = current_user.id)
        new_blog.save_blog()
        subscriber = Subscriber.query.all()
        for subscriber in subscriber:
            # notification_message(blog_title, 
            #                 "email/notification", subscriber.email, new_blog = new_blog)
            pass
        return redirect(url_for("main.blog", id = new_blog.id))
    
    return render_template("new_blog.html",blog_form = blog_form)


@main.route("/profile/<int:id>/<int:blog_id>/delete")
@login_required
def delete_blog(id, blog_id):
    user = User.query.filter_by(id = id).first()
    blog = Blog.query.filter_by(id = blog_id).first()
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for("main.profile", id = user.id))