# Django Blog with Authentication & REST API

A full-featured, production-deployed blog platform built with Django — featuring user authentication, a complete REST API, third-party service integrations, and real production debugging.

🔗 **Live demo:** https://django-blog-app-production-58e4.up.railway.app

## Features
- User authentication (signup, login, logout) — anyone can create an account and start writing
- Full CRUD for posts: create, edit, delete — restricted to each post's original author
- Categorized posts (Lifestyle, Business, Tech, Health, Other)
- Image uploads per post, stored on Cloudinary (persistent, independent of server storage)
- Commenting system — logged-in users only, with dual permissions: a comment can be deleted by either its author or the post's author
- Complete REST API (GET, POST, PUT, PATCH, DELETE) for both posts and comments, secured with token authentication
- Public read access, authenticated write access (`IsAuthenticatedOrReadOnly`)
- PostgreSQL database in production (persistent across deploys)
- Backend validation on every form — no client-side-only checks

## Tech Stack
- Python, Django 6.0
- Django REST Framework (token authentication, serializers)
- PostgreSQL (production), SQLite (local development)
- Cloudinary (image storage)
- Whitenoise (static file serving)
- Gunicorn (production WSGI server)
- Deployed on Railway

## What I Learned
This project took me from basic CRUD to real production engineering. Beyond Django fundamentals (models, views, templates, `ForeignKey` relationships across Post/Comment/User), I built:
- A full REST API with DRF, including token auth and object-level permissions (e.g., only a post's author can edit it — enforced both in the web views and independently in the API)
- File upload handling (`ImageField`, `request.FILES`) and its production complications — Railway's ephemeral filesystem wipes uploaded files on every redeploy, which I solved by integrating Cloudinary for persistent external storage
- Production deployment end-to-end: environment variables, `DEBUG`/`SECRET_KEY` handling, HTTPS/CSRF trusted origins, PostgreSQL setup, and Railway's internal vs. public networking

**Real production bugs I debugged and fixed independently:**
- A silent `collectstatic` failure caused by a third-party package (`django-cloudinary-storage`) overriding Django's built-in management command based on an unrelated settings value — diagnosed by manually replicating Django's internal file-collection logic in the shell to isolate where the real command was silently skipping every file
- Django 6.0's newer `STORAGES` dictionary setting silently superseding the older `DEFAULT_FILE_STORAGE` setting — meaning Cloudinary credentials loaded correctly but were never actually used, until traced via `default_storage.__class__` inspection
- A database persistence bug where Railway's internal service networking failed to resolve, fixed by switching to public networking for the PostgreSQL connection

## Running Locally
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the project root with:
    DEBUG=True
    SECRET_KEY=your-generated-secret-key
    CLOUDINARY_CLOUD_NAME=your-cloud-name
    CLOUDINARY_API_KEY=your-api-key
    CLOUDINARY_API_SECRET=your-api-secret
        (Generate a secret key with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
        
4. Run migrations: `python manage.py migrate`
5. Create an account: `python manage.py createsuperuser` (or sign up via `/signup/`)
6. Start the server: `python manage.py runserver`
7. Visit `http://127.0.0.1:8000/`

## API Endpoints
| Endpoint | Methods | Auth |
|---|---|---|
| `/api/posts/` | GET, POST | Read: public · Write: token required |
| `/api/posts/<id>/` | GET, PUT, PATCH, DELETE | Read: public · Write: author only |
| `/api/comments/` | GET, POST | Read: public · Write: token required |
| `/api/comments/<id>/` | GET, PUT, DELETE | Read: public · Write: comment or post author |
| `/api/login/` | POST | Returns auth token for valid credentials |


## Testing
Includes unit tests (Django's `TestCase`) covering core authentication and permission logic:
- Authenticated users can create posts; unauthenticated users cannot
- Non-authors are blocked from deleting posts they don't own

Run tests with:
```
python manage.py test
```