from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Review(db.Model):
    __tablename__ = "review"
    names = db.Column(db.String,primary_key=True)
    isbn = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    rating = db.Column(db.String, nullable=False)
    
    def __init__(self,names,isbn,email,comment,rating) :
        self.names = names
        self.isbn = isbn
        self.email = email
        self.comment=comment
        self.rating = rating
     
    