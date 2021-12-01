from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from functools import wraps
from mega import Mega
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from datetime import date
from random import choice, randint, shuffle
from yt import upload_vid_to_yt
import cloudinary
from cloudinary import uploader
import requests
import base64
import os

# TODO : Change all env variables
# --- Constants ---
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Mystic_Kings = "https://chat.whatsapp.com/Hlj0KZdogdWGXpU7M5YJTW"
Holy_Weebs = "https://chat.whatsapp.com/D5ed7HHs3qq2oHK77Kq9Hj"

# TODO : Try to upload image files directly to server
ImgBB_Key = "5a48610469a8a375bb344eb0335517dc"
ImgBB_Link = "https://api.imgbb.com/1/upload"

Unsplash_Access_Key = 'YG2pu5F3eWsOiwsIMtEugbOrA9zD2ZV2ZBTQjrQd5fQ'
Unsplash_Secret_Key = 'VTMIdRm9m6Uw1MKheKaXOAYULsgIV8Y18ucqTBcmFe4'
Unsplash_Link = f'https://api.unsplash.com/photos/?client_id={Unsplash_Access_Key}'

Cloudinary_Api_Link = 'https://api.cloudinary.com/v1_1/rp-web/image/upload'
Cloudinary_Api_Key = '694757294873781'
Cloudinary_Api_Secret = 'Jtc6kSrM4CShKDaa9yljnHsVL7g'
Cloudinary_Api_Name = 'rp-web'

# --- Mega ---
mega = Mega()

# --- Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hey_yo_mf'
# os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
Bootstrap(app)

# --- Flask-Mail ---
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'bigbrawler001@gmail.com'
app.config['MAIL_PASSWORD'] = 'adityakore'
app.config['MAIL_DEFAULT_SENDER'] = 'bigbrawler001@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

# --- Database ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///rising-phoenix.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Login-Manager ---
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        return user
    else:
        return None


# --- Database Tables ---
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    profile_pic = db.Column(db.Text)
    bio = db.Column(db.Text)
    queries = db.relationship("Query", backref='user', lazy=True)
    uploads = db.relationship("Gallery", backref='user', lazy=True)


class Query(db.Model):
    __tablename__ = "queries"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    topic = db.Column(db.String(250), nullable=False)
    query = db.Column(db.Text, nullable=False)


class Gallery(db.Model):
    __tablename__ = "gallery"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(250), nullable=False)


class Gallery_Video(db.Model):
    __tablename__ = "video_upload"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    source = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(250), nullable=False)


class Gallery_Photo(db.Model):
    __tablename__ = "photo_upload"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    source = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(250), nullable=False)


class Features(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    source = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.Text, nullable=False)


db.create_all()


# --- Custom Functions ---
def generate_id():
    password_letters = [choice(LETTERS) for _ in range(randint(8, 10))]
    password_numbers = [choice(NUMBERS) for _ in range(randint(2, 4))]
    password_list = password_letters + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    return password


# --- custom decorators ---
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


# --- error-handlers ---
@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.html")


