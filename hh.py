import os, csv
from booksdb import *
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
dbscope = scoped_session(sessionmaker(bind=engine))

def main():
    Base.metadata.create_all(bind=engine)
    f = open("books.csv")
    print(f)
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, year in reader:
        book = Books(isbn=isbn, title=title, author=author, year=int(year))
        dbscope.add(book)
    dbscope.commit()
    dbscope.close()

if __name__ == "__main__":
    main()