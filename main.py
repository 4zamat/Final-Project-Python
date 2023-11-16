from flaskapp import *
from flask import render_template
# session here: Flask does this is by using a signed cookie.
from flask import request, session, redirect, url_for
from werkzeug.utils import secure_filename
from database.models import User, db, Car
from database import crud


@app.route("/")
# @app.route("/<context>")
def home(context=None):
    data = {"Data": "Some data here to be sent as dict (JSON)"}
    return render_template("index.html", context=None)


@app.route("/about")
def about(context=None):
    return render_template("about.html", context=context)


@app.route("/user/<int:user_id>")
def user_page(user_id, context=None):
    query = db.session.query(User).join(Car).filter(Car.car_owner == user_id).first()
    if query:
        return render_template("user page.html", context=query)
    else:
        query = db.session.query(User).filter(User.user_id == user_id).first()
        return render_template("user page.html", context=query)


@app.route("/login", methods=["GET", "POST"])
def login(context=None):
    if request.method == "POST":
        # you can check uncommenting this region if your data is coming or not
        # print(f"Username: {request.form['username']}, Password: {request.form['password']}")
        # making a query to a database
        user = db.session.query(User).filter_by(login=request.form['username'],
                                                password=request.form['password']).first()
        print(user)
        if user:
            session['authenticated'] = True
            session['uid'] = user.user_id
            session['username'] = user.login
            return redirect(url_for("user_page", user_id=user.user_id))
        else:
            return render_template("login.html", context="The login or username were wrong")

    return render_template("login.html", context=context)


@app.route("/logout")
def logout():
    session.pop('authenticated', None)
    session.pop('uid', None)
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/register', methods=["GET", "POST"])
def register(context=None):
    if request.method == "POST":
        login = request.form['username']
        fname = request.form['fname']
        sname = request.form['sname']
        pass1 = request.form['password']
        pass2 = request.form['password_conf']

        data = db.session.query(User).filter_by(login=request.form['username']).first()

        if data:
            return redirect(url_for("register", error="Already registered!"))
        elif pass1 != pass2:
            return redirect(url_for("register", error="Passowords do not match!"))
        else:
            crud.add_user(User(login=login,
                               user_fname=fname,
                               user_sname=sname,
                               password=pass1))

            return redirect(url_for("login", context="Succesfully registered!"))
    return render_template("registration.html", context=context)


@app.route("/upload", methods=["GET", "POST"])
def upload_file(context=None):
    if request.method == "POST":
        f = request.files["file_to_save"]
        f.save(f"saved files/{secure_filename(f.filename)}")
        return redirect(url_for('upload_file', context={"Status": "Successfully uploaded"}))
    return render_template("file upload.html", context=context)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
