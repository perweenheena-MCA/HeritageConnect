from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    language = db.Column(db.String(10), default="en", nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    comments = db.relationship("Comment", backref="author", lazy=True)
    likes = db.relationship("Like", backref="user", lazy=True)
    bookmarks = db.relationship("Bookmark", backref="user", lazy=True)
    heritage_contents = db.relationship("HeritageContent", backref="author", lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id: str):
    try:
        return User.query.get(int(user_id))
    except Exception:
        return None


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class Region(db.Model):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=False, default=0.0)
    lng = db.Column(db.Float, nullable=False, default=0.0)


class HeritageContent(db.Model):
    __tablename__ = "heritage_contents"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)

    # “AI” generated fields (deterministic stub)
    summary = db.Column(db.Text, nullable=True)
    suggested_tags = db.Column(db.Text, nullable=True)  # comma-separated
    suggested_categories = db.Column(db.Text, nullable=True)

    image_filename = db.Column(db.String(255), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"), nullable=True)

    content_type = db.Column(db.String(50), default="story", nullable=False)  # story, festival, tradition

    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    views = db.Column(db.Integer, default=0, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    comments = db.relationship("Comment", backref="heritage", lazy=True, cascade="all, delete-orphan")


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey("heritage_contents.id"), nullable=False, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    body = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey("heritage_contents.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    __table_args__ = (db.UniqueConstraint("heritage_id", "user_id", name="uq_like"),)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Bookmark(db.Model):
    __tablename__ = "bookmarks"

    id = db.Column(db.Integer, primary_key=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey("heritage_contents.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    __table_args__ = (db.UniqueConstraint("heritage_id", "user_id", name="uq_bookmark"),)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

