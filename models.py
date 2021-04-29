from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import bcrypt
db = SQLAlchemy()

class userswithtime(db.Model):
   
   __tablename__ = "userswithtime"
   emailid = db.Column(db.String, primary_key = True)
   password = db.Column(db.String,nullable = False)
   timestamp = db.Column(db.DateTime(timezone=True),nullable = False)

   def __init__(self,emailid,password):
      
      self.emailid = emailid
      self.password = bcrypt.encrypt(password)
      self.timestamp = datetime.now()


   