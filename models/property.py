# import os

# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from flask_login import login_required, current_user
# from werkzeug.utils import secure_filename

# from extensions import db
# from models.property import Property, PropertyImage

# property_bp = Blueprint("property", __name__, url_prefix="/properties")


# UPLOAD_FOLDER = "static/uploads/properties"

# ALLOWED_EXTENSIONS = {
#     "png",
#     "jpg",
#     "jpeg",
#     "webp"
# }


# def allowed_file(filename):
#     return (
#         "." in filename
#         and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
#     )


# @property_bp.route("/add", methods=["GET", "POST"])
# @login_required
# def add_property():

#     if request.method == "POST":

#         title = request.form.get("title")
#         description = request.form.get("description")
#         price = request.form.get("price")
#         property_type = request.form.get("property_type")
#         listing_type = request.form.get("listing_type")
#         location = request.form.get("location")
#         bedrooms = request.form.get("bedrooms")
#         bathrooms = request.form.get("bathrooms")
#         area = request.form.get("area")

#         # Basic validation
#         if not all([
#             title,
#             description,
#             price,
#             property_type,
#             listing_type,
#             location,
#             bedrooms,
#             bathrooms,
#             area
#         ]):
#             flash("Please fill in all fields.", "error")
#             return redirect(url_for("property.add_property"))

#         # Create property
#         new_property = Property(
#             owner_id=current_user.id,
#             title=title,
#             description=description,
#             price=price,
#             property_type=property_type,
#             listing_type=listing_type,
#             location=location,
#             bedrooms=bedrooms,
#             bathrooms=bathrooms,
#             area=area
#         )

#         db.session.add(new_property)
#         db.session.commit()

#         # Create upload folder if it doesn't exist
#         os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#         # Handle multiple images
#         images = request.files.getlist("images")

#         for image in images:

#             if image and allowed_file(image.filename):

#                 filename = secure_filename(image.filename)

#                 image_path = os.path.join(
#                     UPLOAD_FOLDER,
#                     filename
#                 )

#                 image.save(image_path)

#                 property_image = PropertyImage(
#                     property_id=new_property.id,
#                     image_path=image_path
#                 )

#                 db.session.add(property_image)

#         db.session.commit()

#         flash("Property added successfully!", "success")

#         return redirect(
#             url_for("property.my_properties")
#         )

#     return render_template("add_property.html")


# @property_bp.route("/my-properties")
# @login_required
# def my_properties():

#     properties = Property.query.filter_by(
#         owner_id=current_user.id
#     ).all()

#     return render_template(
#         "my_properties.html",
#         properties=properties
#     )

from extensions import db
from datetime import datetime


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    property_type = db.Column(
        db.String(50),
        nullable=False
    )

    listing_type = db.Column(
        db.String(50),
        nullable=False
    )

    location = db.Column(
        db.String(200),
        nullable=False
    )

    bedrooms = db.Column(
        db.Integer,
        nullable=False
    )

    bathrooms = db.Column(
        db.Integer,
        nullable=False
    )

    area = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="available"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    images = db.relationship(
        "PropertyImage",
        backref="property",
        lazy=True,
        cascade="all, delete-orphan"
    )


class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    image_path = db.Column(
        db.String(255),
        nullable=False
    )