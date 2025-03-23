import aiosqlite
from carbon_scanner.config import config
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple, Union
from flask import Flask, current_app

DATABASE_URL = config.DATABASE_URL


class DatabaseManager:
    def __init__(self, db_url: str = DATABASE_URL) -> None:
        self.db_url: str = db_url
        self.conn: Optional[aiosqlite.Connection] = None
        self._app: Optional[Flask] = None

    async def __aenter__(self) -> "DatabaseManager":
        self.conn = await aiosqlite.connect(self.db_url)
        await self._initialize_tables()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.conn:
            await self.conn.close()

    def init_app(self, app: Flask) -> None:
        """Initialize the database manager with a Flask application."""
        self._app = app

        # Register extension in Flask app
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["db"] = self

        # Configure teardown handler to close connections
        @app.teardown_appcontext
        async def close_connection(_: Optional[Exception]) -> None:
            if self.conn:
                await self.conn.close()
                self.conn = None

        # Register before_request handler to ensure connection is available
        @app.before_request
        async def ensure_connection() -> None:
            if not self.conn:
                self.conn = await aiosqlite.connect(self.db_url)
                await self._initialize_tables()

    async def _initialize_tables(self) -> None:
        # Create a simple users table and prompts table for storing context
        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT,
                email TEXT UNIQUE,
                password_hash TEXT,
                password_salt TEXT,
                created_at TEXT,
                last_login TEXT,
                coins INTEGER DEFAULT 0
            );
            """
        )
        await self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                prompt TEXT NOT NULL,
                context TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """
        )
        await self.conn.commit()

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a user by their ID."""
        cursor = await self.conn.execute(
            "SELECT id, email, password_hash, password_salt, created_at, last_login FROM users WHERE id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        if not row:
            return None

        # Convert row to dictionary
        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "password_salt": row[3],
            "created_at": row[4],
            "last_login": row[5],
        }

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by their email."""
        cursor = await self.conn.execute(
            "SELECT id, email, password_hash, password_salt, created_at, last_login FROM users WHERE email = ?",
            (email,),
        )
        row = await cursor.fetchone()
        if not row:
            return None

        # Convert row to dictionary
        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "password_salt": row[3],
            "created_at": row[4],
            "last_login": row[5],
        }

    async def create_user(self, user_data: Dict[str, Any]) -> None:
        await self.conn.execute(
            "INSERT INTO users (email, password_hash, password_salt, created_at) VALUES (?, ?, ?, ?)",
            (
                user_data["email"],
                user_data["password_hash"],
                user_data["password_salt"],
                str(user_data["created_at"]),
            ),
        )
        await self.conn.commit()

    async def update_user_login(self, user_id: str) -> None:
        await self.conn.execute(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (datetime.now().isoformat(), user_id),
        )
        await self.conn.commit()

    async def store_prompt_context(
        self, user_id: int, prompt: str, context: Optional[str] = None
    ) -> None:
        await self.conn.execute(
            "INSERT INTO prompts (user_id, prompt, context) VALUES (?, ?, ?)",
            (user_id, prompt, context),
        )
        await self.conn.commit()

    async def get_prompts_for_user(self, user_id: int) -> List[Tuple[int, str, str]]:
        cursor = await self.conn.execute(
            "SELECT id, prompt, context FROM prompts WHERE user_id = ?", (user_id,)
        )
        return await cursor.fetchall()

    async def get_coins_by_id(self, user_id: int) -> int:
        cursor = await self.conn.execute(
            "SELECT coins FROM users WHERE id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return 0
        return row[0] or 0

    async def get_coins_by_email(self, email: str) -> int:
        cursor = await self.conn.execute(
            "SELECT coins FROM users WHERE email = ?", (email,)
        )
        row = await cursor.fetchone()
        if not row:
            return 0
        return row[0] or 0

    async def update_coins_by_id(self, user_id: int, amount: int) -> bool:
        cursor = await self.conn.execute(
            "SELECT coins FROM users WHERE id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return False
        current_coins = row[0] or 0
        new_coins = current_coins + amount
        if new_coins < 0:
            return False
        await self.conn.execute(
            "UPDATE users SET coins = ? WHERE id = ?", (new_coins, user_id)
        )
        await self.conn.commit()
        return True

    async def update_coins_by_email(self, email: str, amount: int) -> bool:
        cursor = await self.conn.execute(
            "SELECT coins FROM users WHERE email = ?", (email,)
        )
        row = await cursor.fetchone()
        if not row:
            return False
        current_coins = row[0] or 0
        new_coins = current_coins + amount
        if new_coins < 0:
            return False
        await self.conn.execute(
            "UPDATE users SET coins = ? WHERE email = ?", (new_coins, email)
        )
        await self.conn.commit()
        return True
