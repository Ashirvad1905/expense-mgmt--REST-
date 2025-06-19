# 💸 Expense Management Backend

A full-featured backend for an Expense Management Web Application built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. It supports user authentication, role-based access, expense tracking, budgeting, and reporting features.

---

## 🚀 Tech Stack

- **FastAPI** — High-performance Python web framework
- **PostgreSQL** — Relational database
- **SQLAlchemy + Alembic** — ORM & migrations
- **Graphene / GraphQL** (coming soon)
- **JWT (OAuth2)** — Authentication
- **Docker** *(optional)* — Containerization
- **Pre-commit hooks** — Code quality checks

---

## 🧑‍💼 User Roles

- **Admin**
- **Manager**
- **Regular User**

---

## 🧩 Features

### 🔐 Authentication
- Signup/Login with hashed passwords
- JWT-based access tokens
- Role-based access control

### 🧾 Expense Management
- Add, update, delete expenses
- Add receipt URLs, recurring flag
- Category-based tagging

### 📊 Budgeting
- Set category-wise budgets
- Time-period tracking
- Budget exceeded alerts (planned)

### 📂 Categories
- Nested categories with parent-child support
- CRUD operations

### 📈 Reports (planned)
- Graphs: pie/bar/line charts
- Export to PDF/CSV

---

## 🛠️ Project Setup

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
