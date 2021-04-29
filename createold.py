import os
from flask import Flask, request, render_template
from models import *
from flask import Flask, session, redirect
from flask_session import Session
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
engine = create_engine(os.getenv("DATABASE_URL"))

Session(app)
db.init_app(app)

@app.route('/')
def hello_world():
    return redirect('/register')
@app.route('/register', methods = ['POST','GET'])
def register():
    db.create_all()
    if request.method == 'POST':
        data = request.form
        userdata = USERS(request.form['email'],request.form['psw'])
        user = USERS.query.filter_by(emailid=request.form['email']).first()
        if user is not None:
            print("User is already existing. Please try to register with a new")
            var1 = "Error: User is already existing. Please try to register with a new one"
            return render_template("reg.html", var1 = var1)
        db.session.add(userdata)
        db.session.commit()
        print("Registration Success")
        var1 ='Registration Success'
        return render_template("reg.html", var1 = var1)
    else:
        return render_template("reg.html")
    

@app.route('/admin')
def admin():
    data = USERS.query.order_by(desc(USERS.timestamp)).all()
    print(data)
    return render_template("admin.html",admin = data)

@app.route('/auth', methods=['POST'])
def login():
    print(request.form)
    user = USERS.query.filter_by(emailid=request.form['email']).first()
    if user is not None:
        if bcrypt.verify(request.form['psw'], user.password):
            session['email'] = request.form['email']
            print(session)
            return redirect('/home')
        else:
            var1 = "Wrong Credentials"
            return render_template("reg.html", var1 = var1)
    else:
        print("You are not a registered user. Please first register to login")
        var1 = "Error: You are not a registered user. Please first register to login"
        return render_template("reg.html", var1 = var1)
@app.route('/home')
def home():
    try:
        user=session['email']
        return render_template("login.html")
    except:
        var1 = "You must log in to view the homepage"
        return render_template("reg.html",var1 = var1)

@app.route('/logout')
def logout():
    try:
        session.clear()
        var1 = "Logged Out"
        return render_template("reg.html", var1 = var1)
    except:
        var1 = "You must first log in to logout"
        return render_template("reg.html",var1 = var1)