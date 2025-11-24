import os, datetime, json
from sqlalchemy import create_engine, text

DB_PATH = os.environ.get("DB_PATH", "/app/storage.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

def init_db():
    with ENGINE.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS network_scans (
                id TEXT PRIMARY KEY,
                package_name TEXT,
                status TEXT,
                created_at TEXT,
                findings_json TEXT
            )
        """))

def save_scan(scan_id, package_name, status, findings):
    with ENGINE.begin() as conn:
        res_json = json.dumps(findings, ensure_ascii=False)
        conn.execute(
            text("INSERT OR REPLACE INTO network_scans (id, package_name, status, created_at, findings_json) VALUES (:id,:pkg,:status,:created_at,:res)"),
            {"id": scan_id, "pkg": package_name, "status": status, "created_at": datetime.datetime.utcnow().isoformat(), "res": res_json}
        )

def get_scan_result(scan_id):
    with ENGINE.connect() as conn:
        r = conn.execute(text("SELECT id, package_name, status, created_at, findings_json FROM network_scans WHERE id=:id"), {"id": scan_id}).fetchone()
        if not r: return None
        return {
            "id": r[0],
            "package_name": r[1],
            "status": r[2],
            "created_at": r[3],
            "findings": json.loads(r[4]) if r[4] else []
        }
