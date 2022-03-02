from wtforms import Form, StringField, PasswordField, validators


class RegisterForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25), validators.DataRequired()])

    email = StringField('email', [validators.Length(min=6, max=35), validators.DataRequired()])

    password = PasswordField(name='password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=6, message='Passwords must be at least 6 digits'),
    ])

    confirm = PasswordField(name='password2', validators=[
        validators.DataRequired(),
        validators.Length(min=6, message='Passwords must be at least 6 digits'),
    ])


class LoginForm(Form):
    username = StringField('username', [validators.Length(min=6, max=35), validators.DataRequired()])

    password = PasswordField('password', [
        validators.DataRequired(),
    ])


class PostForm(Form):
    title = StringField('title', [validators.Length(min=3, max=35), validators.DataRequired()])
    href = StringField('href')
    text = StringField('text', [validators.Length(min=10, max=500), validators.DataRequired()])


class CommentForm(Form):
    text = StringField('text', [validators.Length(min=10, max=500), validators.DataRequired()])
    pass


class ContactForm(Form):
    pass
