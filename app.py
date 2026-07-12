from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "malleswari_secret_key"

# ==========================
# Database Configuration
# ==========================
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:Malli123@database-1.ct2ke66uqwus.us-east-1.rds.amazonaws.com:3306/chrocet"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==========================
# User Model
# ==========================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)


# ==========================
# Routes
# ==========================

@app.route("/")
def home():
    username = session.get("user_name")
    return render_template(
        "index.html",
        username=username
    )

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/product")
def product():
    return render_template("product-details.html")


# ==========================
# Register User
# ==========================
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


# ==========================
# Login
# ==========================
@app.route("/authenticate", methods=["POST"])
def authenticate():

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):

    session["user_id"] = user.id
    session["user_name"] = user.name
    session["email"] = user.email

    return redirect(url_for("home"))

    return render_template(
        "login.html",
        error="Invalid Email or Password"
    )


# ==========================
# Test Database
# ==========================
@app.route("/testdb")
def test():
    try:
        db.session.execute(db.text("SELECT 1"))
        return "Database Connected Successfully"
    except Exception as e:
        return str(e)


# ==========================
# Run Application
# ==========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)