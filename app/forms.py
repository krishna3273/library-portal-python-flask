from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Books

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    subject=StringField('Subject')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AddBook(FlaskForm):
    book = TextAreaField('Book Name', validators=[DataRequired(), Length(min=1, max=400)])
    author =  StringField('Author Name', validators=[DataRequired()])
    btype=StringField('Book Type',validators=[DataRequired()])
    submit = SubmitField('Submit')
    img = TextAreaField('Image', validators=[DataRequired()])

    def validate_book(self, book):
        book = Books.query.filter_by(book_name=book.data).first()
        if book is not None:
            raise ValidationError('Book already present')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField("Search")

class BookIssue(FlaskForm):
    issuer = StringField('Issuer', validators=[DataRequired()])
    book_issued = TextAreaField('Book Issued', validators=[DataRequired(), Length(min=1, max=400)])
    submit = SubmitField("Search")
    user_reg = False
    def validate_book_issued(self, book_issued):
        book = Books.query.filter_by(book_name=book_issued.data).first()
        if book is None:
            raise ValidationError('Book not present')

    def validate_issuer(self, issuer):
        user = User.query.filter_by(username=issuer.data).first()
        if user is None:
            raise ValidationError('User not registered to portal')

class SendForm(FlaskForm):
    #text=TextAreaField('Text',validators=[DataRequired(),Length(min=1,max=200)])
    reciever=StringField('reciever')
    submit=SubmitField("send")

    def validate_reciever(self, reciever):
        user = User.query.filter_by(username=reciever.data).first()
        if user is None:
            raise ValidationError('User not present')

class ForgotForm(FlaskForm):
    username=StringField('username')
    submit=SubmitField("send")
class VerificationForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password')])
    confirm=StringField("confirm")