from flask import Flask, current_app, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from typing import Optional, Dict, Any
import uuid
import hashlib
import os
from datetime import datetime


class User(UserMixin):
    """User class that implements UserMixin for Flask-Login compatibility."""

    def __init__(self, user_id: str, email: str, **kwargs):
        self.id = user_id
        self.email = email
        self.is_active = kwargs.get("is_active", True)
        self.is_authenticated = kwargs.get("is_authenticated", True)
        self.created_at = kwargs.get("created_at", datetime.now())
        self.last_login = kwargs.get("last_login", None)
        self.profile = kwargs.get("profile", {})

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """Hash a password with a salt."""
        if not salt:
            salt = os.urandom(32).hex()
        hashed = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()
        return hashed, salt

    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """Verify a password against a hash and salt."""
        return User.hash_password(password, salt)[0] == hashed


class AuthManager:
    """Manages authentication using Flask-Login."""

    def __init__(self, app: Optional[Flask] = None):
        self.login_manager = LoginManager()
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize the auth manager with a Flask application."""
        self.login_manager.init_app(app)
        self.login_manager.login_view = "auth.login"
        self.login_manager.login_message = "Please log in to access this page."

        @self.login_manager.user_loader
        async def load_user(user_id: str) -> Optional[User]:
            """Load a user from the database by ID."""
            # This would typically query from your database
            # For demonstration, using a simple approach
            db = current_app.extensions.get("db")
            if not db:
                return None

            try:
                # Assuming db has an async get_user method
                user_data = await db.get_user(user_id)
                if user_data:
                    return User(
                        user_id=user_data["id"],
                        email=user_data["email"],
                        is_active=user_data.get("is_active", True),
                        created_at=user_data.get("created_at"),
                        last_login=user_data.get("last_login"),
                        profile=user_data.get("profile", {}),
                    )
                return None
            except Exception as e:
                current_app.logger.error(f"Error loading user: {str(e)}")
                return None

    async def register_user(
        self, email: str, password: str, **kwargs
    ) -> Optional[User]:
        """Register a new user in the system."""
        db = current_app.extensions.get("db")
        if not db:
            return None

        # Check if user already exists
        existing_user = await db.get_user_by_email(email)
        if existing_user:
            return None

        # Create new user with hashed password
        hashed_pw, salt = User.hash_password(password)
        user_id = str(uuid.uuid4())

        user_data = {
            "id": user_id,
            "email": email,
            "password_hash": hashed_pw,
            "password_salt": salt,
            "created_at": datetime.now(),
            "is_active": True,
            **kwargs,
        }

        # Save to database
        try:
            await db.create_user(user_data)
            return User(user_id=user_id, email=email, **kwargs)
        except Exception as e:
            current_app.logger.error(f"Error creating user: {str(e)}")
            return None

    async def login(self, email: str, password: str) -> Optional[User]:
        """Log a user in by email and password."""
        db = current_app.extensions.get("db")
        if not db:
            return None

        # Get user from database
        user_data = await db.get_user_by_email(email)
        if not user_data:
            return None

        # Verify password
        if not User.verify_password(
            password, user_data["password_hash"], user_data["password_salt"]
        ):
            return None

        # Update last login
        await db.update_user_login(user_data["id"])

        # Create user object
        user = User(
            user_id=user_data["id"],
            email=user_data["email"],
            is_active=user_data.get("is_active", True),
            created_at=user_data.get("created_at"),
            last_login=datetime.now(),
            profile=user_data.get("profile", {}),
        )

        # Use Flask-Login to log in user
        login_user(user)
        return user

    def logout(self) -> None:
        """Log the current user out."""
        logout_user()
