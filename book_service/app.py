from flask import Flask
from config import Config
from models import db 
from controllers.book_controller import book_controller

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(book_controller, url_prefix='/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)