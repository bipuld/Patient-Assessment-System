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
1.Data entry done by the clinical user for the patient should be consistent.
2.The system assumes that the patient’s records are updated regularly with thier correct information. 
3.This system assumes that all users will not violate data privacy regulations and will not misuse patient information. 
4.The system assumes that a stable and good internet connection is available to maintain and access records without any breakage. 
5.Data integrity should be handled by the user. 

## Challenges faced during development and how I overcame them
Challenges faced during development Process:
1.Multi-Tenancy Features: 
Problem: I faced issues with how to enable multiple clinicians to maintain records seamlessly without any loopholes. 
Solution: The solution was achieved by designing the architecture of the database to work easily. Different clinicians can have relationships with patients.Through logical thinking about their relationship and testing multiple times, I met that solution . 

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


## Process of Deploymnet of Django Project on  AWS EC2

This guide thorugh Deploying a django project on AWS EC2 using (Ubuntu + Postgres database ,Nginx and Gunicorn )
Requirments to deploy project on AWS EC2:-
1. **Django project**: Should have django project to host on AWS EC2
2. **Github account** (project in repo) : Should have Githhub account and also must have repo consits of django project 
3. **AWS account** :AWS account should be created for handling instances
4. **Purchased domain** :Should have the domain purchased from the domain provider site.
5. **Cloudfare account** : For Using DNS provided by cloudfare in the domian provider and SSL setup



## Deployment Phases
Here are some phase that fall under the deploymnet of Django Web App on the AWS EC2
1.Django-Github
2.Github
3.AWS AC
4.Domain
5.Cloudfare
6.Setup SSL
7.Testing

### Phase 1 and phase 2 : Setup Django project and Push to Github
Ready our project django for deployment,In my project our system is ready then push to github account

### phase 3 : AWS EC2 (setup):
1. **Creating a AWS instance** 
    - In the AWS account,Create one instances with diffrent configuration such as OS,create also key-pair (.pem)
    - Download in the local storage and other configuration like allows Https and Https 
    - Now instance is created on AWS and connect it and also using cmd we have to change the permission of the (.pem) save file then using cmd given after connecting with instances.
    - We have to  use that cmd(in the directory of the .pem file ) to access our ubuntu server in locally cmd after updiang all package now.  - Clone the git project by using git clone ,make virtualenv ,activate it using bash $ source env/bin/activate ,install requirmentes.txt with cmd 
    - Then in our server the project is ready 
2. **Setup Postgres** 
    - Now Using postgres(As I choose ) i have to install some package on that server using cmd on documentation 
    -- sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
3. **Install Gunicorn on project** 
    - Install Gunicorn package on the project
4. **Migrate Database**
    - Run python manage.py makemigrations and python manage.py migrate.
5. **Testing on server**
    - Running python manage.py runserver if everything works good then go further step 
6. **Configure Gunincorn**
    - Creating System Socket & Service for Gunicorn with cmd provided on documentaion of hosting platform (Such that:https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04) or any user perferences
7. **Configure Nginx**
    - Configure Nginx to Proxy pass to Gunicorn (connecting the Nginx to Gunicorn)
8. **Start and Restart Service of Gunicorn**
    - Now, Project is ready and hosted in IP provided on the instances on the AWS

### phase 4 : Domain Configuration with Route53:
1. **Setup Route53 on AWS**
    - Used a Route53 on AWS (To create a route between Ip and domain)
    - Configure with that ,with creating a hosting zone
    - We have to create a diffrent record with type A and another with CNAM
2. **Update DomainDNS**
    -   In above config we have got a DNS which we have to change in the domian provider site,(In my case I should used godaddy domain  provider)

### phase 5 and phase 6: Configure Cloudfare for SSL 
1. **Clodfare Configuration**
    - In domain to cloudfare phase (It allows us to used HTTP service)
    - On the cloudfare account used your website-domain (you buy)
    - Then it provied the new dns,changed it to domain provider website(such as godaddy)
2. **Enable HTTPS**
    - Check the HTTPS mode to Full or Strict or Flexible (I will use Flexible)

### Phase 7 :Testing
1. **Testing on Deployment**
    - On the Testing ,We have to check does it working on https securely or not (if not we have to wait for some confirmation,mail or any     messages from provider,AWS  )
    - Lastly ,Our project is deployed on the production level

## Conclusion 
By using this following method I can deployed this project on AWS EC2 (Amazon Web Service Elastic Compute Cloud)




