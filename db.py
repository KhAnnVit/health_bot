
import asyncpg
from config import DATABASE_URL
from typing import List, Optional, Dict

DB_URL = DATABASE_URL

pool = None


async def init_db():
    """Создаёт пул соединений и таблицы"""
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

    async with pool.acquire() as conn:
        # Таблица пользователей
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id BIGINT PRIMARY KEY,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Таблица веса
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS weight_logs (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
                weight DECIMAL(5,2) NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                note TEXT
            )
        """)

        # Таблица давления
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS pressure_logs (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
                systolic INTEGER NOT NULL,
                diastolic INTEGER NOT NULL,
                pulse INTEGER,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                note TEXT
            )
        """)

    print("✅ База данных готова!")


async def add_user(telegram_id, username):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (telegram_id, username)
            VALUES ($1, $2)
            ON CONFLICT (telegram_id) DO UPDATE SET username = $2
        """, telegram_id, username)


async def add_weight(telegram_id, weight, note=None):
    async with pool.acquire() as conn:
        await add_user(telegram_id, "")
        await conn.execute("""
            INSERT INTO weight_logs (telegram_id, weight, note)
            VALUES ($1, $2, $3)
        """, telegram_id, weight, note)


async def add_pressure(telegram_id, systolic, diastolic, pulse=None, note=None):
    async with pool.acquire() as conn:
        await add_user(telegram_id, "")
        await conn.execute("""
            INSERT INTO pressure_logs (telegram_id, systolic, diastolic, pulse, note)
            VALUES ($1, $2, $3, $4, $5)
        """, telegram_id, systolic, diastolic, pulse, note)


async def get_weight_history(telegram_id, limit=10):
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT weight, recorded_at, note
            FROM weight_logs
            WHERE telegram_id = $1
            ORDER BY recorded_at DESC
            LIMIT $2
        """, telegram_id, limit)
        return [dict(row) for row in rows]


async def get_pressure_history(telegram_id, limit=10):
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT systolic, diastolic, pulse, recorded_at, note
            FROM pressure_logs
            WHERE telegram_id = $1
            ORDER BY recorded_at DESC
            LIMIT $2
        """, telegram_id, limit)
        return [dict(row) for row in rows]


async def close_db():
    if pool:
        await pool.close()