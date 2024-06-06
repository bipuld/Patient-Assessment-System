## Overview
This Patients Assessment System is used to effectively store data of the patients with their assessment that supports the multi-tenancy features (Different clinical users can maintain their record of patients easily)

## Tech Stack 
Backend: Django
API: Django REST Framework
Database: MySQL (for localhost development)

## Project Structure
The project follows a structured approach to effectively manage patient records and their Assessment . It includes the following components:
- **User Profile Management:** Allows users to create profiles with necessary information also login,logout,get profile.
- **Patient Record Management:** Enables users to perform CRUD operations on patient records.
- **Assessment Record Management:** CRUD on Assessment records associated with patients details
-  **Clinician Role:** Roles of clinician with patients and Assessment Records

### Features
- **User Authentication:** Secure user authentication system with JWT tokens.
- **User Profile Creation:** Creation of user profiles with essential details.
- **Patient Record Management:** CRUD operations for managing patient records.
- **Assessment Record Management:** Ensure that each clinician can only access Assessment records associated with their patients
- **Seamless Features:** Enable clinicians to view and update patient assessments seamlessly.
- **Maintain Relationship:** Establish a clear link between clinicians and their respective patients.


## Assumptions made during this development of Patients Assessment System.
some of them are mentions below:

1.Data entry done by the clinical user for the patient should be consistent. T
2.The system assumes that the patients’ records are updated regularly with thier correct information. 
3.This system assumes that all users will not violate data privacy regulations and will not misuse patient information. 
4.The system assumes that a stable and good internet connection is available to maintain and access records without any breakage. 
5.Data integrity should be handled by the user. 

## Challenges faced during development and how I overcame them
Challenges faced during development Process:
1.Multi-Tenancy Features: 
Problem: I faced issues with how to enable multiple clinicians to maintain records seamlessly without any loopholes. 
Solution: The solution was achieved by designing the architecture of the database to work easily. Different clinicians can have relationships with patients. Through logical thinking about their relationship and testing multiple times, I met that solution . 

2.Deployment Process to AWS: 
Problem: I faced issues during the deployment process phase to write. 
Solution: I conducted research on deploying a Django project on AWS. I consulted different blogs and posts, and finally, I reached a solution. 

## Additional features implement in this project:
In the Admin panel, which is handled by the user, the viewing of the patients’ records is quite impressive.
It includes filters for date, type, clinicians, and more. This allows for an easy view of the relationship with the user who created them.
Also, for viewing assessment records in the admin panel, I have implemented filtering by clinician, date, and assessment type, and show counts. This makes the system more efficient and user-friendly.

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

### Assessment 
- **Assessment Management:** `GET/POST/PUT/DELETE /patients/api/assessment/` - CRUD operations for managing patient records.

### Getting all the Clincian Available in Our Record 
- **Clincian Record:** '`GET /patients/api/ListClinician/` - Getting all the Clinician Data available in our record

### Creating the Clincian For the user 
- **Clincian Record:** '`POST /patients/api/ClinicianCreate/` - Create all the Clinician for the User

### Getting Specific Patients data with their specific clincian  
- **Clincian Record:** '`GET /patients/api/patient-clinician/` - Getting all the Patients data of Specific clinican (if it is created with that user )


## Description
This project provides setup instructions for local development.

## Setup Instructions
1. **Clone the Project**: `git clone <repository_url>`
2. **Create and Activate Virtual Environment**:
    - Windows: `python -m venv env` && `.\env\Scripts\activate`
    - Linux/Mac: `python -m venv env` && `source env/bin/activate`
    - goto project directory cd project_dir
3. **Install Project Dependencies**: `pip install -r requirements.txt`
4. **Configure Database**: Update `DATABASES` settings in `project_name/settings.py` with DB_NAME,USER,PASSWORD.
5. **Apply Migrations**: `python manage.py makemigrations` && `python manage.py migrate`
6. **Run Development Server**: `python manage.py runserver`
7. **Create Admin User**: `python manage.py createsuperuser` for admin panel
