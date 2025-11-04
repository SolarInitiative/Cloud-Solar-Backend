"""
Script to create an admin user in the database.
This user can be used for testing and will work with the dev API key middleware.
"""

import asyncio
from app.db.base import SessionLocal
from app.models.models import User
from app.core.security import get_password_hash
from supertokens_python.recipe.emailpassword.asyncio import sign_up
from supertokens_python.recipe.emailpassword.interfaces import SignUpOkResult


async def create_admin_user():
    """Create an admin user with SuperTokens integration."""
    db = SessionLocal()

    # Admin credentials
    username = "admin"
    email = "admin@cloudsolar.com"
    password = "Admin@123456"
    full_name = "Solar Admin"
    location = "Headquarters"

    try:
        print("=" * 60)
        print("Creating Admin User")
        print("=" * 60)

        # Check if user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"\n[X] User '{username}' already exists!")
            print(f"   User ID: {existing_user.id}")
            print(f"   Email: {existing_user.email}")
            print(f"   Is Admin: {existing_user.is_admin}")

            # Offer to make them admin
            if not existing_user.is_admin:
                existing_user.is_admin = True
                db.commit()
                print(f"\n[OK] Updated user to admin status")
            return

        # Register with SuperTokens first
        print("\n1. Registering with SuperTokens...")
        supertokens_result = await sign_up("public", email, password)

        if not isinstance(supertokens_result, SignUpOkResult):
            print("[X] Failed to register with SuperTokens")
            print("   The email might already be registered")
            return

        print(f"   [OK] SuperTokens user created: {supertokens_result.user.id}")

        # Create user in local database
        print("\n2. Creating user in local database...")
        hashed_password = get_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            location=location,
            is_active=True,
            is_admin=True,  # Make this user an admin
            supertokens_user_id=supertokens_result.user.id
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print(f"   ✓ User created with ID: {new_user.id}")

        print("\n" + "=" * 60)
        print("Admin User Created Successfully!")
        print("=" * 60)
        print(f"\n📋 Credentials:")
        print(f"   Username: {username}")
        print(f"   Email:    {email}")
        print(f"   Password: {password}")
        print(f"\n🔑 User Details:")
        print(f"   ID:       {new_user.id}")
        print(f"   Is Admin: {new_user.is_admin}")
        print(f"   Is Active: {new_user.is_active}")
        print(f"   SuperTokens ID: {new_user.supertokens_user_id}")
        print("\n" + "=" * 60)
        print("\n💡 You can now use these credentials to:")
        print("   1. Login via: POST /auth/login")
        print("   2. Use with dev API key: X-API-Key: dev_api_key_123")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(create_admin_user())
