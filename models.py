from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__= 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    isbn = db.Column(db.String(50), unique=True)

    def to_dic(self):
        return {
            'id': self.id,
            'title':self.title,
            'author':self.author,
            'year':self.year,
            'isbn':self.isbn
        }
    
    def __repr__(self):
        return f'<Book {self.title}>'   