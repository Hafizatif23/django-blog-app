# Django Blog with Authentication

A full-featured blog application built with Django, featuring user authentication, categorized posts, image uploads, and comments.

## Features
- User authentication (signup via Django admin, login/logout)
- Create, edit, and delete blog posts — restricted to the post's original author
- Categorize posts (Lifestyle, Business, Tech, Health, Other)
- Optional image upload per post
- Commenting system, restricted to logged-in users
- Post list and individual post detail pages
- Backend validation on all forms (posts and comments)

## Tech Stack
- Python
- Django
- SQLite
- Pillow (image handling)
- HTML/CSS

## What I Learned
This was my third Django project, and the first to include real authentication and file handling. Key concepts covered: Django's built-in auth system (`@login_required`, `request.user`), enforcing object-level permissions (users can only edit their own posts), `ForeignKey` relationships between models (Post→User, Comment→Post, Comment→User), and image uploads (`ImageField`, `request.FILES`, media file configuration).

## Running Locally
1. Clone the repo
2. Install dependencies: `pip install django pillow`
3. Run migrations: `python manage.py migrate`
4. Create an admin/test account: `python manage.py createsuperuser`
5. Start the server: `python manage.py runserver`
6. Visit `http://127.0.0.1:8000/`