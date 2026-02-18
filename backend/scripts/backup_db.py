import shutil
import os
import datetime

# Configuration
# Assuming script is run from backend root or similar, but let's make it robust
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # MedSos root
DB_PATH = os.path.join(BASE_DIR, "storage", "app.db")
BACKUP_DIR = os.path.join(BASE_DIR, "storage", "backups")

def backup_db():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"app_backup_{timestamp}.db")
    
    try:
        shutil.copy2(DB_PATH, backup_file)
        print(f"Backup created successfully: {backup_file}")
    except Exception as e:
        print(f"Error creating backup: {e}")

if __name__ == "__main__":
    backup_db()
