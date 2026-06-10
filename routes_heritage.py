import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models import HeritageContent, Category, Region

bp_heritage = Blueprint("heritage", __name__)

UPLOAD_DIR = os.path.join("static", "uploads")


def ai_like_categorize(title, description, category_id=None):
    text = f"{title} {description}".lower()
    tag_bank = [
        ("folk", "folk"),
        ("tale", "tales"),
        ("festival", "festival"),
        ("dance", "dance"),
        ("craft", "craft"),
        ("tradition", "traditions"),
        ("legend", "legends"),
        ("ritual", "ritual"),
        ("music", "music"),
        ("drums", "drums"),
        ("race", "race"),
        ("story", "story"),
    ]

    tags = {v for k, v in tag_bank if k in text}
    if not tags:
        tags = {"heritage", "culture"}

    categories_guess = []
    if "festival" in text or "drum" in text or "procession" in text:
        categories_guess.append("Festivals")
    if "folk" in text or "legend" in text or "tale" in text:
        categories_guess.append("Folk Tales")
    if "dance" in text or "craft" in text:
        categories_guess.append("Regional Arts")
    if "tradition" in text or "ritual" in text or "custom" in text:
        categories_guess.append("Regional Traditions")
    if not categories_guess:
        categories_guess.append("Regional Traditions")

    summary = " ".join((title or "").strip().split()[:10])
    if description:
        summary = (description.strip()[:160] + ("..." if len(description.strip()) > 160 else ""))

    return ",".join(sorted(tags)), ",".join(categories_guess), summary


@bp_heritage.route("/contribute", methods=["GET", "POST"])
@login_required
def upload():
    categories = Category.query.order_by(Category.name).all()
    regions = Region.query.order_by(Region.name).all()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category_id = request.form.get("category_id") or None
        region_id = request.form.get("region_id") or None
        content_type = request.form.get("content_type", "story")

        if not title:
            flash("Title is required.", "error")
            return redirect(url_for("heritage.upload"))

        category_id = int(category_id) if category_id else None
        region_id = int(region_id) if region_id else None

        suggested_tags, suggested_categories, summary = ai_like_categorize(title, description, category_id=category_id)

        # image upload
        file = request.files.get("image")
        filename = None
        if file and file.filename:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_DIR, filename))

        hc = HeritageContent(
            title=title,
            description=description,
            summary=summary,
            suggested_tags=suggested_tags,
            suggested_categories=suggested_categories,
            image_filename=filename,
            category_id=category_id,
            region_id=region_id,
            content_type=content_type,
            is_approved=False,
            views=0,
            author_id=current_user.id,
        )
        db.session.add(hc)
        db.session.commit()
        flash("Submission received. It will appear after admin approval.", "success")
        return redirect(url_for("archive.browse"))

    return render_template("heritage/upload.html", categories=categories, regions=regions)

