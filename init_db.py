import os
from app import create_app
from extensions import db
from models import User, Category, Region, HeritageContent
from datetime import datetime


def seed():
    # Users
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", email="admin@example.com", is_admin=True, is_active=True)
        admin.set_password("admin123")
        db.session.add(admin)

    alice = User.query.filter_by(username="alice").first()
    if not alice:
        alice = User(username="alice", email="alice@example.com", is_admin=False, is_active=True)
        alice.set_password("alice123")
        db.session.add(alice)

    db.session.flush()

    # Categories
    categories = ["Folk Tales", "Festivals", "Regional Arts", "Regional Traditions"]
    cat_objs = {}
    for name in categories:
        obj = Category.query.filter_by(name=name).first()
        if not obj:
            obj = Category(name=name)
            db.session.add(obj)
        cat_objs[name] = obj

    # Regions (demo coordinates)
    regions = [
        ("Uttarakhand", 30.0668, 79.0193),
        ("Rajasthan", 26.9124, 75.7873),
        ("Karnataka", 12.9716, 77.5946),
    ]
    reg_objs = {}
    for name, lat, lng in regions:
        obj = Region.query.filter_by(name=name).first()
        if not obj:
            obj = Region(name=name, lat=lat, lng=lng)
            db.session.add(obj)
        reg_objs[name] = obj

    db.session.flush()

    # Heritage content
    def add_heritage(title, description, category_name, region_name, content_type, approved):
        existing = HeritageContent.query.filter_by(title=title).first()
        if existing:
            return
        hc = HeritageContent(
            title=title,
            description=description,
            summary=(description[:140] + "...") if description else None,
            suggested_tags="story, heritage, local",
            suggested_categories=category_name,
            image_filename=None,
            category_id=cat_objs[category_name].id if category_name else None,
            region_id=reg_objs[region_name].id if region_name else None,
            content_type=content_type,
            is_approved=approved,
            views=0,
            author_id=alice.id,
        )
        db.session.add(hc)

    add_heritage(
        "The Legend of the Nanda Devi",
        "A folk tale describing the protective spirit of Nanda Devi and the mountains that guard villages.",
        "Folk Tales",
        "Uttarakhand",
        "story",
        True,
    )
    add_heritage(
        "Desert Drums: Jaisalmer Folk Festival",
        "Festival notes on folk music, camel processions, and nighttime storytelling across the dunes.",
        "Festivals",
        "Rajasthan",
        "festival",
        True,
    )
    add_heritage(
        "Kambala: The Tradition of Buffalo Racing",
        "Regional tradition highlighting community gatherings, preparation rituals, and local craftsmanship.",
        "Regional Traditions",
        "Karnataka",
        "tradition",
        False,
    )

    db.session.commit()


def main():
    app = create_app()
    with app.app_context():
        # ensure uploads dir
        os.makedirs(os.path.join(app.static_folder, "uploads"), exist_ok=True)
        seed()
        print("Database initialized with sample data.")


if __name__ == "__main__":
    main()

