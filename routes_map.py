from flask import Blueprint, render_template
from models import Region, HeritageContent

bp_map = Blueprint("map", __name__)


@bp_map.route("/map")
def show_map():
    regions = Region.query.order_by(Region.name).all()
    # Count approved content per region
    region_stats = []
    for r in regions:
        count = HeritageContent.query.filter_by(region_id=r.id, is_approved=True).count()
        region_stats.append((r, count))

    return render_template("map.html", region_stats=region_stats)

