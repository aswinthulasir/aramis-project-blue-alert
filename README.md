# Medical Billing System Documentation

## Project Overview
The **Medical Billing System** is a streamlined solution designed to handle core billing functionalities in a healthcare setting. This project focuses on efficiency, simplicity, and clean architecture while ensuring accurate and seamless billing operations. The system supports both **admin** and **user-level access and controls**.

## Prerequisites
Before setting up the project, ensure you have the following dependencies installed:

- **Python** (3.13 or higher)
- **PostgreSQL** (14 or higher)
- **FastAPI**

## Initial Setup

### 1. Create the Project Directory
```bash
# Create directory for this project
mkdir billing_system
cd billing_system
```

### 2. Set Up a Virtual Environment
```bash
# Create a virtual environment
python -m venv venv
```

#### Activate the Virtual Environment
```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn psycopg2  # Use 'asyncpg' instead of 'psycopg2' for async support
```

### 4. (Optional) Save Dependencies to a `requirements.txt` File
To ensure consistency across environments, generate a `requirements.txt` file:
```bash
pip freeze > requirements.txt
```
To install dependencies from the file in the future, use:
```bash
pip install -r requirements.txt
```

### 5. Setup Database
1. Install PostgreSQL
Ensure that PostgreSQL is installed on your system. If not, download and install it from:
https://www.postgresql.org/download/

2. Create the Database:

```sql
-- Open PostgreSQL CLI (psql) and run the following commands
CREATE DATABASE medical_billing;

-- Create a dedicated user
CREATE USER billing_admin WITH ENCRYPTED PASSWORD 'admin_password'; (username and admin_password can be changed accordingly)

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE medical_billing TO billing_admin;
```

### Project Configuration
5. Environment Variables:
Create a **`.env`** file in the root directory and define the database connection details:

```ini
DATABASE_URL=postgresql://billing_admin:admin_password@localhost:5432/medical_billing
SECRET_KEY=your_secret_key
```

### 5. Install Required Dependencies
```bash
pip install pydantic[dotenv] psycopg[binary] sqlalchemy alembic
```

### 6. Run the server
```bash
uvicorn app.main:app --reload
```

## Database Schema, Query and Procedure Setup
(For more security and authenticity, most of the querys and procedures are defined in the PostgreSQL CLI instead of the backend schema)

### Create tables
List of tables in your PostgreSQL database:

1. **auth**  
2. **billing**  
3. **jwt_token**  
4. **passwords**  
5. **patients**  
6. **rates**  
7. **roles**  
8. **service** 
9. **services** 
10. **staffs**  
11. **users**  

### Querys for table creation

