from models import db
from pydantic import BaseModel, Field

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
    
class BookModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    author: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1800, le=2025)  
    isbn: str = Field(..., min_length=8, max_length=50)
    class Config:
        extra = 'forbid'

class LoginModel(BaseModel):
    username: str = Field(..., min_length=1, max_length=30)
    password: str = Field(..., min_length=1, max_length=30)
    class Config:
        extra = 'forbid'