# 🌍 Tour Package Booking System 🏝️

A **Django-based** web application where users can **book travel packages**, vendors can **list packages**, and admins can **manage operations**.

---

## 🚀 Features
✅ **User Authentication** (Login, Register, Logout)  
✅ **Admin Dashboard** (Manage Vendors, Users, and Bookings)  
✅ **Vendor Dashboard** (Create, Edit, and Delete Tour Packages)  
✅ **Tour Package Booking System** (Search, Book, Pay Online)  
✅ **Role-Based Access** (Admin, Vendor, User)  
✅ **Secure Payment Integration** (Razorpay or Stripe)  

---

## ⚡ Installation & Setup

### **1️⃣ Clone the Repository**
First, clone this repository to your local machine:
```
git clone https://github.com/Amritha2002-s/TourPackages.git
cd TourPackages
```
### **2️⃣ Set Up a Virtual Environment (Recommended)**
Create and activate a virtual environment:
```
python -m venv env
source env/bin/activate   # On macOS/Linux
env\Scripts\activate      # On Windows

```
### **3️⃣ Install Dependencies**
```
pip install -r requirements.txt

```
### **4️⃣ Configure the Database**
```
python manage.py makemigrations
python manage.py migrate

```
### **5️⃣ Create a Superuser**

To create an admin user 
Enter username, email, and password when prompted.
(Enter 3 of them or else it will not be created)
```
python manage.py createsuperuser

```
### **6️⃣ Run the Development Server**

```
python manage.py runserver

```
Now visit http://127.0.0.1:8000/ in your browser.
### **🎯 Project Structure**
```
TourPackages/
├── tour/            # Main Django App
├── templates/       # HTML Templates
├── static/          # Static Files (CSS, JS)
├── db.sqlite3       # Database (if using SQLite)
├── manage.py        # Django Management Script
├── requirements.txt # Dependencies
├── README.md        # Documentation
├── .env             # Environment Variables (Add to .gitignore)
```
---

### **🌟 Support**
If you like this project, ⭐ Star this repo and share it with others!
---
