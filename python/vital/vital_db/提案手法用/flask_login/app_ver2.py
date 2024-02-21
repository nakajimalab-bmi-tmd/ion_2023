from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pytz
import time
import irisnative


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///practice.db"
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Post(db.Model):   #Postテーブルを作った的な
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default = datetime.now(pytz.timezone("Asia/Tokyo")))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(12))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET","POST"])
#@login_required
def index():
    return render_template("index.html")
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = User(username=username, password=generate_password_hash(password, method = "sha256"))

        db.session.add(user)
        db.session.commit()

        return redirect("/login")
    else:
        return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('QR_patient', username=username))
    else:
        return render_template("login.html")
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get("title")
        body = request.form.get("body")

        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()

        return redirect("/")
    else:
        return render_template("create.html")


@app.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):
    post = Post.query.get(id)

    if request.method == 'GET':
        return render_template("update.html", post=post)
    else:
        post.title = request.form.get("title")
        post.body = request.form.get("body")
        db.session.commit()

        return redirect("/")
    
@app.route("/<int:id>/delete", methods=["GET"])
@login_required
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect("/")

@app.route("/QR_patient/<username>", methods=["GET", "POST"])
@login_required
def QR_patient(username):
    if request.method == "POST":
        patient = request.form.get("ID")
        return redirect(url_for('QR_device', username=username, patient=patient))
    else:
        return render_template("QR_patient_ver2.html")
    
@app.route("/QR_device/<username>/<patient>", methods=["GET", "POST"])
@login_required
def QR_device(username, patient):
    if request.method == "POST":
        ip = "192.168.11.3"
        port = 1972
        namespace = "FS"
        user = "_SYSTEM"
        password = "bmi-2718"

        # create database connection and IRIS instance
        connection = irisnative.createConnection(ip,port,namespace,user,password)
        iris_native = irisnative.createIris(connection)

        dt_now = datetime.now()
        device = request.form.get("ID")
        insert_pa = iris_native.classMethodValue("ion.bital","Insert","機器ID", patient, None, device, dt_now.strftime("%Y/%m/%d %H:%M:%S.%f"), None, None)
        insert_nu = iris_native.classMethodValue("ion.bital","Insert","機器ID", username, None, device, dt_now.strftime("%Y/%m/%d %H:%M:%S.%f"), None, None)
        connection.close()
        return render_template("QR_device_ver2.html")
    
    else:
        return render_template("QR_device_ver2.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
    #app.run(debug=True)

