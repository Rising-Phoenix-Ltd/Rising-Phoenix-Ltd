from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os

# --- Constants ---
Mystic_Kings = "https://chat.whatsapp.com/Hlj0KZdogdWGXpU7M5YJTW"
Holy_Weebs = "https://chat.whatsapp.com/D5ed7HHs3qq2oHK77Kq9Hj"

# --- Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

Bootstrap(app)

# --- Database ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///rising-phoenix.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Login-Manager ---
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Database Tables ---
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    queries = relationship("Query", back_populates="query_user")
    uploads = relationship("Gallery", back_populates="gallery_user")


class Query(db.Model):
    __tablename__ = "queries"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    topic = db.Column(db.String(250), nullable=False)
    query = db.Column(db.Text, nullable=False)
    query_user = relationship("User", back_populates="queries")


class Gallery(db.Model):
    __tablename__ = "gallery"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(250), nullable=False)
    heading = db.Column(db.String(250), nullable=False)
    source = db.Column(db.Text, nullable=False)
    gallery_user = relationship("User", back_populates="uploads")


class Features(db.Model):
    __tablename__ = "features"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    link = db.Column(db.Text, nullable=False)


db.create_all()


# --- custom decorators ---
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id >= 3:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


# --- error-handlers ---
@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for('login'))


# --- web-routes ---
@app.route('/')
def home():
    return render_template("home.html", current_user=current_user)


# needs to flash flask messages
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if User.query.filter_by(email=email).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=email,
            name=username,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template("register.html", current_user=current_user)


# needs flash messages to work
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html", current_user=current_user)


# needs the flash messages to work
@app.route('/login-spl', methods=["GET", "POST"])
def login_spl():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("That email does not exist, please try again.")
        return redirect(url_for('login'))
    elif not check_password_hash(user.password, password):
        flash('Password incorrect, please try again.')
        return redirect(url_for('login'))
    else:
        login_user(user)
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/feature')
def feature():
    return render_template("feature.html", current_user=current_user)


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        topic = request.form['topic']
        query = request.form['query']

        new_query = Query(
            name=name,
            email=email,
            topic=topic,
            query=query
        )
        db.session.add(new_query)
        db.session.commit()
        return render_template("join.html", current_user=current_user, query_sent=True)
    return render_template("join.html", current_user=current_user)


@app.route('/join-whatsapp/<int:num>', methods=['GET', 'POST'])
@login_required
def join_whatsapp(num):
    if num == 1:
        return redirect(Mystic_Kings)
    elif num == 2:
        return redirect(Holy_Weebs)


@app.route('/privacy')
def privacy():
    return render_template("privacy.html")


if __name__ == "__main__":
    app.run(debug=True)
