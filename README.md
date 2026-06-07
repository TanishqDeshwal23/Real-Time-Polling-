# 📊 PulseVote - Real-Time Polling Platform

## 🚀 Overview

PulseVote is a real-time polling platform built using FastAPI, WebSockets, SQLAlchemy, and MySQL. The application allows users to create live polls, cast votes instantly, and view updates in real time across multiple connected clients.

The project demonstrates real-time communication, database persistence, asynchronous programming, and full-stack web development concepts.

---

## ✨ Features

### 🗳️ Live Poll Creation

* Create polls dynamically.
* Add multiple voting options.
* Polls are stored permanently in MySQL.

### ⚡ Real-Time Voting

* Vote updates are instantly reflected across all connected clients.
* Powered by WebSocket communication.

### 💾 Database Persistence

* Polls are stored in MySQL.
* Votes are stored and updated in real time.
* Data remains available after server restarts.

### 🔄 Multi-Client Synchronization

* Multiple browser tabs or users can participate simultaneously.
* All clients receive updates instantly.

### 🎨 Modern User Interface

* Responsive design.
* Professional dashboard layout.
* Interactive vote progress indicators.
* Clean and intuitive user experience.

---

## 🏗️ System Architecture

```text
Frontend (HTML, CSS, JavaScript)
              │
              │ WebSocket + REST API
              ▼
       FastAPI Backend
              │
              ▼
      SQLAlchemy ORM
              │
              ▼
        MySQL Database
```

---

## 🛠️ Technology Stack

### Backend

* FastAPI
* WebSockets
* SQLAlchemy
* AsyncIO
* Uvicorn

### Database

* MySQL
* aiomysql

### Frontend

* HTML5
* CSS3
* JavaScript

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```text
RealTime_Polling_Engine/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── create_tables.py
├── test_db.py
├── requirements.txt
├── index.html
├── run_project.bat
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/TanishqDeshwal23/Real-Time-Polling-.git
cd Real-Time-Polling-
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure MySQL Database

Create a database:

```sql
CREATE DATABASE polling_db;
```

Update the database connection string inside `database.py`.

Example:

```python
DATABASE_URL = "mysql+aiomysql://root:YOUR_PASSWORD@localhost:3306/polling_db"
```

### 6. Create Database Tables

```bash
python create_tables.py
```

### 7. Run Application

```bash
python main.py
```

Application will start at:

```text
http://127.0.0.1:8080
```

---

## 📊 Database Schema

### Poll Table

| Field | Type    |
| ----- | ------- |
| id    | Integer |
| title | String  |

### Choice Table

| Field   | Type        |
| ------- | ----------- |
| id      | Integer     |
| text    | String      |
| votes   | Integer     |
| poll_id | Foreign Key |

---

## 🔌 API Endpoints

### REST APIs

| Method | Endpoint | Description        |
| ------ | -------- | ------------------ |
| GET    | /        | Load frontend      |
| GET    | /polls   | Retrieve all polls |

### WebSocket

| Endpoint |
| -------- |
| /ws      |

Supported actions:

### Create Poll

```json
{
  "action": "create_poll",
  "question": "Favorite Language?",
  "options": ["Python", "Java", "C++"]
}
```

### Cast Vote

```json
{
  "action": "vote",
  "poll_id": 1,
  "option": "Python"
}
```

---

## 📸 Screenshots

### Poll Creation Interface

(Add Screenshot Here)

### Real-Time Voting

(Add Screenshot Here)

### MySQL Database Records

(Add Screenshot Here)

---

## 🎯 Learning Outcomes

This project demonstrates:

* Real-Time Communication
* WebSocket Programming
* Asynchronous Backend Development
* Database Integration
* ORM Concepts
* Client-Server Architecture
* Multi-User Synchronization
* Git & GitHub Workflow

---

## 🔮 Future Enhancements

* User Authentication
* Poll Expiration System
* Admin Dashboard
* Vote Analytics
* Poll Sharing via Links
* Export Poll Results
* Docker Deployment
* Cloud Hosting

---

## 👨‍💻 Author

**Tanishq Deshwal**

GitHub: https://github.com/TanishqDeshwal23

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.
