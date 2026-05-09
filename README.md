# 🔗 Job Posting Link Hub

![Job Hub UI](https://img.shields.io/badge/UI-Beautiful_Dark_Mode-6c63ff?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

A lightweight, fast, and beautiful personal API and web interface to store job posting links in one centralized place.

Built with **Python**, **FastAPI**, **SQLite**, and **Vanilla HTML/CSS/JS**.

## ✨ Features
- **Modern Dark UI**: A beautiful, responsive frontend to easily paste and view your job links.
- **Duplicate Prevention**: Automatically rejects links that you've already saved.
- **Search & Filter**: Live sorting of your database to find specific companies or roles.
- **RESTful API**: Complete CRUD operations via `/links` using FastAPI.
- **Self-Contained DB**: Uses a single `links.db` SQLite file for zero-configuration persistence.

## 🚀 Getting Started

### 1. Prerequisites
You need Python 3 installed on your machine.

### 2. Installation
Clone/download this directory, then install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Running the App
Start the local server using `uvicorn`:

```bash
uvicorn main:app --reload --port 8000
```

### 4. Accessing the Hub
- **Frontend App**: [http://localhost:8000](http://localhost:8000)
- **Interactive API Docs / Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💻 API Usage (cURL Examples)

The backend exposes a fully functional REST API. Here is how you can interact with it via the terminal:

### Save a Link
```bash
curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://linkedin.com/jobs/view/123456",
    "job_title": "ML Engineer",
    "company": "Acme Corp"
  }'
```
*(Only `url` is strictly required)*

### List All Links
```bash
curl http://localhost:8000/links
```

### Delete a Link
```bash
curl -X DELETE http://localhost:8000/links/1
```

---

## 🌍 How to create a Public API Link

If you need to test the API from your mobile device or share it temporarily, you can expose your local server using **Ngrok**:

1. Install ngrok via brew (macOS): `brew install ngrok/ngrok/ngrok`
2. Make sure your local server is running on port 8000.
3. In a new terminal, run: `ngrok http 8000`
4. Ngrok will give you an `https` URL that you can access from anywhere in the world! 

*For permanent hosting, consider deploying this folder to a service like Render or Fly.io and mounting a persistent disk for the `links.db` file.*

---

## 📁 File Structure

```text
job_postings/
├── backend/
│   ├── main.py            # FastAPI backend logic and endpoints
│   ├── requirements.txt   # Python dependencies
│   └── links.db           # SQLite database (auto-generated)
└── frontend/
    └── index.html         # Beautiful frontend interface
```
