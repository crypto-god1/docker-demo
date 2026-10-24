# 🐳 Dockerized Flask Control Center & Student Management Portal

A full-stack containerized web application built with **Python 3.11**, **Flask**, and **Docker**. Features real-time container telemetry, live system diagnostics, an interactive REST API console, and an in-memory Student Management System.

Developed as part of the **Cloud Computing & RTOS Containerization Lab (DA3)**.

---

## 👨‍💻 Student Information

- **Author**: Hare Preeth
- **Registration Number**: `25BCE5652`
- **Department**: Computer Science and Engineering
- **Course**: Cloud Computing / RTOS & Microservices

---

## 🚀 Key Features

- **Live Container Telemetry**:
  - Live Hostname / Container ID detection.
  - Real-time container uptime counter.
  - In-container disk & storage utilization monitoring.
  - OS runtime & Python environment diagnostics.
- **Interactive Student Management (CRUD)**:
  - Add, list, and delete student records directly from the interface.
  - Persistent in-memory container state.
- **Live REST API Console**:
  - `GET /api/health`: Health status and container timestamp.
  - `GET /api/stats`: Real-time system performance and hardware telemetry.
  - `GET /api/students`: Fetch and query student records.
- **Modern Glassmorphism UI**:
  - Sleek dark theme with Docker-inspired neon accents.
  - One-click copy for essential Docker CLI commands.
  - Fully responsive across desktop, tablet, and mobile.

---

## 🛠️ Project Structure

```text
docker-demo/
├── Dockerfile              # Docker container configuration
├── app.py                  # Flask backend with REST API & telemetry
├── requirements.txt        # Python package dependencies
├── templates/
│   └── index.html          # Modern frontend dashboard & interactive console
└── README.md               # Documentation
```

---

## 🐳 Quick Start with Docker

### 1. Build the Docker Image
```bash
docker build -t flask-demo .
```

### 2. Run the Container
```bash
docker run -d -p 5000:5000 --name flask-container flask-demo
```

### 3. Open the Application
Navigate to [http://localhost:5000](http://localhost:5000) or [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## 🧪 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Renders the Docker Control Center Dashboard |
| `GET` | `/api/health` | Container health probe & status |
| `GET` | `/api/stats` | Live container hardware & OS metrics |
| `GET` | `/api/students` | Get all enrolled student records |
| `POST` | `/api/students` | Add a new student record (`{ name, reg_no, dept, course }`) |
| `DELETE` | `/api/students/<id>` | Delete a student record by ID |

---

## 📋 Essential Docker CLI Commands

```bash
# Check running container status
docker ps

# Stream live container logs
docker logs -f flask-container

# Inspect live container CPU & Memory usage
docker stats flask-container

# Open an interactive shell inside container
docker exec -it flask-container sh

# Stop and remove container
docker rm -f flask-container
```

---

## 📄 License
Created for academic coursework and learning purposes.
