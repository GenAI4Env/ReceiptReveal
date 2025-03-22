import aiosqlite
from carbon_scanner.config import config

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
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
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

    async def add_user(self, username: str, password: str):
        await self.conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        await self.conn.commit()

    async def get_user(self, username: str):
        cursor = await self.conn.execute(
            "SELECT id, username, password FROM users WHERE username = ?", (username,)
        )
        return await cursor.fetchone()

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
