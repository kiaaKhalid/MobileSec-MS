import os, datetime, json
from sqlalchemy import create_engine, text

DB_PATH = os.environ.get("DB_PATH", "/app/storage.db")
# On utilise SQLite pour ce MVP
ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

def init_db():
    with ENGINE.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS secrets_scans (
                id TEXT PRIMARY KEY,
                filename TEXT,
                status TEXT,
                created_at TEXT,
                findings_json TEXT
            )
        """))

def save_result(scan_id, filename, status, findings):
    with ENGINE.begin() as conn:
        res_json = json.dumps(findings, ensure_ascii=False)
        conn.execute(
            text("INSERT OR REPLACE INTO secrets_scans (id, filename, status, created_at, findings_json) VALUES (:id,:filename,:status,:created_at,:res)"),
            {"id": scan_id, "filename": filename, "status": status, "created_at": datetime.datetime.utcnow().isoformat(), "res": res_json}
        )

def get_result(scan_id):
    with ENGINE.connect() as conn:
        r = conn.execute(text("SELECT id, filename, status, created_at, findings_json FROM secrets_scans WHERE id=:id"), {"id": scan_id}).fetchone()
        if not r: return None
        return {
            "id": r[0], "filename": r[1], "status": r[2], "created_at": r[3],
            "findings": json.loads(r[4]) if r[4] else []
        }

def get_all_scans(limit=50):
    with ENGINE.connect() as conn:
        rows = conn.execute(
            text("SELECT id, filename, status, created_at FROM secrets_scans ORDER BY created_at DESC LIMIT :limit"),
            {"limit": limit}
        ).fetchall()
        
        return [
            {
                "id": r[0],
                "filename": r[1],
                "status": r[2],
                "created_at": r[3]
            }
            for r in rows
        ]