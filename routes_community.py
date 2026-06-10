from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import HeritageContent, Like, Bookmark, Comment

bp_community = Blueprint("community", __name__)


@bp_community.route("/heritage/<int:heritage_id>/like", methods=["POST"])
@login_required
def like(heritage_id):
    hc = HeritageContent.query.filter_by(id=heritage_id, is_approved=True).first_or_404()
    existing = Like.query.filter_by(heritage_id=hc.id, user_id=current_user.id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
    else:
        db.session.add(Like(heritage_id=hc.id, user_id=current_user.id))
        db.session.commit()
    return redirect(url_for("archive.detail", heritage_id=hc.id))


@bp_community.route("/heritage/<int:heritage_id>/bookmark", methods=["POST"])
@login_required
def bookmark(heritage_id):
    hc = HeritageContent.query.filter_by(id=heritage_id, is_approved=True).first_or_404()
    existing = Bookmark.query.filter_by(heritage_id=hc.id, user_id=current_user.id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
    else:
        db.session.add(Bookmark(heritage_id=hc.id, user_id=current_user.id))
        db.session.commit()
    return redirect(url_for("archive.detail", heritage_id=hc.id))


@bp_community.route("/heritage/<int:heritage_id>/comment", methods=["POST"])
@login_required
def comment(heritage_id):
    hc = HeritageContent.query.filter_by(id=heritage_id, is_approved=True).first_or_404()
    body = request.form.get("body", "").strip()
    if not body:
        flash("Comment cannot be empty.", "error")
        return redirect(url_for("archive.detail", heritage_id=hc.id))

    c = Comment(heritage_id=hc.id, user_id=current_user.id, body=body)
    db.session.add(c)
    db.session.commit()
    return redirect(url_for("archive.detail", heritage_id=hc.id))

