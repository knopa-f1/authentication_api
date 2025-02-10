# Authentication API

This is a RESTful API for user authentication and authorization, built with Django and Django REST Framework. It uses JWT tokens for authentication, where the access token is verified without database calls, and the refresh token is stored in the database.

## Features
- User registration and login
- JWT-based authentication (access and refresh tokens)
- Token refreshing and logout
- User profile retrieval and update
- Configuration of token lifetimes using `django-constance`
- Browsable API for easy testing

## Technologies Used
- Django
- Django REST Framework
- PyJWT
- PostgreSQL
- Gunicorn

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/knopa-f1/authentication-api.git
   cd authentication-api
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables in a `.env` file:
   ```env
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   ALLOWED_HOSTS=127.0.0.1,localhost
   ````
5. Apply migrations:
   ```sh
   python manage.py migrate
   ```
6. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints

| Method | Endpoint         | Description |
|--------|-----------------|-------------|
| POST   | `/api/register` | Register a new user |
| POST   | `/api/login`    | Authenticate and get access & refresh tokens |
| POST   | `/api/refresh`  | Get a new access token using a refresh token |
| POST   | `/api/logout`   | Logout and invalidate the refresh token |
| GET    | `/api/me`       | Retrieve user profile |
| PUT    | `/api/me`       | Update user profile |

### Example Request: Register a User
```sh
curl -X POST http://127.0.0.1:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"email": "newuser@example.com", "password": "securepassword"}'
```

### Example Request: Get a New Access Token
```sh
curl -X POST http://127.0.0.1:8000/api/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh_token": "your_refresh_token_here"}'
```

## Running Tests
To run tests, use:
```sh
pytest
```

## Admin Panel
The Django admin panel is available at:
```
https://name-of-your-service.com/admin/
```
Use the superuser credentials created earlier to log in.
