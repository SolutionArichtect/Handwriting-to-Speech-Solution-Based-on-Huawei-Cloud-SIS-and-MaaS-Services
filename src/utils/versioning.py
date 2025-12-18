import os
import json
import datetime

STATE_PATH = "log/version_state.json"

def _load_state():
    if not os.path.exists("log"):
        os.makedirs("log")
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"major": 0, "minor": 0, "patch": 0, "count": 0}

def _save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False)

def current_version():
    s = _load_state()
    return f"{s['major']}.{s['minor']}.{s['patch']}"

def bump_patch():
    s = _load_state()
    s["patch"] += 1
    s["count"] += 1
    if s["patch"] >= 10:
        s["patch"] = 0
        s["minor"] += 1
    _save_state(s)
    v = f"{s['major']}.{s['minor']}.{s['patch']}"
    ts = datetime.datetime.now().isoformat()
    with open("log/version_log", "a", encoding="utf-8") as f:
        f.write(f"{ts}: version {v}\n")
    return v
