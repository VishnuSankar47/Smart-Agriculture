# Smart Agriculture 🌾

A web-based platform built with **Python (Django)** and **MySQL** that connects farmers directly with customers, enabling online listing, booking, and purchase of agricultural produce.

---

## Features

### Admin
- Approve / reject farmer registration requests
- Manage product categories (add, edit, delete)
- View all booking details
- View and reply to user complaints

### Farmer
- Register and await admin approval
- List produce under categories
- View booking history and sales

### User (Customer)
- Register and browse available produce
- Book items and make payment
- View purchase history
- Submit and track complaints

---

## Tech Stack

| Layer      | Technology                |
|------------|---------------------------|
| Backend    | Python 3, Django          |
| Frontend   | HTML5, CSS3, JavaScript   |
| Database   | MySQL                     |
| Dev Tools  | phpMyAdmin, VS Code       |

---

## Project Structure

```
smart_agriculture/
├── agriculture/            # Main Django app
│   ├── migrations/
│   ├── templates/
│   │   ├── Admin/
│   │   ├── Farmer/
│   │   └── User/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── smart_agriculture/      # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/
│   └── js/
├── sql/
│   └── schema.sql          # Database setup script
├── manage.py
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/smart-agriculture.git
cd smart-agriculture
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up the MySQL database
- Create a database named `smart_agriculture` in MySQL / phpMyAdmin
- Run the schema script:
```bash
mysql -u root -p smart_agriculture < sql/schema.sql
```

### 5. Configure database credentials
Edit `smart_agriculture/settings.py` and update the `DATABASES` section:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smart_agriculture',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Run the development server
```bash
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000`

---

## Default Admin Login
After running the schema script, an admin account is seeded:
- **Username:** `admin`
- **Password:** `admin123`

---

## Academic Context

This project was submitted as a final year project for the **Bachelor of Computer Science** degree at **Swamy Saswathikananda College, Poothotta** (affiliated to Mahatma Gandhi University), academic year 2021–2022.

- **Author:** M Vishnu Sankar (190021030827)
- **Guide:** Mrs. Bincy John, Assistant Professor, Dept. of Computer Science

---

## License

This project is for academic and educational purposes.
