import sys
import os
import datetime
from sqlalchemy.orm import Session

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.database import SessionLocal, engine, Base
from app.models.account import Account, Token

def seed_demo_data():
    """Seeds the database with dummy data for local testing."""
    db: Session = SessionLocal()

    # ensure tables exist
    Base.metadata.create_all(bind=engine)

    try:
        # Check if account exists
        existing_account = db.query(Account).filter(Account.username == "demo_user").first()
        if existing_account:
            print("Demo user already exists.")
            return

        # Create Mock Account
        account = Account(
            threads_user_id="1234567890",
            username="demo_user",
        )
        db.add(account)
        db.commit()
        db.refresh(account)

        # Create Mock Token
        token = Token(
            account_id=account.id,
            access_token="th_mock_token_12345",
            scopes="threads_basic,threads_content_publish",
            expires_at=datetime.datetime.now() + datetime.timedelta(days=60)
        )
        db.add(token)
        db.commit()

        print(f"Seeded demo account: {account.username} (ID: {account.id})")

    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
