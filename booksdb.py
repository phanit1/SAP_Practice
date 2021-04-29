from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Books(Base):
   __tablename__ = "books_info"
   isbn = Column(String, primary_key = True)
   title = Column(String,nullable = False)
   author = Column(String,nullable = False)
   year = Column(Integer,nullable = False)

   def __init__(self,isbn,title,author,year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year