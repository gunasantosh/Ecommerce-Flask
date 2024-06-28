from flask import (
    Blueprint,
    render_template,
    current_app,
    flash,
    request,
    redirect,
    url_for,
)
from website.utils import admin_required
from werkzeug.utils import secure_filename
from website.models import Product, Category
from website import db
import os

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@admin_required
def index():
    return render_template("admin/index.html")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@admin_bp.route("/add-product", methods=["GET", "POST"])
@admin_required
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        category_id = request.form.get("category")
        image_file = request.files.get("image_file")

        if not name or not price or not quantity or not category_id:
            flash("Please fill in all required fields", "error")
            return redirect(url_for("admin.add_product"))

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        else:
            filename = None

        try:
            price = float(price)
            quantity = int(quantity)
            category_id = int(category_id)
        except ValueError:
            flash("Invalid data format", "error")
            return redirect(url_for("admin.add_product"))

        new_product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category_id=category_id,
            image_filename=filename,
        )

        db.session.add(new_product)
        try:
            db.session.commit()
            flash("Product added successfully", "success")
        except Exception as e:
            db.session.rollback()
            flash("Error adding product: " + str(e), "error")

        return redirect(url_for("admin.index"))

    categories = Category.query.all()
    return render_template("admin/add_product.html", categories=categories)


@admin_bp.route("/add-category", methods=["GET", "POST"])
@admin_required
def add_category():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if not name:
            flash("Category name is required", "error")
            return redirect(url_for("admin.add_category"))

        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            flash("Category already exists", "error")
            return redirect(url_for("admin.add_category"))

        new_category = Category(name=name, description=description)
        db.session.add(new_category)
        try:
            db.session.commit()
            flash("Category added successfully", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding category: {e}", "error")

        return redirect(url_for("admin.list_categories"))

    return render_template("admin/add_category.html")


@admin_bp.route("/categories")
@admin_required
def list_categories():
    categories = Category.query.all()
    return render_template("admin/list_categories.html", categories=categories)
