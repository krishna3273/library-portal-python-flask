from flask import render_template, flash, redirect, url_for,session, request, redirect
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddBook, SearchForm, BookIssue, SendForm, ForgotForm, VerificationForm
from app.models import Books, User
from functools import wraps
from datetime import timedelta, datetime, date
from app.emails import send_email, send_email1
import random
import string

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
           return f(*args, **kwargs)
        else:
           flash("Can not  access secret_page without logging in")
           return redirect(url_for('login',next=request.path))
    return decorated_function

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))

@app.route("/forgot",methods=["GET","POST"])
def forgot():
    form=ForgotForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first_or_404()
        subject=random_string(10)
        user.random=subject
        username=user.username
        verify="/verify/"+username
        db.session.commit()
        send_email1(send_to=[user.email],user=user.username,subject=subject)
        return redirect(verify)
    return render_template("forgot.html",form=form)

@app.route("/verify/<username>",methods=["GET","POST"])
def verify(username):
    form=VerificationForm()
    if form.validate_on_submit():
        compare=form.confirm.data
        user=User.query.filter_by(username=username).first_or_404()
        actual=user.random
        if compare==actual:
            user.set_password(form.password.data)
            db.session.commit()
            return redirect(url_for("login"))
        return redirect(url_for("index"))
    return render_template("verify.html",form=form)

@app.route("/mail",methods=['GET','POST'])
@login_required
def email():
    if session["username"]!="admin":
        return redirect(url_for("index"))
    form=SendForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.reciever.data).first_or_404()
        books = User.query.get(user.id).books.all()
        send_email(book=books,send_to=[user.email],subject="test")
        return redirect(url_for('index_admin'))
    return render_template('email.html',form=form)

