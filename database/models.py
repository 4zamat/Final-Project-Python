from flaskapp import db


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)  # integer primary key will be autoincremented by default
    login = db.Column(db.String(255), unique=True, nullable=False)
    user_fname = db.Column(db.String(255))
    user_sname = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)

    user_cars = db.relationship("Car", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(user_id {self.user_id!r}, name={self.user_fname!r}, surname={self.user_fname!r})"


class Car(db.Model):
    __tablename__ = "cars"
    car_id = db.Column(db.Integer, primary_key=True)  # integer primary key will be autoincremented by default
    car_vendor = db.Column(db.String(255), nullable=False)
    car_model = db.Column(db.String(255), nullable=False)
    car_owner = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    owner = db.relationship("User", back_populates="user_cars")

    def __repr__(self) -> str:
        return f"Car(car_id={self.car_id!r}, vendor={self.car_vendor!r}, model={self.car_model!r}, owner={self.car_owner!r})"