# Django Leave Management System

This Django application is a Leave Management System designed to facilitate leave requests and management within an organization. It is divided into two main sections: Admin Section and Employee Section.

## Features

### Admin Section

1. **Dashboard**
   - View available leave types, employees, departments, pending leaves, declined leaves, and approved leaves.

2. **Employee Section**
   - View, edit, and add new employee details.

3. **Department Section**
   - Add, update, and view department information.

4. **Leave Section**
   - View, edit, and add new leave types.

5. **Manage Leave Section**
   - Approve and decline leave requests.
   - View pending, declined, and approved leaves.

6. **Admin Section**
   - Add new admin and update admin details.

### Employee Section

1. Apply for leave.
2. View leave application history.
3. Update personal information.
4. Recover password.

## Login Details

### Admin Section
- **Username:** lamar
- **Password:** 1252

### Employee Section
- **Username:** AKAM001
- **Password:** 1000

## Installation

Follow these steps to set up the Leave Management System:

1. Clone the repository:
   ```bash
   git clone https://github.com/santospaul1/Leave-Management-System-in-Django-.git
   cd django-leave-management
2. Install dependencies:
   ```bash
    pip install -r requirements.txt

3.  Apply migrations:
    ```bash
    python manage.py migrate
4.  Create a superuser for initial login:
    ```bash
    python manage.py createsuperuser
5.  Run the development server:
    ```bash
    python manage.py runserver
6.  Access the application at http://localhost:8000

<h2>Contributing</h2>
Contributions are welcome! Follow the standard GitHub Fork & Pull Request workflow.

<h2>License</h2>
This project is licensed under the MIT License - see the LICENSE file for details.

