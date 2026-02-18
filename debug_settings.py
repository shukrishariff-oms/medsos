import sys
import os

# Add backend to path
sys.path.append(os.getcwd())

try:
    from app.core.settings import settings
    print(f"Settings loaded. get_scopes_list check: {settings.get_scopes_list()}")
except Exception as e:
    print(f"Error loading settings: {e}")

try:
    from app.db.database import get_db, Base
    from app.models.account import Account
    from sqlalchemy import create_engine
    
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    engine = create_engine(settings.DATABASE_URL)
    connection = engine.connect()
    print("Database connection successful.")
    
    # Check tables
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables: {tables}")
    
    required_tables = ['accounts', 'tokens', 'posts', 'replies', 'insights_snapshots']
    missing = [t for t in required_tables if t not in tables]
    if missing:
        print(f"MISSING TABLES: {missing}")
    else:
        print("All required tables exist.")

except Exception as e:
    print(f"Database error: {e}")
