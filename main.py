from flask import render_template, request, session, redirect, url_for, flash
from database.models import User, Movie, Booking, db
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
    all_movies = Movie.query.order_by(Movie.release_date.desc()).all()
    for film in all_movies:
        film.release_date = film.release_date.strftime("%B %d, %Y")
    return render_template("movies.html", all_movies=all_movies)


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


@app.route("/movie/<movie_id>")
def movie_page(movie_id):
    movie = Movie.query.get(movie_id)
    # booking = Booking.query.get()

    if movie is None:
        return "User not found", 404

    return render_template("movie.html", movie=movie)

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


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         user = User.query.filter_by(login=request.form['username'], password=request.form['password']).first()
#         if user:
#             login_user(user)
#             return redirect(url_for("user_page", user_id=user.user_id))
#         else:
#             return render_template("login.html", context="The login or username were wrong")
#
#     return render_template("login.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(login=username, password=password).first()
        if user:
            login_user(user)
            if username == 'admin' and password == 'admin':
                return redirect(url_for("admin_page"))
            else:
                return redirect(url_for("user_page", user_id=user.user_id))
        else:
            return render_template("login.html", context="The login or username were wrong")

    return render_template("login.html")


# @app.route('/admin/dashboard')
# @login_required
# def admin_dashboard():
#     if current_user.is_admin:
#         return render_template('RestApi.html')
#     else:
#         # Redirect to a forbidden page or login page
#         flash('You do not have the necessary privileges.', 'danger')
#         return "You are not authorized to view this profile", 403


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


#admin
# @app.route('/admin')
# def Index():
#     all_data = User.query.all()
#
#     return render_template("RestApi.html", users = all_data)
@app.route('/admin')
@login_required  # Requires the user to be logged in to access this route
def admin_page():
    if current_user.login == 'admin':  # Use the appropriate attribute for the username
        all_data = User.query.all()
        return render_template("RestApi.html", users=all_data)
    else:
        return "Access forbidden. You must be an admin to access this page.", 403

@app.route('/admin/movie')
@login_required  # Requires the user to be logged in to access this route
def admin_movie_page():
    if current_user.login == 'admin':  # Use the appropriate attribute for the username
        all_movie_data = Movie.query.all()
        return render_template("RestApi_Movie.html", users=all_movie_data)
    else:
        return "Access forbidden. You must be an admin to access this page.", 403

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

        return redirect(url_for('admin_page'))

@app.route('/insert/movie', methods = ['POST'])
def insert_movie():
    if request.method == 'POST':

        title = request.form['title']
        genre = request.form['genre']
        duration = request.form['duration']
        description = request.form['description']
        release_date = request.form['release_date']
        poster = request.form['poster']

        my_movie_data = Movie(title,genre,duration,description,release_date, poster)
        db.session.add(my_movie_data)
        db.session.commit()

        flash("Movie Inserted Successfully")

        return redirect(url_for('admin_movie_page'))


#update
@app.route('/update', methods = ['POST'])
def update():

    if request.method == 'POST':
        my_data = User.query.get(request.form.get('user_id'))

        my_data.login = request.form['login']
        my_data.user_fname = request.form['user_fname']
        my_data.user_sname = request.form['user_sname']
        my_data.password = request.form['password']

        db.session.commit()
        flash("User Updated Successfully")

        return redirect(url_for('admin_page'))


@app.route('/update/movie', methods = ['POST'])
def update_movie():

    if request.method == 'POST':
        my_movie_data = Movie.query.get(request.form.get('movie_id'))

        my_movie_data.title = request.form['title']
        my_movie_data.genre = request.form['genre']
        my_movie_data.duration = request.form['duration']
        my_movie_data.description = request.form['description']
        my_movie_data.release_date = request.form['release_date']
        my_movie_data.poster = request.form['poster']

        db.session.commit()
        flash("Movie Updated Successfully")

        return redirect(url_for('admin_movie_page'))

#delete
@app.route('/delete/<id>/', methods = ['GET', 'DELETE'])
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("User Deleted Successfully")

    return redirect(url_for('admin_page'))

@app.route('/delete/movie/<id>/', methods = ['GET', 'DELETE'])
def delete_movie(id):
    my_movie_data = Movie.query.get(id)
    db.session.delete(my_movie_data)
    db.session.commit()
    flash("Movie Deleted Successfully")

    return redirect(url_for('admin_movie_page'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
