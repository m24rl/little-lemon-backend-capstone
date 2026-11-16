# Little Lemon — Back-End Developer Capstone

Django and Django REST Framework application with a static homepage, menu API, authenticated table reservations, Djoser registration and token login, MySQL configuration, migrations and seven automated tests.

## Set up

Requires Python 3.11+ and MySQL 8.0+. Use a fresh local database for this project.

```console
git clone https://github.com/m24rl/little-lemon-backend-capstone.git
cd little-lemon-backend-capstone
python -m pip install pipenv
pipenv sync
```

Set these environment variables in your shell before running Django:

| Variable | Default |
| --- | --- |
| MYSQL_DATABASE | littlelemon_capstone |
| MYSQL_HOST | 127.0.0.1 |
| MYSQL_PORT | 3306 |
| MYSQL_USER | littlelemon |
| MYSQL_PASSWORD | empty; set your local password |
| DJANGO_SECRET_KEY | random development key; set a persistent secret for deployments |

PowerShell: `$env:MYSQL_PASSWORD='your-local-password'`.
Bash: `export MYSQL_PASSWORD='your-local-password'`.

Create the database and local user in MySQL, replacing the password placeholder:

```sql
CREATE DATABASE littlelemon_capstone CHARACTER SET utf8mb4;
CREATE USER 'littlelemon'@'localhost' IDENTIFIED BY 'YOUR_LOCAL_PASSWORD';
GRANT ALL PRIVILEGES ON littlelemon_capstone.* TO 'littlelemon'@'localhost';
```

Alternatively, if Docker Compose is available, set MYSQL_PASSWORD and MYSQL_ROOT_PASSWORD to local secrets, then run `docker compose up -d db`. Wait for MySQL to finish initializing before migration. The container publishes its port on the local machine only and persists data in a named volume. Do not start it if another MySQL server already occupies port 3306.

```console
pipenv run python manage.py migrate
pipenv run python manage.py loaddata menu
pipenv run python manage.py createsuperuser
pipenv run python manage.py runserver
```

Visit http://127.0.0.1:8000/ for the static homepage. The admin interface is at /admin/.

For an optional preview without MySQL, set DJANGO_USE_SQLITE=1 before migration and startup. Unset it to use MySQL. MySQL is the default backend required by the course. No personal database or credentials are committed.

## API routes

See **Readme.txt** for the required reviewer route list and **requests.http** for sample requests.

| Route | Methods | Access |
| --- | --- | --- |
| /restaurant/menu/ | GET, POST | Public GET; staff POST |
| /restaurant/menu/{id}/ | GET, PUT, PATCH, DELETE | Public GET; staff writes |
| /restaurant/booking/tables/ | GET, POST | Authenticated; customers see their own records |
| /restaurant/booking/tables/{id}/ | GET, PUT, PATCH, DELETE | Owner or staff |
| /auth/users/ | POST | Public registration |
| /auth/users/me/ | GET | Authenticated profile |
| /auth/token/login/ | POST | Username and password |
| /auth/token/logout/ | POST | Authenticated; revokes current token |
| /restaurant/api-token-auth/ | POST | Alternative DRF token endpoint |
| /api/menu/ and /api/bookings/ | Same CRUD as above | Convenience aliases |

Register with username, email, password and re_password. Login returns auth_token. In Insomnia, choose the appropriate method, enter the full URL, set JSON body and Content-Type: application/json, and add `Authorization: Token YOUR_LOCAL_TOKEN` for protected requests. The word **Token**, not Bearer, is required for this configuration. Create separate customer and staff requests to verify permissions. Never commit tokens or passwords to source control.

Menu prices use DecimalField; inventory cannot be negative. Reservations require 1–20 guests and a future timezone-aware date/time, e.g. 2030-01-01T18:00:00Z. The server assigns the owner from request.user. Cross-customer access returns 404 because object lookup uses an owner-filtered queryset. Staff may view and manage all bookings. Write operations return 201 for creation, 200 for updates, 204 for deletion, 400 for invalid data, 401 for missing/invalid token and 403 for insufficient menu-write permissions. GET collections are paginated with count, next, previous and results.

Search menu titles with `?search=pasta`; order by price with `?ordering=price` or `?ordering=-price`; navigate with `?page=2`.

## Validation

```console
pipenv run python manage.py check
pipenv run python manage.py makemigrations --check --dry-run
pipenv run python manage.py test restaurant.tests
```

Seven tests cover model formatting, static HTML rendering, public menu reads, staff-only menu CRUD, price validation, registration, login, token revocation, booking CRUD, owner assignment, cross-user isolation, guest/date validation, search and ordering.

Local automated tests passed using SQLite with DJANGO_USE_SQLITE=1. No MySQL service was installed in the execution environment, so this result does **not** establish a live MySQL connection. MySQL settings and driver are included; configure your own server to verify that backend. For MySQL test databases, the local test user also needs privileges on test_littlelemon_capstone.*. Tests were performed with Django 5.2.19, DRF 3.18.3 and Djoser 2.3.5.

This is a course/development project. Before public deployment, set a persistent secret key, disable debug, restrict allowed hosts, use HTTPS, configure static-file serving and apply the normal Django deployment checks.
