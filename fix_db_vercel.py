import re

with open('backend/app/database.py', 'r') as f:
    content = f.read()

pattern = r'DATABASE_URL = os\.getenv\("DATABASE_URL", "sqlite:///\./oil_safety\.db"\)'

new_code = """import shutil

VERCEL_ENV = os.getenv("VERCEL")
DB_PATH = "./oil_safety.db"

if VERCEL_ENV:
    # On Vercel, the filesystem is read-only except for /tmp.
    # We must copy the bundled SQLite DB to /tmp to allow writes!
    tmp_db_path = "/tmp/oil_safety.db"
    if not os.path.exists(tmp_db_path):
        # We need to find the original db. Since api/index.py is in api/,
        # the db might be in backend/oil_safety.db or ./oil_safety.db
        possible_paths = ["./oil_safety.db", "backend/oil_safety.db", "../backend/oil_safety.db"]
        for p in possible_paths:
            if os.path.exists(p):
                shutil.copy2(p, tmp_db_path)
                break
    DB_PATH = tmp_db_path

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")"""

content = content.replace(pattern, new_code)

with open('backend/app/database.py', 'w') as f:
    f.write(content)
