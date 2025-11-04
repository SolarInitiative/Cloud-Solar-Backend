"""
Script to clear all data from the database.

WARNING: This will delete ALL data from the database!
Use with caution, especially in production environments.
"""

from app.db.base import SessionLocal, engine
from app.models.models import User
from sqlalchemy import text


def clear_all_data():
    """Clear all data from all tables in the database."""
    db = SessionLocal()

    try:
        print("=" * 60)
        print("WARNING: This will delete ALL data from the database!")
        print("=" * 60)

        # Count current records
        user_count = db.query(User).count()
        print(f"\nCurrent data:")
        print(f"  - Users: {user_count}")

        confirm = input("\nAre you sure you want to delete all data? (yes/no): ")

        if confirm.lower() != 'yes':
            print("Operation cancelled.")
            return

        # Delete all users
        print("\nDeleting all users...")
        db.query(User).delete()
        db.commit()

        # Reset sequences (for auto-increment IDs)
        print("Resetting ID sequences...")
        db.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
        db.commit()

        print("\n" + "=" * 60)
        print("All data has been cleared successfully!")
        print("=" * 60)

        # Verify deletion
        user_count = db.query(User).count()
        print(f"\nRemaining data:")
        print(f"  - Users: {user_count}")

    except Exception as e:
        print(f"\nError occurred: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    clear_all_data()
