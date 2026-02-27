# Django XML CRUD API 

This project is a Django-based CRUD web service integrated with a MySQL database, designed to manage library book records through XML-based HTTP API endpoints.

---

## Project Requirements

The application meets the following functional and technical requirements:

- **Framework:** The project is built using the Django web framework (version 5.0.4) with no Django REST Framework used — only built-in Django tools and Python's standard `xml.etree.ElementTree` library.

- **Database Configuration:** The Django project is configured to use MySQL as the backend database (`library_db`), with proper connection settings defined in `settings.py` including host, port, charset, and strict mode.

- **Application & Model:** A Django application (`books`) has been created containing a model (`Book`) that defines a database table with the following fields: `title`, `author`, `year`, `genre`, `isbn`, `created_at`, and `updated_at` — satisfying the minimum requirement of three fields.

- **Migrations:** Database migrations have been performed using `python manage.py makemigrations` and `python manage.py migrate`, successfully creating the `books` table in MySQL.

- **XML Request Handling:** All client requests must be sent in XML format. The server parses incoming XML using `ET.fromstring()` and extracts field values from XML tags.

- **XML Response Handling:** All server responses are returned strictly in valid XML format. JSON responses are not used anywhere in the project. Responses are built using `ET.Element` and `ET.tostring()` and returned as `HttpResponse` with `content_type='application/xml'`.

- **Complete CRUD Functionality:**
  - **Create** (`POST /api/books/`): Accepts XML body and inserts a new book record into MySQL.
  - **Retrieve All** (`GET /api/books/`): Returns all book records as XML.
  - **Retrieve One** (`GET /api/books/<id>/`): Returns a single book record by ID as XML.
  - **Update** (`PUT /api/books/<id>/`): Accepts XML body and updates an existing book record in MySQL.
  - **Delete** (`DELETE /api/books/<id>/`): Removes a book record from MySQL and returns XML confirmation.
  - **Search** (`GET /api/books/search/?q=keyword`): Searches books by title or author and returns XML results.

- **Error Handling:** Proper XML-based error responses are returned for all failure cases including missing required fields (400), book not found (404), duplicate ISBN (409), and invalid method (405).

- **API Testing:** All endpoints have been tested using Postman, including create, retrieve, update, delete, and error handling scenarios.

- **URL Routing:** Routing is configured in both `library_project/urls.py` and `books/urls.py` to ensure all endpoints function correctly under the `/api/` prefix.

- **Admin Verification:** Records can be viewed and managed through the Django Administration panel at `/admin` after creating a superuser.

- **MySQL Verification:** Data stored in MySQL is verified using the MySQL command-line client with `SELECT * FROM books;`.

---

## Functional Validation

The completed project clearly validates all CRUD operations through XML-based HTTP API endpoints:

1. **Create:** Send `POST http://127.0.0.1:8000/api/books/` with XML body to insert a book record.
2. **Read All:** Send `GET http://127.0.0.1:8000/api/books/` to retrieve all books as XML.
3. **Read One:** Send `GET http://127.0.0.1:8000/api/books/1/` to retrieve a specific book as XML.
4. **Update:** Send `PUT http://127.0.0.1:8000/api/books/1/` with XML body to update a book record.
5. **Delete:** Send `DELETE http://127.0.0.1:8000/api/books/1/` to remove a book record.
6. **Error Handling:** Send invalid requests to verify proper XML error responses are returned.
7. **Admin Verification:** Records can also be managed through the Django Administration panel at `/admin`.
8. **MySQL Verification:** Run `SELECT * FROM books;` in MySQL CLI to confirm data is persisted.

---

## Tech Stack

- **Backend:** Django 5.0.4 (Python 3.11+)
- **Database:** MySQL 8.0
- **XML Processing:** Python built-in `xml.etree.ElementTree`
- **CORS:** django-cors-headers
- **API Testing:** Postman

---

## Project Structure

```
library_project/
│
├── manage.py                    # Django command-line utility
├── requirements.txt             # Python package dependencies
├── .gitignore                   # Files excluded from version control
├── README.md                    # Project documentation (this file)
│
├── library_project/             # Django project configuration package
│   ├── __init__.py              # Package init (PyMySQL setup if used)
│   ├── settings.py              # Settings: MySQL config, installed apps, CORS
│   ├── urls.py                  # Root URL config → routes /api/ to books app
│   └── wsgi.py                  # WSGI entry point for deployment
│
└── books/                       # Django application — core of the project
    ├── __init__.py              # Package init
    ├── apps.py                  # App configuration
    ├── admin.py                 # Django admin registration for Book model
    ├── models.py                # Book model → maps to MySQL 'books' table
    ├── views.py                 # CRUD logic: XML parsing, ORM calls, XML responses
    ├── urls.py                  # URL patterns for all book API endpoints
    └── migrations/
        ├── __init__.py
        └── 0001_initial.py      # Auto-generated migration: creates books table
```

---

## API Endpoints

| Method | URL | Action |
|--------|-----|--------|
| GET | `/api/books/` | Retrieve all books |
| POST | `/api/books/` | Create a new book |
| GET | `/api/books/<id>/` | Retrieve one book by ID |
| PUT | `/api/books/<id>/` | Update a book by ID |
| DELETE | `/api/books/<id>/` | Delete a book by ID |
| GET | `/api/books/search/?q=keyword` | Search books by title or author |

---

## How to Clone and Run (School Lab Setup)

Follow these steps exactly if you are setting up this project on a new machine such as a school laboratory computer.

### Prerequisites — install these first if not already installed
- Python 3.11 or 3.12 → https://www.python.org/downloads/
- MySQL 8.0 → https://dev.mysql.com/downloads/installer/
- Git → https://git-scm.com/downloads

---

### Step 1 — Open Command Prompt

Press `Win + R` → type `cmd` → press Enter.

---

### Step 2 — Clone the repository

```cmd
cd Desktop
git clone https://github.com/YOUR_USERNAME/library-xml-crud.git
cd library-xml-crud
```

Replace `YOUR_USERNAME` with the actual GitHub username.

---

### Step 3 — Create and activate a virtual environment

```cmd
python -m venv venv
venv\Scripts\activate
```

Your prompt should now start with `(venv)`.

---

### Step 4 — Install dependencies

```cmd
pip install -r requirements.txt
```

If `mysqlclient` fails to install, run this instead:

```cmd
pip install PyMySQL
```

Then open `library_project/__init__.py` and add:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

### Step 5 — Create the MySQL database

Open **MySQL Command Line Client** from the Start Menu, enter your root password, then run:

```sql
CREATE DATABASE library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

---

### Step 6 — Update the database password in settings.py

Open `library_project/settings.py` and update the `PASSWORD` field to match the MySQL root password on this machine:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library_db',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password_here',   # ← change this
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

---

### Step 7 — Run migrations

```cmd
python manage.py migrate
```

You should see `Applying books.0001_initial... OK` in the output.

---

### Step 8 — Create admin superuser (optional)

```cmd
python manage.py createsuperuser
```

Enter username `admin` and password `admin1234`.

---

### Step 9 — Start the server

```cmd
python manage.py runserver
```

---

### Step 10 — Test the API

Open Postman and test the endpoints listed in the API Endpoints table above.

The server runs at: `http://127.0.0.1:8000`

Example first request — GET all books:
```
GET http://127.0.0.1:8000/api/books/
```

Example create request — POST with XML body:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<book>
  <title>Clean Code</title>
  <author>Robert C. Martin</author>
  <year>2008</year>
  <genre>Technology</genre>
</book>
```