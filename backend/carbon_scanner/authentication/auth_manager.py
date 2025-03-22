from flask import Flask, current_app, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from typing import Optional, Dict, Any
import uuid
import hashlib
import os
import re
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
    def sanitize_email(email: str) -> str:
        """
        Sanitize and ensure email is valid by:
        1. Removing invalid characters
        2. Replacing spaces with underscores
        3. Appending @genai4env.joefang.org if no domain
        """
        # Check if email is already valid
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return email

        # If no @ symbol, it's missing a domain
        if "@" not in email:
            # Sanitize the local part: remove invalid chars, replace spaces with underscores
            local_part = re.sub(
                r"[^a-zA-Z0-9._%+-]", "", email.strip().replace(" ", "_")
            )
            return f"{local_part}@genai4env.joefang.org"

        # If @ exists but email is still invalid, sanitize both parts
        local_part, domain = email.split("@", 1)
        local_part = re.sub(
            r"[^a-zA-Z0-9._%+-]", "", local_part.strip().replace(" ", "_")
        )

        # If domain doesn't have a dot or is otherwise invalid, replace with our domain
        if "." not in domain or not re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", domain):
            return f"{local_part}@genai4env.joefang.org"

        return f"{local_part}@{domain}"

    @staticmethod
    def hash_password(password: str) -> tuple[str, str]:
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
            db = current_app.extensions.get("db")
            if not db:
                return None
            try:
                # Implement a database call to retrieve user by their ID:
                user_data = await db.conn.execute(
                    "SELECT id, email, is_active, created_at, last_login FROM users WHERE id = ?",
                    (user_id,),
                )
                user_row = await user_data.fetchone()
                if user_row:
                    return User(
                        user_id=str(user_row[0]),
                        email=user_row[1],
                        is_active=(user_row[2] == 1),
                        created_at=user_row[3],
                        last_login=user_row[4],
                    )
                return None
            except Exception as e:
                current_app.logger.error(f"Error loading user: {str(e)}")
                return None

    async def register_user(
        self, email: str, password: str, **kwargs
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
    auth_manager = AuthManager(app)
    app.config["SECRET_KEY"] = "your_secret_key"
    app.config["DEBUG"] = True
