import os

from flask import Flask, request, render_template,url_for, flash
from models import *
from hh import *
from Review import *
from flask import Flask, session, redirect
from flask_session import Session
from sqlalchemy import create_engine, desc , or_
from sqlalchemy.orm import scoped_session, sessionmaker
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

engine = create_engine(os.getenv("DATABASE_URL"))

Session(app)
db.init_app(app)

@app.route('/')
def hello_world():
    # return '<h1>Hello! Please add registration in the above url to register yourselves to website</h1>'
    return redirect('/registration')
@app.route('/registration', methods = ['POST','GET'])
def register():
    db.create_all()
    if request.method == 'POST':
        # data = request.form
        userdata = userswithtime(request.form['email'],request.form['psw'])
        user = userswithtime.query.filter_by(emailid=request.form['email']).first()
        if user is not None:
            print("User is already existing. Please try to register with a new")
            # return redirect('/')
            var1 = "Error: User is already existing. Please try to register with a new one"
            return render_template("reg.html", var1 = var1)
        db.session.add(userdata)
        db.session.commit()
        print("Registration Success")
        # return redirect('/registration')
        var1 ='Registration Success'
        return render_template("reg.html", var1 = var1)
        # return render_template("registrationdata.html",registrationdata = data)
    else:
        return render_template("reg.html")
    

@app.route('/admin')
def admin():
    data = userswithtime.query.order_by(desc(userswithtime.timestamp)).all()
    return render_template("admin.html",admin = data)

@app.route('/auth', methods=['POST'])
def login():
    print(request.form)
    user = userswithtime.query.filter_by(emailid=request.form['email']).first()
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
@app.route('/home', methods=['POST','GET'])
def home():
    try:
        user=session['email']
        if request.method == 'POST':
            req  = request.form['search']
            reqs = str(req)
            bookss = dbscope.query(Books.isbn, Books.title, Books.author, Books.year).filter(or_(Books.title.like("%"+reqs+"%"), Books.author.like("%"+reqs+"%"), Books.isbn.like("%"+reqs+"%"))).all()
            if bookss.__len__()==0:
                var1 = "No search found"
                return render_template("login.html", var1 = var1, user = user)
            return render_template("login.html",bookss = bookss,formaction = '/home', user = user)
        return render_template("login.html", user = user)
    except Exception as e:
        print(e)
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

@app.route('/books/<id>',methods=['POST','GET'])
def books(id):
    print(id)
    cuser = session['email']
    result = db.session.query(Books).filter(Books.isbn == id)
    print(result)
    data=Review.query.all()
    r=Review.query.filter_by(isbn=id).all()
    print(r)
    if request.method=='POST':
        reviewdata=Review(request.form['names'],id,request.form['email'],request.form['comment'],request.form['rating'])
        user = Review.query.filter_by(email=request.form['email'],isbn=id).first()
        data=Review.query.all()
        print(user)
        if user is not None:
            print("User had already given rating.")
            var1 = "Error: User had already given rating."
            return render_template("Book_Page.html", Book_details=result,var1 = var1,comments=r, allreviewdata = data )
        db.session.add(reviewdata)
        db.session.commit()
        var1="Review submitted"
        flash(var1)
        # url="/review/"+str(id)
        
        return redirect(url_for('books', id = id))
    else:
        # return render_template("review.html",comments=r,allreviewdata = data)
        return render_template('Book_Page.html', Book_details=result,Book_details_1=result,comments=r,allreviewdata = data)

# @app.route('/review/<id>', methods=['POST','GET'])
# def review(id):

#     data=Review.query.all()
#     r=Review.query.filter_by(isbn=id).all()
#     print(r)
  
#     if request.method=='POST':
#         reviewdata=Review(request.form['names'],id,request.form['email'],request.form['comment'],request.form['rating'])
#         user = Review.query.filter_by(email=request.form['email']).first()
#         data=Review.query.all()

#         if user is not None:
#             print("User had already given rating.")
#             var1 = "Error: User had already given rating."
#             return render_template("review.html", var1 = var1,comments=r, allreviewdata = data )
#         db.session.add(reviewdata)
#         db.session.commit()
#         var1="Review submitted"
#         flash(var1)
#         # url="/review/"+str(id)
        
#         return redirect(url_for('review', id = 12345))
#     else:
#         return render_template("review.html",comments=r,allreviewdata = data)
