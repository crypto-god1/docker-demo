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

# Zero preloaded student records - clean slate as requested
students_db = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_FILES = {
    "Dockerfile": os.path.join(BASE_DIR, "Dockerfile"),
    "requirements.txt": os.path.join(BASE_DIR, "requirements.txt")
}

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
        "message": "Docker container microservice active and responsive",
        "container_id": socket.gethostname(),
        "author": "Hare Preeth (25BCE5652)",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/api/stats", methods=["GET"])
def stats():
    return jsonify(get_system_info())

# --- DOCKER FILE VIEWER & EDITOR APIS ---
@app.route("/api/files/<filename>", methods=["GET"])
def get_docker_file(filename):
    if filename not in ALLOWED_FILES:
        return jsonify({"error": "Unauthorized file access."}), 403

    filepath = ALLOWED_FILES[filename]
    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            return jsonify({
                "success": True,
                "filename": filename,
                "content": content,
                "lines": len(content.splitlines()),
                "size_bytes": len(content.encode("utf-8"))
            })
        else:
            return jsonify({"error": f"{filename} not found on server."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/files/<filename>", methods=["POST"])
def save_docker_file(filename):
    if filename not in ALLOWED_FILES:
        return jsonify({"error": "Unauthorized file access."}), 403

    filepath = ALLOWED_FILES[filename]
    data = request.get_json(silent=True) or {}
    content = data.get("content", "")

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return jsonify({
            "success": True,
            "filename": filename,
            "message": f"{filename} saved successfully to container filesystem.",
            "lines": len(content.splitlines()),
            "size_bytes": len(content.encode("utf-8")),
            "saved_at": datetime.utcnow().strftime("%H:%M:%S UTC")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- STUDENT MANAGEMENT CRUD APIS ---
@app.route("/api/students", methods=["GET", "POST"])
def handle_students():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        name = data.get("name", "").strip()
        reg_no = data.get("reg_no", "").strip()
        dept = data.get("dept", "Computer Science & Engineering").strip()
        course = data.get("course", "Docker & Cloud Virtualization (DA3)").strip()
        email = data.get("email", "").strip()

        if not name or not reg_no:
            return jsonify({"error": "Name and Registration Number are required."}), 400

        initials = "".join([part[0].upper() for part in name.split()[:2]]) or "ST"
        gradients = [
            "linear-gradient(135deg, #06b6d4, #3b82f6)",
            "linear-gradient(135deg, #8b5cf6, #ec4899)",
            "linear-gradient(135deg, #10b981, #0ea5e9)",
            "linear-gradient(135deg, #f59e0b, #ef4444)",
            "linear-gradient(135deg, #6366f1, #a855f7)"
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

@app.route("/api/students/<int:student_id>", methods=["PUT", "DELETE"])
def modify_student(student_id):
    global students_db

    if request.method == "DELETE":
        before = len(students_db)
        students_db = [s for s in students_db if s["id"] != student_id]
        if len(students_db) < before:
            return jsonify({"success": True, "message": f"Student record #{student_id} purged."})
        return jsonify({"error": "Student record not found."}), 404

    # Handle PUT / Edit
    data = request.get_json(silent=True) or {}
    for s in students_db:
        if s["id"] == student_id:
            if "name" in data and data["name"].strip():
                s["name"] = data["name"].strip()
                s["initials"] = "".join([part[0].upper() for part in s["name"].split()[:2]]) or "ST"
            if "reg_no" in data and data["reg_no"].strip():
                s["reg_no"] = data["reg_no"].strip()
            if "dept" in data:
                s["dept"] = data["dept"].strip()
            if "course" in data:
                s["course"] = data["course"].strip()
            if "email" in data:
                s["email"] = data["email"].strip()
            return jsonify({"success": True, "student": s})

    return jsonify({"error": "Student record not found."}), 404

# --- INTERACTIVE TERMINAL SIMULATOR / INSPECTOR ---
@app.route("/api/terminal", methods=["POST"])
def run_terminal_command():
    data = request.get_json(silent=True) or {}
    cmd = data.get("cmd", "").strip().lower()

    container_id = socket.gethostname()
    
    if cmd in ["docker ps", "ps"]:
        output = f"CONTAINER ID   IMAGE        COMMAND           CREATED        STATUS        PORTS                    NAMES\n{container_id[:12]}   flask-demo   \"python app.py\"   Active         Up 2 hours    0.0.0.0:5000->5000/tcp   flask-container"
    elif cmd in ["docker stats", "stats"]:
        output = f"CONTAINER ID   NAME              CPU %     MEM USAGE / LIMIT     MEM %     NET I/O          BLOCK I/O\n{container_id[:12]}   flask-container   0.24%     28.4MiB / 7.68GiB     0.36%     1.2MB / 4.8MB    0B / 0B"
    elif cmd in ["cat dockerfile", "dockerfile"]:
        filepath = ALLOWED_FILES["Dockerfile"]
        try:
            with open(filepath, "r") as f:
                output = f.read()
        except Exception:
            output = "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nEXPOSE 5000\nCMD [\"python\", \"app.py\"]"
    elif cmd in ["cat requirements.txt", "pip list"]:
        output = "Package      Version\n------------ ---------\nFlask        3.0.3\nWerkzeug     3.0.3\nJinja2       3.1.4\nclick        8.1.7\npip          24.0"
    elif cmd in ["uname -a", "uname"]:
        output = f"Linux {container_id} 6.6.114.1-microsoft-standard-WSL2 #1 SMP PREEMPT {platform.machine()} GNU/Linux"
    elif cmd in ["whoami", "id"]:
        output = "uid=0(root) gid=0(root) groups=0(root) [Isolated Container Namespace]"
    elif cmd in ["uptime"]:
        uptime_sec = int(time.time() - START_TIME)
        output = f"up {uptime_sec} seconds, load average: 0.08, 0.03, 0.01"
    else:
        output = f"bash: {cmd}: command available via container runner. Try: 'docker ps', 'cat Dockerfile', 'pip list', 'uname -a', 'uptime'"

    return jsonify({"cmd": cmd, "output": output, "timestamp": datetime.utcnow().strftime("%H:%M:%S")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
