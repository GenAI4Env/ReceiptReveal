from flask import Flask, current_app, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from typing import Optional, Dict, Any, Tuple, Union, List, Callable
import uuid
import hashlib
import os
import re
import base64
from datetime import datetime
from carbon_scanner.database.db_manager import DatabaseManager


class User(UserMixin):
    """User class that implements UserMixin for Flask-Login compatibility."""

    def __init__(self, user_id: str, email: str, **kwargs: Any) -> None:
        self.id: str = user_id
        self.email: str = email
        self.is_active: bool = kwargs.get("is_active", True)
        self.is_authenticated: bool = kwargs.get("is_authenticated", True)
        self.created_at: datetime = kwargs.get("created_at", datetime.now())
        self.last_login: Optional[Union[str, datetime]] = kwargs.get("last_login", None)
        self.profile: Dict[str, Any] = kwargs.get("profile", {})

    @staticmethod
    def sanitize_email(email: str) -> str:
        """
        Validate email or encode it if invalid:
        1. Check if email is valid with a simple regex
        2. If invalid, encode the entire string and use it as the local part
        """
        # Check if email is already valid with a single regex
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return email

        # If email is invalid, encode the entire string to ensure it's safe
        # Use urlsafe base64 encoding (removing padding characters)
        encoded_email = base64.b32hexencode(email.encode()).decode().lower()
        return f"{encoded_email}@genai4env.joefang.org"

    @staticmethod
    def hash_password(password: str) -> Tuple[str, str]:
        """Hash a password with a salt."""
        salt = os.urandom(16)
        hashed_pw = hashlib.sha256(salt + password.encode("utf-8")).hexdigest()
        return hashed_pw, salt.hex()

    @staticmethod
    def verify_password(password: str, salt: str, hashed_pw: str) -> bool:
        """Verify a password against a hash and salt."""
        test_hash = hashlib.sha256(
            bytes.fromhex(salt) + password.encode("utf-8")
        ).hexdigest()
        return test_hash == hashed_pw


class AuthManager:
    """Manages authentication using Flask-Login."""

    def __init__(self, app: Optional[Flask] = None) -> None:
        self.login_manager: LoginManager = LoginManager()
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
            # Get db from Flask extensions
            db: Optional[DatabaseManager] = current_app.extensions.get("db")
            if not db:
                current_app.logger.error("Database extension not initialized")
                return None

            try:
                # Use the db_manager method to retrieve user
                user_data = await db.get_user_by_id(user_id)
                if user_data:
                    return User(
                        user_id=str(user_data["id"]),
                        email=user_data["email"],
                        is_active=user_data["is_active"],
                        created_at=user_data["created_at"],
                        last_login=user_data["last_login"],
                    )
                return None
            except Exception as e:
                current_app.logger.error(f"Error loading user: {str(e)}")
                return None

    async def register_user(
        self, email: str, password: str, **kwargs: Any
    ) -> Optional[User]:
        """Register a new user in the system."""
        # Sanitize email before registration
        sanitized_email = User.sanitize_email(email)

        db = current_app.extensions.get("db")
        if not db:
            return None

        # Check if user already exists
        existing_user = await db.get_user_by_email(sanitized_email)
        if existing_user:
            return None

        # Create new user with hashed password
        hashed_pw, salt = User.hash_password(password)
        user_id = str(uuid.uuid4())

        user_data = {
            "id": user_id,
            "email": sanitized_email,
            "password_hash": hashed_pw,
            "password_salt": salt,
            "created_at": datetime.now(),
            "is_active": True,
            **kwargs,
        }

        # Save to database
        try:
            await db.create_user(user_data)
            return User(user_id=user_id, email=sanitized_email, **kwargs)
        except Exception as e:
            current_app.logger.error(f"Error creating user: {str(e)}")
            return None

    async def login(self, email: str, password: str) -> Optional[User]:
        """Log a user in by email and password."""
        # Sanitize email before login
        sanitized_email = User.sanitize_email(email)

        db = current_app.extensions.get("db")
        if not db:
            return None

        # Get user from database
        user_data = await db.get_user_by_email(sanitized_email)
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


if __name__ == "__main__":
    # Example usage
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your_secret_key"
    app.config["DEBUG"] = True

    # Initialize database extension first
    db_manager = DatabaseManager()
    db_manager.init_app(app)

    # Then initialize auth manager
    auth_manager = AuthManager(app)
