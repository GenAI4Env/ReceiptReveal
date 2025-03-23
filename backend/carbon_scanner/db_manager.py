async def create_tables(self):
    async with self.pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                coins INTEGER DEFAULT 0
            )
        ''')

async def increment_coins(self, user_id: int, amount: int = 10):
    async with self.pool.acquire() as conn:
        await conn.execute('''
            UPDATE users 
            SET coins = coins + ? 
            WHERE id = ?
        ''', (amount, user_id)) 