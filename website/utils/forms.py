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
    email = StringField('email', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])


class PostForm(Form):
    pass


class CommentForm(Form):
    pass


class ContactForm(Form):
    pass
