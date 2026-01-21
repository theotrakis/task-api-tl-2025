from flask import Flask, jsonify, request
from storage import load_tasks, save_tasks, next_id, find_task

# Δημιουργία Flask app
app = Flask(__name__)

# ---------- HOME ROUTE ----------
# ΑΥΤΟ είναι το route για το http://127.0.0.1:5000
@app.get("/")
def home():
    return {
        "message": "Task API is running",
        "endpoints": {
            "get_all_tasks": "GET /tasks",
            "get_task": "GET /tasks/<id>",
            "create_task": "POST /tasks",
            "delete_task": "DELETE /tasks/<id>"
        }
    }, 200

# ---------- TASK ROUTES ----------

REQUIRED_FIELDS = ["username", "title", "description", "deadline"]


@app.get("/tasks")
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks), 200


@app.get("/tasks/<int:task_id>")
def get_task_by_id(task_id: int):
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Body must be JSON object"}), 400

    missing = [f for f in REQUIRED_FIELDS if f not in data or data[f] in (None, "")]
    if missing:
        return jsonify({"error": "Missing fields", "missing": missing}), 400

    tasks = load_tasks()

    new_task = {
        "id": next_id(tasks),
        "username": data["username"],
        "title": data["title"],
        "description": data["description"],
        "deadline": data["deadline"],
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return jsonify(new_task), 201


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    tasks = [t for t in tasks if int(t.get("id")) != task_id]
    save_tasks(tasks)

    return jsonify({"message": "Task deleted", "id": task_id}), 200


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