@app.route("/mail1",methods=['GET','POST'])
@login_required
def email1():
    if session["username"]!="admin":
        return redirect(url_for("index"))
    users=User.query.all()
    for user in users:
        books = User.query.get(user.id).books.all()
        present=date.today()
        for book in books:
            if present+timedelta(days=2)==book.due or present+timedelta(days=1)==book.due:  
                send_email(book=book,send_to=[user.email],subject="Submission date for this book is close, submit it soon to avoid fines.")
            if present==book.due :
                send_email(book=book,send_to=[user.email],subject="Today is the submission date, submit or re-issue to avoid fines.")
            if present>book.due:
                date_format = "%Y-%m-%d"
                a = datetime.strptime(str(present), date_format)
                b = datetime.strptime(str(book.due), date_format)
                delta = b - a  
                cost=(delta.days)*2
                subject="submission time exceeded.\
                You are due by"+str(delta.days)+"days,Rs."+str(cost)+"is the fine if you pay by today"
                send_email(book=book,send_to=[user.email],subject=subject)
    return redirect(url_for('index_admin'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<subject>',methods=["GET","POST"])
def index(subject=None):
    form = SearchForm()
    if form.validate_on_submit():
        books = Books.query.filter(Books.book_name.contains(form.search.data)).all()
        if subject=="managment":
            books = Books.query.filter(Books.book_name.contains(form.search.data)).filter_by(btype="Management").all()
        if subject=="biographies":
            books = Books.query.filter(Books.book_name.contains(form.search.data)).filter_by(btype="Biographies").all()
        if subject=="romance":
            books = Books.query.filter(Books.book_name.contains(form.search.data)).filter_by(btype="Romance").all()
        if subject=="scifi":
            books = Books.query.filter(Books.book_name.contains(form.search.data)).filter_by(btype="Science Fiction").all()
        if subject=="indian":
            books = Books.query.filter(Books.book_name.contains(form.search.data)).filter_by(btype="Indian Writing").all()
        return render_template('index.html', title='Home', books=books, form = form)
    books = Books.query.all()
    if subject=="managment":
        books = Books.query.filter_by(btype="Management").all()
    if subject=="biographies":
        books = Books.query.filter_by(btype="Biographies").all()
    if subject=="romance":
        books = Books.query.filter_by(btype="Romance").all()
    if subject=="scifi":
        books = Books.query.filter_by(btype="Science Fiction").all()
    if subject=="indian":
        books = Books.query.filter_by(btype="Indian Writing").all()
    return render_template('index.html', title='Home', books=books, form=form)

@app.route('/index_admin', methods=['GET', 'POST'])
@app.route('/index_admin/<subject>',methods=["GET","POST"])
def index_admin(subject=None):
    form = SearchForm()
    user = User.query.filter_by(username=session["username"]).first()
    occupation = user.occupation
    print occupation
    if form.validate_on_submit():
        books = Books.query.filter(Books.book_name.contains(form.search.data)).all()
        if subject=="managment":
            books = Books.query.filter(Books.book_name.contains(form.search.data)).filter_by(btype="Management").all()
        if subject=="biographies":
            books = Books.query.filter(Books.book_name.contains(form.search.data)).filter_by(btype="Biographies").all()
        if subject=="romance":
            books = Books.query.filter(Books.book_name.contains(form.search.data)).filter_by(btype="Romance").all()
        if subject=="scifi":
            books = Books.query.filter(Books.book_name.contains(form.search.data)).filter_by(btype="Science Fiction").all()
        if subject=="indian":
            books = Books.query.filter(Books.book_name.contains(form.search.data)).filter_by(btype="Indian Writing").all()
        return render_template('index_admin.html', title='Home', books=books, form = form,occupation=occupation)
    books = Books.query.all()
    if subject=="managment":
        books = Books.query.filter_by(btype="Management").all()
    if subject=="biographies":
        books = Books.query.filter_by(btype="Biographies").all()
    if subject=="romance":
        books = Books.query.filter_by(btype="Romance").all()
    if subject=="scifi":
        books = Books.query.filter_by(btype="Science Fiction").all()
    if subject=="indian":
        books = Books.query.filter_by(btype="Indian Writing").all()
    return render_template('index_admin.html', title='Home', books=books, form = form,occupation=occupation)

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    occupation=User.query.filter_by(username=session["username"]).first().occupation
    if session["username"]!="admin" and occupation!="faculty":
        return redirect(url_for("index"))
    form = AddBook()
    if form.validate_on_submit():
        book = Books(book_name = form.book.data, author = form.author.data,btype=form.btype.data,img=form.img.data)
        db.session.add(book)
        db.session.commit()
        flash('You have added the book!')
        return redirect(url_for('index_admin'))
    return render_template("add_book.html", title='Add a book', form=form)

@app.route('/issue_book', methods=['GET', 'POST'])
@login_required
def issue_book():
    if session["username"]!="admin":
        return redirect(url_for("index"))
    form = BookIssue()
    if form.validate_on_submit():
        issuer = User.query.filter_by(username = form.issuer.data).first()
        book =  Books.query.filter_by(book_name=form.book_issued.data).first()
        book.issued_by = issuer
        due_date = date.today() + timedelta(days=15)
        book.due=due_date
        db.session.commit()
        flash('Book issued!')
        return redirect(url_for('index_admin'))
    return render_template("issue_book.html", title='Issue a book', form=form,submit="issue")


@app.route("/return_book",methods=["GET","POST"])
@login_required
def return_book():
    if session["username"]!="admin":
        return redirect(url_for("index"))
    form=BookIssue()
    if form.validate_on_submit():
        issuer = User.query.filter_by(username = form.issuer.data).first()
        book =  Books.query.filter_by(book_name=form.book_issued.data).first()
        book.issued_by=None
        book.due=None
        db.session.commit()
        return redirect(url_for("index_admin"))
    return render_template("issue_book.html",title="Return a book",form=form,submit="return")
        

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    books = User.query.get(user.id).books.all()
    return render_template('user.html', user=user, books = books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    form = LoginForm()
    next=request.args.get('next')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
	if not next:
        	if user.username == 'admin' or user.occupation == 'faculty':
            		return redirect(url_for('index_admin'))
        	else:    
            		return redirect(url_for('index'))
        else:
		return redirect(next)
    return render_template('login.html',  title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        if session["username"]=='admin':
            form = RegistrationForm()
            if form.validate_on_submit():
                user = User(username=form.username.data, email=form.email.data,occupation="faculty",subject=form.subject.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('index_admin'))
            return render_template('register.html', title='Register', form=form)
        return redirect(url_for('index_admin'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,occupation="student")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        flash('Now, login')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


         
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))
