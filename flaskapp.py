from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

# app object (literally web server)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r"postgresql://postgres:123@localhost:5432/cinema"

with app.app_context():
    db.init_app(app)

app.config['SECRET_KEY']="nN33WqfhR6vRreD9HW6j2fWj5oxsUS5H7e"