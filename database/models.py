from datetime import datetime
from flaskapp import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    user_fname = db.Column(db.String(255))
    user_sname = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    bookings = db.relationship("Booking", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, login, user_fname, user_sname, password):
        self.login = login
        self.user_fname = user_fname
        self.user_sname = user_sname
        self.password = password

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id!r}, name={self.user_fname!r}, surname={self.user_sname!r})"


    @property
    def id(self):
        return self.user_id


class Movie(db.Model):
    __tablename__ = "movies"
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    poster = db.Column(db.String(255), nullable=False)
    video = db.Column(db.String(255), nullable=False)

    bookings = db.relationship("Booking", back_populates="movie", cascade="all, delete-orphan")

    def __init__(self, title, genre, duration, description, release_date, poster, video):
        # self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.duration = duration
        self.description = description
        self.release_date = release_date
        self.poster = poster
        self.video = video
    def __repr__(self) -> str:
        return f"Movie(movie_id={self.movie_id!r}, title={self.title!r}, release_date={self.release_date!r}, poster={self.poster!r}, video={self.video!r})"


class Booking(db.Model):
    __tablename__ = "bookings"
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="bookings")
    movie = db.relationship("Movie", back_populates="bookings")

    def __repr__(self) -> str:
        return f"Booking(booking_id={self.booking_id!r}, user_id={self.user_id!r}, movie_id={self.movie_id!r}, booking_date={self.booking_date!r})"


class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)