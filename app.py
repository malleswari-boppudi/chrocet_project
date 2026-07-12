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

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image = db.Column(db.String(255))
    stock = db.Column(db.Integer)
    category = db.Column(db.String(100))
# ==========================
# Routes
# ==========================

@app.route("/")
def home():

    username = session.get("user_name")

    products = Product.query.all()

    return render_template(
        "index.html",
        username=username,
        products=products
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


@app.route("/product/<int:id>")
def product(id):

    product = Product.query.get_or_404(id)

    username = session.get("user_name")

    return render_template(
        "product-details.html",
        product=product,
        username=username
    )
# ==========================
# Add to Cart
# ==========================
@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT * FROM cart
        WHERE user_id=%s AND product_id=%s
    """, (user_id, product_id))

    item = cursor.fetchone()

    if item:
        cursor.execute("""
            UPDATE cart
            SET quantity = quantity + 1
            WHERE user_id=%s AND product_id=%s
        """, (user_id, product_id))

    else:
        cursor.execute("""
            INSERT INTO cart(user_id, product_id, quantity)
            VALUES(%s,%s,1)
        """, (user_id, product_id))

    mysql.connection.commit()
    cursor.close()

    return redirect("/cart")  

@app.route("/cart")
def cart():

    if "user_id" not in session:
        return redirect("/login")

    cursor = mysql.connection.cursor()

    cursor.execute("""
    SELECT
        cart.id,
        products.id,
        products.name,
        products.price,
        products.image,
        cart.quantity,
        (products.price * cart.quantity) AS total

    FROM cart

    JOIN products
    ON cart.product_id = products.id

    WHERE cart.user_id=%s
    """, (session["user_id"],))

    cart_items = cursor.fetchall()

    grand_total = sum(item[6] for item in cart_items)

    cursor.close()

    return render_template(
        "cart.html",
        cart_items=cart_items,
        grand_total=grand_total
    )
# ==========================
# Increase Cart Item Quantity
# ==========================
@app.route("/increase/<int:cart_id>")
def increase(cart_id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
    UPDATE cart
    SET quantity = quantity + 1
    WHERE id=%s
    """, (cart_id,))

    mysql.connection.commit()
    cursor.close()

    return redirect("/cart")
# ==========================
# Decrease Cart Item Quantity
# ==========================
@app.route("/decrease/<int:cart_id>")
def decrease(cart_id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
    UPDATE cart
    SET quantity = quantity - 1
    WHERE id=%s AND quantity>1
    """, (cart_id,))

    mysql.connection.commit()
    cursor.close()

    return redirect("/cart")
# ==========================
# Remove Cart Item
# ==========================
@app.route("/remove/<int:cart_id>")
def remove(cart_id):

    cursor = mysql.connection.cursor()

    cursor.execute("""
    DELETE FROM cart
    WHERE id=%s
    """, (cart_id,))

    mysql.connection.commit()
    cursor.close()

    return redirect("/cart")
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