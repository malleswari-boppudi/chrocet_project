from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

EMAIL = "admin@gmail.com"
PASSWORD = "admin123"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/authenticate", methods=["POST"])
def authenticate():

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return redirect(url_for("home"))

    return render_template(
        "login.html",
        error="Invalid Email or Password"
    )

@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    confirm = request.form.get("confirm_password")

    if password != confirm:
        return "Passwords do not match"

    # Database code will be added later

    return redirect(url_for("login_page"))

@app.route("/product")
def product():
    return render_template("product-details.html")


@app.route("/testdb")
def test():

    try:

        db.session.execute(db.text("SELECT 1"))

        return "Database Connected Successfully"

    except Exception as e:

        return str(e)
#connection to Database code
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:Malli123@database-1.ct2ke66uqwus.us-east-1.rds.amazonaws.com:3306/chrocet"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100), unique=True)

    phone = db.Column(db.String(20))

    password = db.Column(db.String(255))

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    confirm = request.form.get("confirm_password")

    if password != confirm:
        return "Passwords do not match"

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return "Email already registered"

    hashed_password = generate_password_hash(password)

    new_user = User(
        name=name,
        email=email,
        phone=phone,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login_page"))
       

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)