# --- web-routes ---
@app.route('/')
def home():
    return render_template("tabs/home.html", current_user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        if User.query.filter_by(name=username).first():
            flash('This Username is already taken.')
            return redirect(request.url)
        email = request.form["email"]
        password = request.form["password"]
        account_link = f"https://risingphoenix.herokuapp.com/profile/u/{username}"
        if User.query.filter_by(email=email).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        unique_id = generate_id()
        while User.query.filter_by(unique_id=unique_id).first():
            unique_id = generate_id()
        new_user = User(
            unique_id=unique_id,
            email=email,
            name=username,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        msg = Message(
            subject="Welcome to Rising Phoenix",
            body=f"Hi {username}, welcome to Rising Phoenix\n\n"
                 f"Now that your account is ready, you can share your content with us and get featured on our "
                 f"YouTube channel!\n"
                 f"You can also Join our lively groups and chat with them day & night :)\n\n"
                 f"By the way, here is you very own awesome profile page: {account_link}"
                 f" Go ahead and customize it, its all yours!.\n\n"
                 f"See you on the other side,\n"
                 f"Rising Phoenix\n\n"
                 f"--\n"
                 f"This is auto-generated message.\n"
                 f"Please visit https://risingphoenix.herokuapp.com for further query.",
            recipients=[email]
        )
        mail.send(msg)
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template("accounts/register.html", current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist! Join us now!!.")
            return redirect(url_for('register'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("accounts/login.html", current_user=current_user)


@app.route('/login-spl', methods=["GET", "POST"])
def login_spl():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("That email does not exist, please try again.")
        return redirect(url_for('register'))
    elif not check_password_hash(user.password, password):
        flash('Password incorrect, please try again.')
        return redirect(url_for('login'))
    else:
        login_user(user)
        return redirect(url_for('home'))


@app.route('/forgot-pass', methods=['GET', 'POST'])
def forgot():
    if request.method == "POST":
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(request.url)
        else:
            name = user.name
            id = user.unique_id
            reset_link = "https://risingphoenix.herokuapp.com/reset?id="

            msg = Message(
                subject="Password Reset",
                body=f"Hello {name}\n"
                     f"You have requested for resetting password on Rising Phoenix\n\n"
                     f"Please follow the link below to reset your password:\n"
                     f"{reset_link}{id}\n\n"
                     # f"http://127.0.0.1:5000/reset?id={id}\n\n"
                     f"If you haven't requested the reset, please ignore this email.\n\n\n"
                     f"This is an Auto-generated mail. Sender doesn't support replies.\n"
                     f"Contact the developers if you have any queries.",
                recipients=[email]
            )
            mail.send(msg)
            flash('Mail Sent. Please check your Email Inbox.')
            return redirect(request.url)
    return render_template("accounts/forgot-password.html")


# TODO : Add the redirect forbidden route if user access via typing link
@app.route('/reset', methods=['GET'])
def reset_password():
    id = request.args.get("id")
    return render_template("accounts/reset-password.html", id=id)


@app.route('/reset-success/<id>', methods=['POST'])
def reset_password_post(id):
    user = User.query.filter_by(unique_id=id).first()
    name = user.name
    email = user.email
    date_time = date.today().strftime("%m/%d/%Y, %H:%M:%S")

    db.session.delete(user)
    db.session.commit()
    password = request.form['password']
    hash_and_salted_password = generate_password_hash(
        password,
        method='pbkdf2:sha256',
        salt_length=8
    )
    reset_id = User(
        unique_id=user.unique_id,
        name=name,
        email=email,
        password=hash_and_salted_password,
        profile_pic=user.profile_pic,
        bio=user.bio
    )
    db.session.add(reset_id)
    db.session.commit()
    msg = Message(
        subject="Rising Phoenix Password Reset",
        body=f"Hello {name}\n"
             f"Your Password reset was successful on {date_time}.\n\n"
             f"Please continue to enjoy our service without any hesitation.\n"
             f"We are always there for any queries you have.\n\n"
             f"If you haven't done the reset,"
             f" please contact us immediately via our support line on https://risingphoenix.herokuapp.com/join\n"
             f"Also, please mention your query as 'Pass Issue'\n\n\n"
             f"--\n"
             f"This is an Auto-generated mail. Sender doesn't support replies.",
        recipients=[email]
    )
    mail.send(msg)
    flash('Password changed successfully! Please login to Continue.')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/feature', methods=['GET', 'POST'])
def feature():
    videos_data = Features.query.all()
    return render_template("tabs/feature.html", current_user=current_user, videos=videos_data)


@app.route("/delete/<int:vid_id>")
@admin_only
def delete_vid(vid_id):
    vid_to_delete = Features.query.get(vid_id)
    db.session.delete(vid_to_delete)
    db.session.commit()
    return redirect(url_for('feature'))


@app.route('/feature/admin', methods=['GET', 'POST'])
@admin_only
def feature_admin():
    if request.method == "POST":
        new_video = Features(
            title=request.form['title'],
            source=request.form['src'],
            thumbnail=request.form['thumbnail'],
        )
        db.session.add(new_video)
        db.session.commit()
        return redirect(url_for('feature'))
    return render_template("admin.html")


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == "POST":
        if not current_user:
            flash('You need to login to send Query')
            return redirect(url_for('login'))
        else:
            name = request.form['name']
            email = request.form['email']
            topic = request.form['topic']
            query = request.form['query']

            msg = Message(
                subject="Query From Website",
                body=f"Hello, you have new query\n\n"
                     f"Name: {name}\n"
                     f"Email: {email}\n"
                     f"Topic: {topic}\n"
                     f"Query: {query}",
                recipients=["risingphoenix.web.in@gmail.com"]
            )
            mail.send(msg)

            new_query = Query(
                name=name,
                email=email,
                topic=topic,
                query=query,
                user=current_user
            )
            db.session.add(new_query)
            db.session.commit()
            return render_template("tabs/join.html", current_user=current_user, query_sent=True)
    return render_template("tabs/join.html", current_user=current_user)


@app.route('/join-whatsapp/<int:num>', methods=['GET', 'POST'])
@login_required
def join_whatsapp(num):
    if num == 1:
        return redirect(Mystic_Kings)
    elif num == 2:
        return redirect(Holy_Weebs)


@app.route('/gallery')
def gallery():
    video_data = Gallery_Video.query.all()
    photo_data = Gallery_Photo.query.all()
    return render_template("tabs/gallery.html", current_user=current_user, videos=video_data, photos=photo_data)


# TODO : see if you can use user_id to get the username
# TODO : date time change to ago format
# TODO : remove the possibility of uploading pdfs and others
@app.route('/gallery/upload', methods=['GET', 'POST'])
def gallery_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        else:
            name = current_user.name
            title = request.form['title']
            description = request.form['description']
            option = request.form['option']
            date_time = date.today().strftime("%d %b %Y")

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_to_upload = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # TODO: Fix the base64 code for image, or find some other way to upload files (ps. removed option from upload-admin)
            if option == 'Image':
                m = mega.login(os.environ.get('MEGA_ID'), os.environ.get('MEGA_PASS'))
                m.upload(file_to_upload)
            else:
                m = mega.login(os.environ.get('MEGA_ID'), os.environ.get('MEGA_PASS'))
                m.upload(file_to_upload)
            new_upload = Gallery(
                name=name,
                title=title,
                description=description,
                date=date_time,
                user=current_user,
                type=option
            )
            db.session.add(new_upload)
            db.session.commit()

            post_req = Gallery.query.filter_by(title=title).first()
            msg = Message(
                subject="Upload From Website",
                body=f"Hello, you have new upload on website\n\n"
                     f"USER ID: {current_user.id}\n"
                     f"POST ID: {post_req.id}\n"
                     f"Name: {name}\n"
                     f"Title: {title}\n"
                     f"Description: {description}\n"
                     f"Date & time: {date_time}\n"
                     f"File Name: {filename}",
                recipients=["risingphoenix.web.in@gmail.com"]
            )
            mail.send(msg)
            os.remove(file_to_upload)
            flash("Thanks for submitting your work."
                  " We will review it and take according action.\n"
                  "Note: We don't take any credits of your work. We respect it.")
            return redirect(url_for('gallery'))
    return render_template("upload.html")


@app.route('/gallery/upload/admin', methods=['GET', 'POST'])
def gallery_upload_admin():
    if request.method == 'POST':
        upload_user = User.query.get(request.form['user_id'])
        email = upload_user.email

        post = Gallery.query.get(request.form['post_id'])
        name = post.name
        title = post.title
        description = post.description
        type = post.type

        if type == 'Image':
            admin_upload = Gallery_Photo(
                name=name,
                title=title,
                description=description,
                source=request.form['link'],
                date=post.date,
            )
            db.session.delete(post)
            db.session.add(admin_upload)
            db.session.commit()
            return redirect(url_for('gallery'))

        elif type == 'Video':
            yt_url = request.form['youtube']
            msg = Message(
                subject="Your Video Selected!",
                body=f"Hello, your video has been selected for YouTube upload!\n\n"
                     f"Thanks for sharing your content with us.\n"
                     f"The link to the video: {yt_url}\n"
                     f"Title: {title}\n"
                     f"Description: {description}\n\n"
                     f"--\n"
                     f"This is a Auto-generated mail. Sender doesn't support replies.\n"
                     f"Contact the developers if you have any queries.",
                recipients=[email]
            )
            mail.send(msg)
            admin_upload = Gallery_Video(
                name=name,
                title=title,
                description=description,
                source=request.form['link'],
                date=post.date,
            )
            db.session.delete(post)
            db.session.add(admin_upload)
            db.session.commit()
            return redirect(url_for('gallery'))
    return render_template("upload-admin.html")


@app.route('/gallery/delete/vid<int:vid_id>')
def gallery_vid_delete(vid_id):
    video = Gallery_Video.query.get(vid_id)
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('gallery'))


@app.route('/gallery/delete/photo<int:photo_id>')
def gallery_photo_delete(photo_id):
    photo = Gallery_Photo.query.get(photo_id)
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('gallery'))


# TODO : Make storage for profile pics (locally or cloud)
@app.route('/profile/u/<name>')
def profile(name):
    user = User.query.filter_by(name=name).first()
    try:
        if current_user.unique_id == user.unique_id:
            return render_template('profile.html', is_auth=True, user=user)
        else:
            return render_template('profile.html', user=user)
    except AttributeError:
        return redirect(url_for('login'))


# TODO : Make the settings work again
@app.route('/profile/u/<name>/settings')
def settings(name):
    user = User.query.filter_by(name=name).first()
    try:
        if current_user.unique_id == user.unique_id:
            return render_template('settings/settings.html', is_auth=True, user=user)
        else:
            return redirect(url_for('home'))
    except AttributeError:
        return redirect(url_for('not_found'))


# TODO : Make the settings work again
# TODO : Save the Profile Pic somewhere
# TODO : Make it not compulsory to upload profile pic
@app.route('/profile/u/<name>/settings/post', methods=['GET', 'POST'])
def settings_post(name):
    user = User.query.filter_by(name=name).first()
    try:
        if current_user.unique_id == user.unique_id:
            if 'profile-pic' not in request.files:
                flash('No file selected')
                return redirect(url_for('settings', name=name))

            if 'profile-pic' in request.files:
                file = request.files['profile-pic']
                if file.filename == '':
                    print('empty')
                else:
                    filename = f'profile-{name}_' + secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    file_to_upload = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                    m = mega.login(os.environ.get('MEGA_ID'), os.environ.get('MEGA_PASS'))
                    m.upload(file_to_upload)

                    os.remove(file_to_upload)

            email = request.form['edit-email']
            name = request.form['edit-username']
            bio = request.form['edit-bio']

            user_change = User(
                id=user.id,
                unique_id=user.unique_id,
                name=name,
                email=email,
                password=user.password,
                profile_pic=user.profile_pic,
                bio=bio
            )
            db.session.delete(user)
            db.session.commit()
            db.session.add(user_change)
            db.session.commit()
            flash('Pic Under Review! Please wait till tomorrow for changes to be seen.')
            return redirect(url_for('settings', name=name))
        else:
            return redirect(url_for('home'))
    except AttributeError:
        return redirect(url_for('not_found'))


@app.route('/profile/u/<name>/settings/change-password', methods=['GET'])
def change_password(name):
    user = User.query.filter_by(name=name).first()
    try:
        if current_user.unique_id == user.unique_id:
            return render_template('settings/change-password.html', is_auth=True, user=user)
        else:
            logout_user()
            flash('Please Login to Continue')
            return redirect(url_for('login'))
    except AttributeError:
        flash('Please Login to Continue')
        return redirect(url_for('login'))


# TODO : Check all the parameters for the password Change
@app.route('/profile/u/<name>/settings/change-password/post', methods=['POST'])
def change_password_post(name):
    user = User.query.filter_by(name=name).first()
    try:
        if current_user.unique_id == user.unique_id:
            old_pass = request.form['old_pass']
            new_pass = request.form['new_pass']
            if old_pass == new_pass:
                flash('Please Enter A Brand-New Password!')
                return redirect(request.url)
            elif not check_password_hash(user.password, old_pass):
                flash('Incorrect Old Password! Please Try Again.')
                return redirect(request.url)
            else:
                name = user.name
                email = user.email
                date_time = date.today().strftime("%m/%d/%Y, %H:%M:%S")
                hash_and_salted_password = generate_password_hash(
                    new_pass,
                    method='pbkdf2:sha256',
                    salt_length=8
                )
                reset_id = User(
                    unique_id=user.unique_id,
                    name=name,
                    email=email,
                    password=hash_and_salted_password,
                    profile_pic=user.profile_pic,
                    bio=user.bio
                )
                db.session.delete(user)
                db.session.commit()
                db.session.add(reset_id)
                db.session.commit()
                msg = Message(
                    subject="Rising Phoenix Password Reset",
                    body=f"Hello {name}\n"
                         f"Your Password reset was successful on {date_time}.\n\n"
                         f"Please continue to enjoy our service without any hesitation.\n"
                         f"We are always there for any queries you have.\n\n"
                         f"If you haven't done the reset, "
                         f"please contact us immediately via our support line on "
                         f"https://risingphoenix.herokuapp.com/join\n"
                         f"Also, please mention your query as 'Pass Issue'\n\n\n"
                         f"--\n"
                         f"This is an Auto-generated mail. Sender doesn't support replies.",
                    recipients=[email]
                )
                mail.send(msg)
                flash('Password changed successfully! Please login to Continue.')
                logout_user()
                return redirect(url_for('login'))
        else:
            return redirect(url_for('home'))
    except AttributeError:
        return redirect(url_for('not_found'))


@app.route('/profile/u/<name>/settings/others', methods=['GET'])
def other_settings(name):
    user = User.query.filter_by(name=name).first()
    try:
        if current_user.unique_id == user.unique_id:
            return render_template('settings/others.html', is_auth=True, user=user)
        else:
            return redirect(url_for('home'))
    except AttributeError:
        return redirect(url_for('not_found'))


@app.route('/profile/u/<name>/settings/others/post', methods=['POST'])
def other_settings_post(name):
    user = User.query.filter_by(name=name).first()
    try:
        if current_user.unique_id == user.unique_id:
            return render_template('settings/others.html', is_auth=True, user=user)
        else:
            return redirect(url_for('home'))
    except AttributeError:
        return redirect(url_for('not_found'))


# TODO : make a terms & conditions pdf
@app.route('/terms')
def terms():
    return render_template('privacy.html')


@app.route('/*')
def not_found():
    return render_template('notfound.html')


if __name__ == "__main__":
    app.run()

# Extra Work's
# TODO : Adding @User in url for logged in user
# TODO : Different kinds of flash messages
# TODO : Add Dark-mode to website
# TODO : Change the icon size
# TODO : Login button fix
# TODO : Make and work on Settings Privacy section
# TODO : Retrieve the Name and Location of device using website
# TODO : See if you can make users choose whether it is video upload or Image upload
# TODO : Fix the Pre-filled input issue in the settings tab
# TODO : Catch the Tickboxes from other-settings tab
# TODO : Add the Forbidden Page to website
# TODO : Add one time usable code for resetting password
