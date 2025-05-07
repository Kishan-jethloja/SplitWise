# 💰SplitWise - Smart Expense Sharing System

## 🌟Overview
Split-Wise is a comprehensive expense sharing system developed using Django framework. This project aims to simplify the process of splitting bills and managing shared expenses among friends, roommates, and groups, making it easier to track who owes whom and settle debts efficiently.

## 🤝Contributors
This project is a collaborative effort between:

Kishan Jethloja
Madhav Javia

As part of our academic journey in web development, we combined our skills and creativity to build this innovative expense management platform that helps people manage their shared finances effortlessly.

## 🚀Features
- User Authentication and Authorization
- Group Creation and Management
- Expense Tracking and Splitting
- Real-time Balance Calculation
- Admin Dashboard
- Responsive Design

## ⚙️Technology Stack
- Backend Framework: Django 5.1.3+
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Template Engine: Django Templates

## 📁Project Structure
```
SplitWise/
├── myapp/              # Main application directory
│   ├── templates/      # HTML templates
│   │   ├── admin.html  # Admin panel template
│   │   └── ...        # Other templates
│   ├── static/         # CSS, JS, images
│   ├── views.py        # Application logic
│   ├── models.py       # Database models
│   └── urls.py         # URL routing
├── myproject/          # Project configuration
│   ├── settings.py     # Django settings
│   ├── urls.py         # Main URL configuration
│   └── wsgi.py         # WSGI configuration
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```

## 🖥️Installation and Setup
1. **Clone the repository**
```bash
git clone https://github.com/Kishan-jethloja/SplitWise.git
cd SplitWise
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# For Windows:
venv\Scripts\activate
# For Linux/Mac:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Start the development server**
```bash
python manage.py runserver
```

## 🔐Login
### Admin Login
The admin can log in using superuser credentials. If you have not created one yet, run:
```bash
python manage.py createsuperuser
```

### User Login
Users can log in through the Login Page using their credentials. New users can sign up via the Signup Page.

## 🔍Explore Features
### 👤For Users:
- Create and join groups
- Add and split expenses
- Track balances
- View expense history
- Settle debts

### 👨‍💼For Admins:
- Manage users
- View all groups
- Monitor system activity
- Access admin dashboard

## 📌Closing Remarks
This project demonstrates practical implementation of Django web development and aims to solve real-world problems in expense sharing. We hope SplitWise continues to evolve with more advanced features in the future, helping create smarter and more efficient ways to manage shared expenses.

Feel free to fork this repository and make improvements. Your contributions are welcome!

Thank you for your interest in SplitWise!
