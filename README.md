# HeritageConnect (Hackathon)

AI-powered cultural preservation & education platform.

## Features
- Auth: register/login/logout + profile
- Upload heritage content (stories/festivals/traditions)
- AI-like categorization stub (deterministic keywords)
- Browse/search/filter archive by category/region/tags
- Cultural map with region markers
- Community: like, bookmark, comments
- Multilingual UI switcher (simple dictionary-based)
- Admin dashboard: approve/delete/manage
- Analytics dashboard

## Setup
### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Initialize database + sample data
```bash
python init_db.py
```

### 3) Run the app
```bash
python app.py
```

Then open: `http://127.0.0.1:5000`

## Notes
- Uploaded images are stored in `static/uploads/`.
- AI categorization is a deterministic stub to keep this hackathon-friendly.

