from flask import Blueprint, render_template, request
from extensions import db
from models import HeritageContent, Category, Region

bp_archive = Blueprint("archive", __name__)


@bp_archive.route("/archive")
def browse():
    # Filters
    category_id = request.args.get("category_id")
    region_id = request.args.get("region_id")
    q = request.args.get("q", "").strip()

    query = HeritageContent.query.filter_by(is_approved=True)

    if category_id:
        query = query.filter(HeritageContent.category_id == int(category_id))
    if region_id:
        query = query.filter(HeritageContent.region_id == int(region_id))
    if q:
        like = f"%{q}%"
        query = query.filter(
            (HeritageContent.title.ilike(like)) | (HeritageContent.description.ilike(like))
        )

    # tags filter: comma-separated in suggested_tags
    tag = request.args.get("tag")
    if tag:
        query = query.filter(HeritageContent.suggested_tags.ilike(f"%{tag}%"))

    categories = Category.query.order_by(Category.name).all()
    regions = Region.query.order_by(Region.name).all()

    contents = query.order_by(HeritageContent.created_at.desc()).all()

    return render_template(
        "archive/browse.html",
        contents=contents,
        categories=categories,
        regions=regions,
        selected_category_id=category_id,
        selected_region_id=region_id,
        q=q,
        tag=tag,
    )


@bp_archive.route("/archive/<int:heritage_id>")
def detail(heritage_id: int):
    hc = HeritageContent.query.filter_by(id=heritage_id, is_approved=True).first_or_404()
    hc.views += 1
    db.session.commit()

    like_count = len(hc.likes) if hasattr(hc, "likes") else None
    return render_template("heritage/detail.html", hc=hc)

