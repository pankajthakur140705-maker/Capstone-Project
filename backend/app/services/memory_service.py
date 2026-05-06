import json
import os

DB_FILE = "app/data/user_memory.json"


def load_memory():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(DB_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def update_user_memory(user_id: str, message: str):
    memory = load_memory()

    if user_id not in memory:
        memory[user_id] = {
            "messages": [],
            "profile": {}
        }

    memory[user_id]["messages"].append(message)

    # keep last 10 messages
    memory[user_id]["messages"] = memory[user_id]["messages"][-10:]

    save_memory(memory)
    return memory[user_id]