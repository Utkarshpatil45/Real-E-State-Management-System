from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models.user import User


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "error")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            phone=phone
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")

# login
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            flash("Login successful!", "success")

            return redirect(url_for("auth.dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")

# logout
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))

# dashboard
@auth.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")
# @auth.route("/dashboard")
# @login_required
# def dashboard():

#     return f"""
#         <h1>Welcome, {current_user.name}!</h1>
#         <p>Email: {current_user.email}</p>
#         <p>Role: {current_user.role}</p>

#         <a href="{url_for('auth.logout')}">Logout</a>
#     """