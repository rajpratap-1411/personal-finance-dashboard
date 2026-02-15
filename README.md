<<<<<<< HEAD
# Personal Finance Dashboard

A Django-based web application for managing personal finances with a comprehensive dashboard.

## ✅ Features (FULLY IMPLEMENTED)

- ✅ **User Authentication** - Login, Register, Logout
- ✅ **Track Income** - Add salary, freelance, investments, etc.
- ✅ **Track Expenses** - Add food, rent, transport, etc.
- ✅ **Dashboard** - Real-time financial summary
- ✅ **Charts & Visualizations** - Category-wise and monthly trends
- ✅ **Transaction Management** - Add, Edit, Delete transactions
- ✅ **Auto Categories** - Default categories created for new users
- ✅ **Monthly Calculations** - Automatic income, expense, and savings calculation

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (venv)
- PostgreSQL 12 or higher installed and running

## Setup Instructions

### 1. Clone or Navigate to the Project

```bash
cd personal-finance-dashboard
```

### 2. Activate Virtual Environment

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

Make sure PostgreSQL is installed and running on your system. Create a database for the project:

**Using psql command line:**
```sql
CREATE DATABASE personal_finance_db;
```

Or use pgAdmin or any other PostgreSQL client to create the database.

### 5. Create Environment File

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=personal_finance_db
DB_USER=postgres
DB_PASSWORD=1411
DB_HOST=localhost
DB_PORT=5432
```

**Note:** 
- You can use the default SECRET_KEY for development. For production, generate a new secret key.
- Update database credentials if they differ from the defaults.

### 6. Install PostgreSQL Dependencies

```bash
pip install -r requirements.txt
```

This will install `psycopg2-binary` which is required for PostgreSQL connectivity.

### 7. Run Migrations

```bash
python manage.py migrate
```

### 8. Create a Superuser (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
personal-finance-dashboard/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .gitignore               # Git ignore file
├── personal_finance_dashboard/  # Main project package
│   ├── __init__.py
│   ├── settings.py          # Django settings (PostgreSQL configured)
│   ├── urls.py              # URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
└── venv/                    # Virtual environment (don't commit)
```

## Database

This project uses PostgreSQL as the database backend. Make sure PostgreSQL is running before starting the Django server.

**Default Database Configuration:**
- Database Name: `personal_finance_db`
- User: `postgres`
- Password: `1411`
- Host: `localhost`
- Port: `5432`

You can override these settings by setting environment variables in your `.env` file.

## 🚀 Quick Start (Project is READY!)

### 1. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Run Migrations (Already done, but if needed)
```bash
python manage.py migrate
```

### 3. Create Superuser (Optional - for admin panel)
```bash
python manage.py createsuperuser
```

### 4. Start Server
```bash
python manage.py runserver
```

### 5. Open in Browser
```
http://127.0.0.1:8000
```

### 6. Register & Start Using!
- Go to `/accounts/register` to create account
- Default categories will be created automatically
- Start adding income and expenses!

## 📖 Detailed Setup Guide

See **SETUP_GUIDE.md** for complete instructions in Hindi/English.

## Development

- Django Admin: `http://127.0.0.1:8000/admin/`
- Main application: `http://127.0.0.1:8000/`

## License

This project is open source and available for personal use.

=======
# personal-finance-dashboard
Django Personal Finance Dashboard with accounts, transactions, and analytics
>>>>>>> 428b9ede5df55bbff0b277490bb78871c26ff5b1
