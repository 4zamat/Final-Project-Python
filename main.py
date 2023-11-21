from flask import render_template, request, session, redirect, url_for, flash
from database.models import User, Movie, db
from database import crud
from flaskapp import *
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/home")
def home():
    data = {"Data": "Some data here to be sent as dict (JSON)"}
    return render_template("HomePage.html", context=None)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/food")
def food():
    return render_template("food.html")


@app.route("/movies")
def movies():
    # movies = Movie.query.all()
    return render_template("movies.html")


@app.route("/user/<int:user_id>")
@login_required
def user_page(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    # Check if the requested user_id matches the current user's id
    if user_id != current_user.id:
        return "You are not authorized to view this profile", 403
    user = User.query.get(user_id)
    # booking = Booking.query.get()

    if user is None:
        return "User not found", 404

    # Checking if user is viewing his profile
    if user_id == current_user.id:
        return render_template("user.html", user=user, username=current_user.login)
    else:
        return "You are not authorized to view this profile", 403


@app.route('/register', methods=["GET", "POST"])
def register():
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
            return redirect(url_for("register", error="Passwords do not match!"))
        else:
            crud.add_user(User(login=login,
                               user_fname=fname,
                               user_sname=sname,
                               password=pass1))

            return redirect(url_for("login", context="Successfully registered!"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(login=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            return redirect(url_for("user_page", user_id=user.user_id))
        else:
            return render_template("login.html", context="The login or username were wrong")

    return render_template("login.html")
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form['login']
#         password = request.form['password']
#
#         # Check if the user is an admin
#         admin = User.query.filter_by(username=username, password=password, is_admin=True).first()
#
#         if admin:
#             login_user(admin)
#             flash('Admin login successful!', 'success')
#             return redirect(url_for("admin_dashboard"))
#         else:
#             # Check if the user is a regular user
#             user = User.query.filter_by(username=username, password=password).first()
#
#             if user:
#                 login_user(user)
#                 flash('User login successful!', 'success')
#                 return redirect(url_for("user_page", user_id=user.user_id))
#             else:
#                 flash('Invalid login credentials', 'danger')
#
#     return render_template("login.html", context=None)


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.is_admin:
        return render_template('admin_dashboard.html')
    else:
        # Redirect to a forbidden page or login page
        flash('You do not have the necessary privileges.', 'danger')
        return "You are not authorized to view this profile", 403


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


#admin
@app.route('/admin')
def Index():
    all_data = User.query.all()

    return render_template("RestApi.html", users = all_data)


#insert
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        login = request.form['login']
        user_fname = request.form['user_fname']
        user_sname = request.form['user_sname']
        password = request.form['password']


        my_data = User(login,user_fname, user_sname,password)
        db.session.add(my_data)
        db.session.commit()

        flash("User Inserted Successfully")

        return redirect(url_for('Index'))



#update_portfolio
@app.route('/update', methods = ['POST'])
def update():

    if request.method == 'POST':
        my_data = User.query.get(request.form.get('user_id'))

        my_data.login = request.form['login']
        my_data.user_fname = request.form['user_fname']
        my_data.user_sname = request.form['user_sname']
        my_data.password = request.form['password']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))


#delete
@app.route('/delete/<id>/', methods = ['GET', 'DELETE'])
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
