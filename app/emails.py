from flask_mail import Mail, Message
from app import app
from flask import render_template
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'krishnamaheshteja.n404@gmail.com'
app.config['MAIL_PASSWORD'] = 'somanukala'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)
def send_email(book,send_to,subject):
   msg = Message("Alert", sender = "krishnamaheshteja.n404@gmail.com", recipients =send_to)
   msg.html = render_template("email/reset_password.html",book=book,subject=subject)
   mail.send(msg)
   return "Sent"
def send_email1(send_to,subject,user):
   msg = Message("Password Change", sender = "krishnamaheshteja.n404@gmail.com", recipients =send_to)
   msg.html = render_template("email/reset_password1.html",subject=subject,user=user)
   mail.send(msg)
   return "Sent"
