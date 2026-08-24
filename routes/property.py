import os

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from extensions import db
from models.property import Property, PropertyImage

property_bp = Blueprint("property", __name__, url_prefix="/properties")


UPLOAD_FOLDER = "static/uploads/properties"

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@property_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_property():

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        price = request.form.get("price")
        property_type = request.form.get("property_type")
        listing_type = request.form.get("listing_type")
        location = request.form.get("location")
        bedrooms = request.form.get("bedrooms")
        bathrooms = request.form.get("bathrooms")
        area = request.form.get("area")

        # Basic validation
        if not all([
            title,
            description,
            price,
            property_type,
            listing_type,
            location,
            bedrooms,
            bathrooms,
            area
        ]):
            flash("Please fill in all fields.", "error")
            return redirect(url_for("property.add_property"))

        # Create property
        new_property = Property(
            owner_id=current_user.id,
            title=title,
            description=description,
            price=price,
            property_type=property_type,
            listing_type=listing_type,
            location=location,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area=area
        )

        db.session.add(new_property)
        db.session.commit()

        # Create upload folder if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Handle multiple images
        images = request.files.getlist("images")

        for image in images:

            if image and allowed_file(image.filename):

                filename = secure_filename(image.filename)

                image_path = os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )

                image.save(image_path)

                property_image = PropertyImage(
                    property_id=new_property.id,
                    image_path=image_path
                )

                db.session.add(property_image)

        db.session.commit()

        flash("Property added successfully!", "success")

        return redirect(
            url_for("property.my_properties")
        )

    return render_template("add_property.html")


@property_bp.route("/my-properties")
@login_required
def my_properties():

    properties = Property.query.filter_by(
        owner_id=current_user.id
    ).all()

    return render_template(
        "properties.html",
        properties=properties
    )