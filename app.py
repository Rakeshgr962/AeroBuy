from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Connect to MongoDB 
client = MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
users_collection = db["users"]
checkout_collection = db["checkouts"]
orders_collection = db["orders"]
products_collection = db["products"]

# Add products to database if not exists
def initialize_products():
    products = [
        {"name": "Luxury Perfume", "price": 1999, "image": "perfume.jpeg", "category": "beauty"},
        {"name": "Stylish Sunglasses", "price": 799, "image": "sunglasses.jpeg", "category": "fashion"},
        {"name": "Casual Sneakers", "price": 2499, "image": "sneakers.jpeg", "category": "fashion"},
        {"name": "Smart Watch", "price": 3499, "image": "smartwatch.jpeg", "category": "electronics"},
        {"name": "Wireless Headphones", "price": 2199, "image": "headphones.jpeg", "category": "electronics"},
        {"name": "Leather Wallet", "price": 999, "image": "wallet.jpeg", "category": "accessories"},
        {"name": "Digital Camera", "price": 5999, "image": "camera.jpeg", "category": "electronics"},
        {"name": "Wireless Mouse", "price": 499, "image": "mouse.jpeg", "category": "electronics"},
        {"name": "Desk Lamp", "price": 599, "image": "lamp.jpeg", "category": "home"}
    ]
    
    for product in products:
        if not products_collection.find_one({"name": product["name"]}):
            products_collection.insert_one(product)

initialize_products()

@app.route("/")
def home():
    search_query = request.args.get("search", "")
    if search_query:
        products = list(products_collection.find({"name": {"$regex": search_query, "$options": "i"}}).limit(8))
    else:
        products = list(products_collection.find().limit(8))
    return render_template("home.html", products=products, search_query=search_query)

@app.route("/product")
def product():
    search_query = request.args.get("search", "")
    if search_query:
        products = list(products_collection.find({"name": {"$regex": search_query, "$options": "i"}}))
    else:
        products = list(products_collection.find())
    return render_template("project.html", products=products, search_query=search_query)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]
        password = request.form["password"]
        re_password = request.form["re_password"]

        if password != re_password:
            error = "Passwords do not match!"
            return render_template("signin.html", error=error)

        if users_collection.find_one({"contact": contact}):
            error = "User with this contact already exists!"
            return render_template("signin.html", error=error)

        users_collection.insert_one({
            "name": name,
            "contact": contact,
            "password": password,
            "created_at": datetime.now()
        })

        return render_template("welcome.html", name=name)

    return render_template("signin.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_name = request.form.get("product_name")
    product_price = float(request.form.get("product_price"))
    product_image = request.form.get("product_image")

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]
    cart.append({
        "name": product_name,
        "price": product_price,
        "image": product_image,
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    session["cart"] = cart
    return redirect(request.referrer or url_for("home"))

@app.route("/remove_from_cart/<int:index>", methods=["POST"])
def remove_from_cart(index):
    if "cart" in session and 0 <= index < len(session["cart"]):
        session["cart"].pop(index)
        session.modified = True
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    subtotal = sum(item["price"] for item in cart)
    shipping = 8.00
    tax = 0.00
    total = subtotal + shipping + tax
    
    return render_template("cart.html", 
                         cart=cart,
                         subtotal=subtotal,
                         shipping=shipping,
                         tax=tax,
                         total=total)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        checkout_data = {
            "delivery_option": request.form.get("delivery_option"),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "address": request.form.get("address"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "payment_method": request.form.get("payment_method"),
            "cart": session.get("cart", []),
            "subtotal": sum(item["price"] for item in session.get("cart", [])),
            "shipping": 8.00,
            "tax": 0.00,
            "total": sum(item["price"] for item in session.get("cart", [])) + 8.00,
            "checkout_date": datetime.now(),
            "status": "processing"
        }
        
        order_id = checkout_collection.insert_one(checkout_data).inserted_id
        
        orders_collection.insert_one({
            "order_id": str(order_id),
            "customer_email": checkout_data["email"],
            "total_amount": checkout_data["total"],
            "items": len(checkout_data["cart"]),
            "order_date": checkout_data["checkout_date"],
            "status": "confirmed"
        })
        
        session.pop("cart", None)
        return redirect(url_for("order_confirmation", order_id=str(order_id)))
    
    cart = session.get("cart", [])
    if not cart:
        return redirect(url_for("cart"))
        
    subtotal = sum(item["price"] for item in cart)
    shipping = 8.00
    tax = 0.00
    total = subtotal + shipping + tax
    
    delivery_date = (datetime.now() + timedelta(days=3)).strftime("%a, %b %d")
    
    return render_template("checkout.html", 
                         cart=cart,
                         subtotal=subtotal,
                         shipping=shipping,
                         tax=tax,
                         total=total,
                         delivery_date=delivery_date)

@app.route("/order_confirmation/<order_id>")
def order_confirmation(order_id):
    order = checkout_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        return redirect(url_for("home"))
    
    return render_template("order_confirmation.html", order=order)

if __name__ == "__main__":

    app.run(debug=True)
