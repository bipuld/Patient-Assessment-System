## Overview
The Patient Assessment System is a project designed to efficiently manage patient records. It provides functionalities for creating, updating, and deleting patient records, along with other essential features.

## Project Structure
The project follows a structured approach to effectively manage user profiles and patient records. It includes the following components:

- **User Profile Management:** Allows users to create profiles with necessary information.
- **Patient Record Management:** Enables users to perform CRUD operations on patient records.

### Features
- **User Authentication:** Secure user authentication system with JWT tokens.
- **User Profile Creation:** Creation of user profiles with essential details.
- **Patient Record Management:** CRUD operations for managing patient records.

### Endpoints
#### User Authentication
- **Signup:** `POST /api/signup/` - Create a new user account.
- **Login:** `POST /api/login/` - Authenticate user and retrieve JWT access token.
- **Get User Profile:** `GET /api/get-profile/` - Retrieve user profile information.
- **Logout:** `POST /api/logout/` - Invalidate JWT access token and logout.

#### JWT Token Management
- **Token Refresh:** `POST /api/login-token/refresh/` - Refresh JWT access token.
- **Token Verify:** `POST /api/login-token/verify/` - Verify JWT access token.

#### Patients
- **Patients Management:** `GET/POST/PUT/DELETE /patients/` - CRUD operations for managing patient records.

## Description
This project provides setup instructions for local development.

## Setup Instructions
1. **Clone the Project**: `git clone <repository_url>`
2. **Create and Activate Virtual Environment**:
    - Windows: `python -m venv env` && `.\env\Scripts\activate`
    - Linux/Mac: `python -m venv env` && `source env/bin/activate`
3. **Install Project Dependencies**: `pip install -r requirements.txt`
4. **Configure Database**: Update `DATABASES` settings in `project_name/settings.py` or `.env`.
5. **Apply Migrations**: `python manage.py makemigrations` && `python manage.py migrate`
6. **Run Development Server**: `python manage.py runserver`
7. **Create Admin User**: `python manage.py createsuperuser`

## Contributing
Contributions are welcome! Refer to CONTRIBUTING.md for guidelines.

## License
Th