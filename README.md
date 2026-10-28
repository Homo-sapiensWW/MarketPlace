# 🛒 Marketplace REST API

A marketplace backend service with support for user authentication (JWT), a role-based access control model (RBAC), a product catalog, categories, and atomic transactions based on **FastAPI** and **PostgreSQL**.
<img width="1830" height="884" alt="Снимок экрана 2026-10-28 095458" src="https://github.com/user-attachments/assets/f66675b6-4d72-45c9-9df2-6728a668d57a" />
<img width="1212" height="833" alt="Снимок экрана 2026-10-28 095503" src="https://github.com/user-attachments/assets/52b00c8a-de38-46c2-b297-fb548b5baa7d" />
<img width="1831" height="883" alt="Снимок экрана 2026-10-28 095540" src="https://github.com/user-attachments/assets/6c69a521-7ca8-4315-9835-7a87d27abac2" />

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
