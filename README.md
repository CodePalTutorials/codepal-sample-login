# Django Facebook Registration Project

This project is a Django application that allows users to register and log in using their Facebook account. It also provides an API endpoint to retrieve user details.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the database:**
    This project uses SQLite by default (as per the settings when no `DATABASE_URL` is provided).
    Run migrations to create the necessary database tables:
    ```bash
    python manage.py migrate
    ```
    If you want to use PostgreSQL, set the `DATABASE_URL` environment variable. For example:
    `export DATABASE_URL="postgres://user:password@host:port/dbname"`

5.  **Create a superuser (optional):**
    To access the Django admin interface, create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

## Running the Development Server

1.  **Start the server:**
    ```bash
    python manage.py runserver
    ```
    The application will typically be available at `http://127.0.0.1:8000/`.

## Available API Endpoints

The following API endpoints are available:

*   **`POST /api/v1/user/register/facebook`**:
    *   Registers or logs in a user via their Facebook access token.
    *   Expects a JSON payload with `{"access_token": "your_facebook_access_token", "userID": "facebook_user_id"}`. (Note: Added `userID` as it's used in `registration/views.py`)
    *   Returns an access token in the JSON response and sets it in an HTTP-only cookie.

*   **`GET /api/v1/user/get/account`**:
    *   Retrieves the details of the authenticated user (name, email, Facebook ID).
    *   Requires a valid JWT access token (typically sent in an HTTP-only cookie after login, or in the `Authorization: Bearer <token>` header).

*   **`POST /api/token/`**: (Note: Path changed from `/api-token-auth/` during simplejwt migration)
    *   Obtains JWT tokens (access and refresh). This is the standard endpoint from `rest_framework_simplejwt.views.TokenObtainPairView`.
    *   Expects a JSON payload with `{"username": "your_username", "password": "your_password"}` for users created via Django admin or other means (not Facebook login).

## Running Tests

To run the test suite (currently empty):
```bash
python manage.py test
```