```sql
-- users table
CREATE TABLE users (
    u_id VARCHAR(8) UNIQUE NOT NULL,
    staff_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- passwords table
CREATE TABLE passwords (
    id SERIAL PRIMARY KEY,
    u_id VARCHAR(8) NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (u_id) REFERENCES users(u_id) ON DELETE CASCADE
);

--auth table
CREATE TABLE auth (
    id SERIAL PRIMARY KEY,
    u_id VARCHAR(8) NOT NULL,
    jwt_token TEXT NOT NULL,
    FOREIGN KEY (u_id) REFERENCES users(u_id) ON DELETE CASCADE
);

-- u_id auto generation procedure (with set trigger)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION generate_u_id()
RETURNS TEXT AS $$
SELECT substr(encode(gen_random_bytes(6), 'hex'), 1, 8);
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION set_u_id()
RETURNS TRIGGER AS $$
BEGIN
    NEW.u_id := generate_u_id();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_u_id
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION set_u_id();

-- roles table
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role VARCHAR(50) UNIQUE NOT NULL
);

-- staffs table (with composite primary key)
CREATE TABLE staffs (
    staff_id INT,
    u_id VARCHAR(8),
    role_id INT,
    activity BOOLEAN,
    s_name VARCHAR(255) DEFAULT 'Unknown',
    PRIMARY KEY (staff_id, role_id),  -- Composite Primary Key
    FOREIGN KEY (staff_id) REFERENCES users(staff_id),
    FOREIGN KEY (u_id) REFERENCES users(u_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- billing table
CREATE TABLE billing (
    bill_id SERIAL PRIMARY KEY,
    ser_id INT REFERENCES services(ser_id) ON DELETE CASCADE,
    u_id VARCHAR(255) REFERENCES users(u_id) ON DELETE CASCADE,
    p_id INT REFERENCES patients(p_id) ON DELETE CASCADE,
    ser_rate DECIMAL(10,2) NOT NULL,
    payment_sts BOOLEAN DEFAULT FALSE,
    bill_cfm BOOLEAN DEFAULT TRUE;
);

-- jwt_token table
CREATE TABLE jwt_token (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE REFERENCES users(u_id) ON DELETE CASCADE,
    token TEXT NOT NULL
);

-- add date on billing table
UPDATE billing SET bill_date = CURRENT_DATE WHERE bill_date IS NULL;

-- patients table
CREATE TABLE patients (
    p_id SERIAL PRIMARY KEY,
    p_name VARCHAR(255) NOT NULL,
    p_dept VARCHAR(255),
    p_desc TEXT,
    p_age INT CHECK (p_age >= 0),
    p_doc VARCHAR(255) -- Doctor's Name
);

-- rates tabel
CREATE TABLE rates (
    ser_id INT REFERENCES services(ser_id) ON DELETE CASCADE,
    ser_rate DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (ser_id, ser_rate)
);

-- services table
CREATE TABLE services (
    ser_id SERIAL PRIMARY KEY,
    ser_name VARCHAR(255) NOT NULL,
    ser_desc TEXT,
    ser_image TEXT,
    ser_avl BOOLEAN DEFAULT TRUE
);
```
### Connect the database through a single file (config.py) (optional)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_name: str = "local"
    database_username: str = "postgres"
    database_password: str = "admin_password"

settings = Settings()
```
## Project Structure

```
billing_system/
├── backend/
    ├── app/
        ├── routers/
            ├── __init.py
            ├── auth.py
            ├── bills_today.py
            ├── bills.py
            ├── fetch_billing.py
            ├── fetch_patients.py
            ├── fetch_rates.py
            ├── fetch_roles.py
            ├── fetch_services.py
            ├── fetch_users.py
            ├── indi_bills.py
            ├── patients.py
            ├── roles.py
            ├── services.py
            ├── update_services.py
            ├── update_staff.py
        ├── tests/
        ├── config.py
        ├── database.py
        ├── main.py
        ├── utils.py
    ├── env/
    ├── .env
    ├── requirements.txt
├── frontend/
    ├── assets/
    ├── js/
        ├── admScripts.js
        ├── login.js
        ├── p_scripts.js
        ├── scripts.js
        ├── staff_act.js
        ├── staffs.js
    ├── styles/
        ├── admin.css
        ├── home.css
        ├── index.css
    ├── ad01x.html
    ├── add_staffhtml
    ├── admin_dashboard.html
    ├── admin_show_p.html
    ├── bills.html
    ├── dashboard.html
    ├── index.html
    ├── login.html
    ├── patient_bill.html
    ├── patients.html
    ├── show_patients.html
├── README.md

```

## API Endpoints

### 1. Register User

- End point: `http://127.0.0.1:8000/users/register`
- Method: POST
- Description: Regsiter staffs by admin

### 2. Authentication

- End point: `http://localhost:8000/auth/login`
- Method: GET
- Description: Authentication (JWT and Encryption)

### 3. Add Services

- End point: `http://localhost:8000/services/post`
- Method: POST
- Description: Adding services and its rate

### 4. Add Patients

- End point: `http://127.0.0.1:8000/patients/post`
- Method: POST
- Description: Adding patients and their details

### 5. Add Bills

