LITTLE LEMON — CAPSTONE REVIEWER GUIDE

Base URL: http://127.0.0.1:8000

Routes to test:
GET /
GET /restaurant/
GET /restaurant/menu/
POST /restaurant/menu/                     (staff token)
GET /restaurant/menu/1/
PUT /restaurant/menu/1/                    (staff token)
PATCH /restaurant/menu/1/                  (staff token)
DELETE /restaurant/menu/1/                 (staff token)
POST /auth/users/                          (registration)
POST /auth/token/login/                    (login)
GET /auth/users/me/                        (token)
POST /auth/token/logout/                   (token)
POST /restaurant/api-token-auth/           (alternative token login)
GET, POST /restaurant/booking/tables/      (token)
GET, PUT, PATCH, DELETE /restaurant/booking/tables/1/ (owner/staff token)
GET /api/menu/                            (alias)
GET, POST /api/bookings/                   (alias)
GET /admin/                               (Django staff login)

Authentication header: Authorization: Token YOUR_LOCAL_TOKEN
Registration JSON: username, email, password, re_password.
Login JSON: username, password.
Menu JSON: {"title":"Pasta","price":"12.50","inventory":20}
Booking JSON: {"name":"Ada","no_of_guests":2,"booking_date":"2030-01-01T18:00:00Z"}

Dates must be in the future. Menu writes require staff privileges.
Booking ownership is assigned from the authenticated user, never trusted from JSON.
Customers cannot retrieve or modify another customer's bookings.
Public menu reads work without authentication.

Install dependencies with pipenv sync; configure MySQL using README.md.
Apply migrations, load the menu fixture and create your own superuser.
Run tests with: pipenv run python manage.py test restaurant.tests
Seven automated tests passed locally on SQLite. Live MySQL testing is pending a local server.
See README.md for setup and expected status codes, requests.http for Insomnia examples.
