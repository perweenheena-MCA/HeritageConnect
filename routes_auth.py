from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User

bp_auth = Blueprint("auth", __name__)


@bp_auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("auth.register"))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("User already exists.", "error")
            return redirect(url_for("auth.register"))

        u = User(username=username, email=email)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        login_user(u)
        return redirect(url_for("pages.landing"))

    return render_template("auth/register.html")


@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        u = User.query.filter_by(username=username).first()
        if not u or not u.check_password(password):
            flash("Invalid credentials.", "error")
            return redirect(url_for("auth.login"))

        login_user(u)
        return redirect(url_for("pages.landing"))

    return render_template("auth/login.html")


@bp_auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("pages.landing"))


@bp_auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.username = request.form.get("username", current_user.username)
        current_user.email = request.form.get("email", current_user.email)
        current_user.language = request.form.get("language", current_user.language)
        db.session.commit()
        flash("Profile updated.", "success")

    # ensure templates can use latest user
    return render_template("auth/profile.html")

