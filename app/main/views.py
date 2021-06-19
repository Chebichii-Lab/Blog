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