CREATE TABLE IF NOT EXISTS scans (
  id TEXT PRIMARY KEY,
  filename TEXT,
  package_name TEXT,
  status TEXT,
  created_at TEXT,
  result_json TEXT
);

