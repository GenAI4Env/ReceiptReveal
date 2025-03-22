import aiosqlite
from carbon_scanner.config import config
from datetime import datetime

DATABASE_URL = config.DATABASE_URL


class DatabaseManager:
    def __init__(self, db_url=DATABASE_URL):
        self.db_url = db_url
        self.conn = None

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_url)
        await self._initialize_tables()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

    async def _initialize_tables(self):
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
                is_active INTEGER DEFAULT 1,
                last_login TEXT
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

    async def get_user_by_email(self, email: str):
        cursor = await self.conn.execute(
            "SELECT id, email, password_hash, password_salt, created_at, is_active, last_login FROM users WHERE email = ?",
            (email,),
        )
        return await cursor.fetchone()

    async def create_user(self, user_data: dict):
        await self.conn.execute(
            "INSERT INTO users (id, email, password_hash, password_salt, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?)",
            (
                user_data["id"],
                user_data["email"],
                user_data["password_hash"],
                user_data["password_salt"],
                str(user_data["created_at"]),
                1 if user_data.get("is_active") else 0,
            ),
        )
        await self.conn.commit()

    async def update_user_login(self, user_id: str):
        await self.conn.execute(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (datetime.now().isoformat(), user_id),
        )
        await self.conn.commit()

    async def store_prompt_context(
        self, user_id: int, prompt: str, context: str = None
    ):
        await self.conn.execute(
            "INSERT INTO prompts (user_id, prompt, context) VALUES (?, ?, ?)",
            (user_id, prompt, context),
        )
        await self.conn.commit()

    async def get_prompts_for_user(self, user_id: int):
        cursor = await self.conn.execute(
            "SELECT id, prompt, context FROM prompts WHERE user_id = ?", (user_id,)
        )
        return await cursor.fetchall()
