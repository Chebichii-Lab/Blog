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
        new_sub = Subscriber(email = request.form.get("subscriber"))
        db.session.add(new_sub)
        db.session.commit()
        mail_message("Thank you for subscribing to BLOG IT!", "email/welcome", new_sub.email)
    return render_template("index.html",blogs= blogs,quote = quote)


@main.route("/blog/<int:id>", methods = ["POST", "GET"])
def blog(id):
    blog = Blog.query.filter_by(id = id).first()
    comments = Comment.query.filter_by(blog_id = id).all()
    comment_form = CommentForm()
    comment_count = len(comments)

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        comment_form.comment.data = ""
        comment_alias = comment_form.alias.data
        comment_form.alias.data = ""
        if current_user.is_authenticated:
            comment_alias = current_user.username
        new_comment = Comment(comment = comment, comment_at = datetime.now(),comment_by = comment_alias, blog_id = id)
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
        blog.post_title = edit_form.title.data
        edit_form.title.data = ""
        blog.post_content = edit_form.post.data
        edit_form.post.data = ""

        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("main.blog", id = blog.id))

    return render_template("change_blog.html", blog = blog,edit_form = edit_form)