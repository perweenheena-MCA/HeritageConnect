from flask import Flask
from config import Config
from extensions import db, login_manager
from models import User  # noqa

# Blueprints
from routes_auth import bp_auth
from routes_heritage import bp_heritage
from routes_archive import bp_archive
from routes_map import bp_map
from routes_community import bp_community
from routes_admin import bp_admin
from routes_analytics import bp_analytics
from routes_pages import bp_pages


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(bp_pages)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_heritage)
    app.register_blueprint(bp_archive)
    app.register_blueprint(bp_map)
    app.register_blueprint(bp_community)
    app.register_blueprint(bp_admin, url_prefix="/admin")
    app.register_blueprint(bp_analytics, url_prefix="/analytics")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

