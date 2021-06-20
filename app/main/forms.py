from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField,SubmitField)
from wtforms.validators import Required

class BlogForm(FlaskForm):
    title = StringField("Blog title:", validators=[Required()])
    blog = TextAreaField("Type:", validators=[Required()])
    submit = SubmitField("Post")

class UpdateBlogForm(FlaskForm):
    title = StringField("Blog title", validators=[Required()])
    blog = TextAreaField("Type", validators=[Required()])
    submit = SubmitField("Update")

class CommentForm(FlaskForm):
    comment = TextAreaField("Post Comment", validators=[Required()])
    nicname= StringField("Comment Alias")
    submit = SubmitField("Comment")

class UpdateProfile(FlaskForm):
    first_name = StringField("First name")
    last_name = StringField("Last Name")
    bio = TextAreaField("Biography")
    email = StringField("Email")    
    submit = SubmitField("Update")