from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models import HeritageContent, User

bp_admin = Blueprint("admin", __name__)


def require_admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Admin access required.", "error")
        return False
    return True


@bp_admin.route("/dashboard")
@login_required
def dashboard():
    if not require_admin():
        return redirect(url_for("pages.landing"))

    pending = HeritageContent.query.filter_by(is_approved=False).order_by(HeritageContent.created_at.desc()).all()
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/dashboard.html", pending=pending, users=users)


@bp_admin.route("/approve/<int:heritage_id>", methods=["POST"])
@login_required
def approve(heritage_id):
    if not require_admin():
        return redirect(url_for("pages.landing"))

    hc = HeritageContent.query.filter_by(id=heritage_id).first_or_404()
    hc.is_approved = True
    db.session.commit()
    flash("Submission approved.", "success")
    return redirect(url_for("admin.dashboard"))


@bp_admin.route("/delete/<int:heritage_id>", methods=["POST"])
def delete(heritage_id):
    if not require_admin():
        return redirect(url_for("pages.landing"))

    hc = HeritageContent.query.filter_by(id=heritage_id).first_or_404()
    db.session.delete(hc)
    db.session.commit()
    flash("Submission deleted.", "success")
    return redirect(url_for("admin.dashboard"))

