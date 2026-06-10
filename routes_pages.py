from flask import Blueprint, render_template, request

bp_pages = Blueprint("pages", __name__)

# Simple dictionary-based i18n
I18N = {
    "en": {
        "nav.archive": "Archive",
        "nav.map": "Map",
        "nav.upload": "Contribute",
        "nav.admin": "Admin",
        "nav.analytics": "Analytics",
    },
    "hi": {
        "nav.archive": "आर्काइव",
        "nav.map": "मानचित्र",
        "nav.upload": "योगदान",
        "nav.admin": "प्रशासन",
        "nav.analytics": "एनालिटिक्स",
    },
}


@bp_pages.app_context_processor
def inject_i18n():
    return {"_t": lambda k, lang=None: I18N.get(lang or request.cookies.get("lang", "en"), {}).get(k, I18N["en"].get(k, k))}


@bp_pages.route("/")
def landing():
    return render_template("index.html")


@bp_pages.route("/set-language/<lang>")
def set_language(lang):
    resp = render_template("index.html")
    # For hackathon simplicity we use cookie. (Server-side templates read cookie.)
    resp.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365)
    return resp

