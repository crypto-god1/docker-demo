import os
import sys
import time
import socket
import platform
import shutil
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
START_TIME = time.time()

# In-memory student records with comprehensive metadata
students_db = [
    {
        "id": 1,
        "name": "Hare Preeth",
        "reg_no": "25BCE5652",
        "dept": "Computer Science & Engineering",
        "course": "Docker & Cloud Virtualization (DA3)",
        "grade": "O (10.0)",
        "status": "Verified Author",
        "avatar_bg": "linear-gradient(135deg, #6366f1, #3b82f6)",
        "initials": "HP",
        "email": "harepreethkumar2711@gmail.com",
        "created_at": "2026-10-24 12:30:00"
    },
    {
        "id": 2,
        "name": "Alex Mercer",
        "reg_no": "25BCE5012",
        "dept": "Information Technology",
        "course": "Operating Systems & RTOS Lab",
        "grade": "A+",
        "status": "Enrolled",
        "avatar_bg": "linear-gradient(135deg, #10b981, #059669)",
        "initials": "AM",
        "email": "alex.mercer@college.edu",
        "created_at": "2026-10-24 13:00:00"
    },
    {
        "id": 3,
        "name": "Sarah Connor",
        "reg_no": "25BCE5144",
        "dept": "Computer Science & Engineering",
        "course": "Microservices & Distributed Systems",
        "grade": "O (10.0)",
        "status": "Enrolled",
        "avatar_bg": "linear-gradient(135deg, #ec4899, #8b5cf6)",
        "initials": "SC",
        "email": "sarah.connor@college.edu",
        "created_at": "2026-10-24 13:15:00"
    }
]

def get_system_info():
    uptime_sec = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

    try:
        total, used, free = shutil.disk_usage("/")
        disk_total_gb = round(total / (1024**3), 2)
        disk_used_gb = round(used / (1024**3), 2)
        disk_pct = round((used / total) * 100, 1) if total > 0 else 0
    except Exception:
        disk_total_gb, disk_used_gb, disk_pct = 0, 0, 0

    container_id = socket.gethostname()

    try:
        container_ip = socket.gethostbyname(container_id)
    except Exception:
        container_ip = "127.0.0.1"

    return {
        "student_name": "Hare Preeth",
        "student_reg": "25BCE5652",
        "container_id": container_id,
        "container_ip": container_ip,
        "uptime_str": uptime_str,
        "uptime_seconds": uptime_sec,
        "os": f"{platform.system()} ({platform.release()})",
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "server_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "disk_used_gb": disk_used_gb,
        "disk_total_gb": disk_total_gb,
        "disk_percent": disk_pct,
        "in_docker": os.path.exists("/.dockerenv") or os.environ.get("CONTAINER", "") == "docker"
    }

@app.route("/")
def home():
    info = get_system_info()
    return render_template("index.html", info=info, students=students_db)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "code": 200,
        "message": "Production microservice running optimally",
        "container_id": socket.gethostname(),
        "author": "Hare Preeth (25BCE5652)",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify(get_system_info())

@app.route("/api/students", methods=["GET", "POST"])
def handle_students():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        name = data.get("name", "").strip()
        reg_no = data.get("reg_no", "").strip()
        dept = data.get("dept", "Computer Science & Engineering").strip()
        course = data.get("course", "Docker & Cloud Virtualization").strip()
        email = data.get("email", "").strip()

        if not name or not reg_no:
            return jsonify({"error": "Name and Registration Number are required."}), 400

        # Generate avatar initials and gradient
        initials = "".join([part[0].upper() for part in name.split()[:2]]) or "ST"
        gradients = [
            "linear-gradient(135deg, #06b6d4, #3b82f6)",
            "linear-gradient(135deg, #8b5cf6, #ec4899)",
            "linear-gradient(135deg, #10b981, #0ea5e9)",
            "linear-gradient(135deg, #f59e0b, #ef4444)"
        ]
        color_idx = len(students_db) % len(gradients)

        new_student = {
            "id": (max([s["id"] for s in students_db]) + 1) if students_db else 1,
            "name": name,
            "reg_no": reg_no,
            "dept": dept,
            "course": course,
            "grade": "A+",
            "status": "Enrolled",
            "avatar_bg": gradients[color_idx],
            "initials": initials,
            "email": email or f"{reg_no.lower()}@college.edu",
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        students_db.append(new_student)
        return jsonify({"success": True, "student": new_student}), 201

    return jsonify({"students": students_db, "total": len(students_db)})

@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    global students_db
    before = len(students_db)
    students_db = [s for s in students_db if s["id"] != student_id]
    if len(students_db) < before:
        return jsonify({"success": True, "message": f"Student record #{student_id} purged."})
    return jsonify({"error": "Student record not found."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
