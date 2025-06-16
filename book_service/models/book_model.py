from models import db


class Book(db.Model):
    __tablename__='books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    isbn = db.Column(db.String(50), unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title':self.title,
            'author':self.author,
            'year':self.year,
            'isbn':self.isbn
        }