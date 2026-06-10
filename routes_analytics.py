from flask import Blueprint, render_template
from flask_login import login_required
from extensions import db
from models import User, HeritageContent, Region

bp_analytics = Blueprint("analytics", __name__)


@bp_analytics.route("/dashboard")
@login_required
def dashboard():
    total_contributions = HeritageContent.query.count()
    total_users = User.query.count()
    most_viewed = HeritageContent.query.order_by(HeritageContent.views.desc()).limit(5).all()

    regions = Region.query.all()
    most_active_regions = []
    for r in regions:
        count = HeritageContent.query.filter_by(region_id=r.id, is_approved=True).count()
        most_active_regions.append((r, count))
    most_active_regions.sort(key=lambda x: x[1], reverse=True)

    return render_template(
        "analytics/dashboard.html",
        total_contributions=total_contributions,
        total_users=total_users,
        most_viewed=most_viewed,
        most_active_regions=most_active_regions[:5],
    )

