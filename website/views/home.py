from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from website.models import Product, Cart, User
from website import db
import json

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    products = Product.query.all()
    return render_template("home/index.html", products=products)


@home_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if "user" not in session:
        flash("Please log in to add items to the cart.", "warning")
        return redirect(url_for("auth.login"))

    user_email = session["user"]["userinfo"]["email"]
    user = User.query.filter_by(email=user_email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    product = Product.query.get_or_404(product_id)

    if product.quantity < 1:
        flash("This product is out of stock.", "danger")
        return redirect(url_for("home.index"))

    cart_item = Cart.query.filter_by(user_id=user.id, product_id=product_id).first()

    if cart_item:
        if product.quantity < cart_item.quantity + 1:
            flash("Not enough stock available.", "danger")
            return redirect(url_for("home.index"))
        cart_item.quantity += 1
    else:
        new_cart_item = Cart(user_id=user.id, product_id=product_id)
        db.session.add(new_cart_item)

    db.session.commit()
    flash("Item added to cart!", "success")
    return redirect(url_for("home.index"))


@home_bp.route("/cart")
def view_cart():
    if "user" not in session:
        flash("Please log in to view your cart.", "warning")
        return redirect(url_for("auth.login"))

    user_email = session["user"]["userinfo"]["email"]
    user = User.query.filter_by(email=user_email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    cart_items = Cart.query.filter_by(user_id=user.id).all()
    return render_template("home/cart.html", cart_items=cart_items)


@home_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "user" not in session:
        flash("Please log in to proceed with the checkout.", "warning")
        return redirect(url_for("auth.login"))

    user_email = session["user"]["userinfo"]["email"]
    user = User.query.filter_by(email=user_email).first()

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    cart_items = Cart.query.filter_by(user_id=user.id).all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        delivery_address = request.form.get("delivery_address")
        coupon_code = request.form.get("coupon_code")

        if not delivery_address:
            flash("Delivery address is required.", "danger")
            return redirect(url_for("home.checkout"))

        # Apply coupon code logic (if any)
        discount = 0
        if coupon_code == "SAVE10":
            discount = 0.10 * total_amount

        final_amount = total_amount - discount

        # Here you would typically handle the payment processing
        # For simplicity, we just clear the cart and show a success message
        Cart.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        flash(
            f"Checkout successful! Your total payment is ${final_amount:.2f}. Thank you for your purchase.",
            "success",
        )
        return redirect(url_for("home.index"))

    return render_template(
        "home/checkout.html", cart_items=cart_items, total_amount=total_amount
    )
