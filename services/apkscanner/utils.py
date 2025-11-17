import uuid
import datetime
import json
import os
from sqlalchemy import create_engine, text

DB_PATH = os.environ.get("APK_DB_PATH", "/app/storage.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

def init_db():
    with ENGINE.connect() as conn:
        sql = open("schema.sql", "r").read()
        conn.execute(text(sql))

def save_scan_result(scan_id, filename, package_name, status, result):
    with ENGINE.begin() as conn:
        res_json = json.dumps(result, ensure_ascii=False)
        conn.execute(
            text("INSERT OR REPLACE INTO scans (id, filename, package_name, status, created_at, result_json) VALUES (:id,:filename,:pkg,:status,:created_at,:res)"),
            {"id": scan_id, "filename": filename, "pkg": package_name, "status": status, "created_at": datetime.datetime.utcnow().isoformat(), "res": res_json}
        )

def update_status(scan_id, status):
    with ENGINE.begin() as conn:
        conn.execute(text("UPDATE scans SET status=:status WHERE id=:id"), {"status": status, "id": scan_id})

def get_scan(scan_id):
    with ENGINE.connect() as conn:
        r = conn.execute(text("SELECT id, filename, package_name, status, created_at, result_json FROM scans WHERE id=:id"), {"id": scan_id}).fetchone()
        if not r:
            return None
        import json
        return {
            "id": r[0],
            "filename": r[1],
            "package_name": r[2],
            "status": r[3],
            "created_at": r[4],
            "result": json.loads(r[5]) if r[5] else None
        }