- End point: `http://127.0.0.1:8000/bills/post`
- Method: POST
- Description: Add bills with respect to p_id

### 6. Add Roles

- End point: `http://127.0.0.1:8000/roles/add`
- Method: POST
- Description: Add various roles of staffs

### 7. Fetch Users

- End point: `http://127.0.0.1:8000/staffs/get `
- Method: GET
- Description: Get all necessary columns of staffs table

### 8. Fetch Services

- End point: `http://127.0.0.1:8000/services/get `
- Method: GET
- Description: Get all necessary columns of services table

### 9. Fetch Patients

- End point: `http://127.0.0.1:8000/patients/get `
- Method: GET
- Description: Get all necessary columns of patients table

### 10. Fetch Billings

- End point: `http://127.0.0.1:8000/billing/get `
- Method: GET
- Description: Get all necessary columns of billing table

### 11. Fetch Roles

- End point: `http://127.0.0.1:8000/roles/get `
- Method: GET
- Description: Get all necessary columns of roles table

### 12. Update User

- End point: `http://127.0.0.1:8000/staffs/update-name/{id}, /update-activity/{id}, /update-role/{id} `
- Method: PUT
- Description: Update the user details such as name, activity status and role

### 13. Block User

- End point: `http://127.0.0.1:8000/staffs/update-activity/{id} `
- Method: PUT
- Description: Update the activity of user

### 14. Get bill of a specific person

- End point: `http://127.0.0.1:8000/api/bills/{id} `
- Method: PUT
- Description: Get the specific bills of each user in a new page


For further api end points and integration statuses please refer the following excel sheet:
`https://docs.google.com/spreadsheets/d/1jTcnCcPjLiWiDMoiUpojOQgYzj0bpxjhgh8L1Ng83rk/edit?usp=sharing`


## Authentication Flow

**Signin Flow**
   
   - Commonly username (email format) and password is filled

   - Submits form

   - Server validates user account

   - Success/failure message displayed

**Signup Flow**

   - Admin fills remaining required fields

   - Created staff authentication parameters (username and password)

   - Selects staff role

   - Submits form

   - Server creates user account

   - Success/failure message displayed


## Security Consideraions

### 1. Database Design

- Four tables - users, passwords, jwt_token and auth is independently designed with nessessary primary and foreign key relationships. No table datas is connected to backend and hence it is not accessible by cracking the source code.

- Independent procedures for each tables written in the Postgre CLI itself for more security.

- Entries are channeled through the same API to these independent tables and vice-versa.

- Hashing is done using bcrypt for proper encryption.

- Frequent updation of token after each login.

- For code sharing and understanding, the jwt code has been transferred to backend. On production,try to implement it on the CLI.

- No salting is done (SHA-256 recomended)

### 2. Role Based Authentication

- Each level of access for both users(staffs) and admin

- Credentials for each staff is created and handled by admin

- Admin login is seperated in another url-path for improving credibility

### 3. OAuth Security

- State parameter used to prevent CSRF

- Access tokens stored securely

- Proper scope limitations

### 4. Session Management
   - JWT expires after 2 hours

## Trouble Shooting

1. **Database Issues**
   ```cmd

   # Reset database (Windows)
    net stop postgresql
    net start postgresql

   # Reset database (Mac)
    brew services restart postgresql

   # Reset database (Linux/Ubuntu/Debian)
    sudo systemctl restart postgresql

   ```
  

2. **Common Issues**

   - Use console error message and seek AI help for troubleshooting and debugging


## Future Improvements

- Use salting procedures using SHA 256 or 512

- Add multi-factor authentication

- UI/UX improvements using React Library

- Adding strong session managements using caches and cookies

- Implementing printing and other inbuilt bill sharing mechanism

- Adding proper routes procedures and route paths

## Contributing

1. Fork the repository

2. Create a feature branch

3. Make changes

4. Submit pull request

## License

Regular Open-source license (MIT)
