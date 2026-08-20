# 🛒 Marketplace REST API

A marketplace backend service with support for user authentication (JWT), a role-based access control model (RBAC), a product catalog, categories, and atomic transactions based on **FastAPI** and **PostgreSQL**.

---

## 🚀 Tech Stack

* **Backend:** Python 3.11+, FastAPI, Pydantic v2
* **Database & ORM:** PostgreSQL (Neon Serverless), SQLAlchemy
* **Security:** JWT (PyJWT), password hashing (Bcrypt / Passlib), OAuth2 Password Flow
* **Testing:** Pytest, HTTPX (FastAPI TestClient)
* **Server:** Uvicorn

---

## ⚙️ Main Functionality

1. **Authentication and Security:**
* User registration with a starting balance (`100`).
* Login with username/password and issuance of a signed JWT Bearer token.
* Role-based access model (`user`, `admin`).
2. **Marketplace & Transactions:**
* Create, view, and filter available lots.
* Atomic purchase of goods: balance check, debit from the buyer, credit to the seller, block the item (`is_sold=True`), and record in the `transactions` history.
* Validate business rules (prohibit purchase of your own item, protect against duplicate purchases).
3. **Administrator Panel:**
* Manage product categories.
* Assign administrator rights.
* Moderate (delete) lots.
4. **Testing:**
* A set of automated integration tests to verify all endpoints and edge business scenarios.

---