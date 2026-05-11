import asyncpg
from asyncpg import PostgresError
from typing import Optional, Dict, Any, List
from config import DATABASE_URL

# Глобальный пул
pool: Optional[asyncpg.Pool] = None


async def init_db():
    """Инициализация пула соединений. Вызывается ОДИН раз при старте."""
    global pool
    if pool is not None:
        return  # Уже создан, не создаём дубликат

    try:
        pool = await asyncpg.create_pool(
            dsn=DATABASE_URL,
            min_size=2,
            max_size=10,
            command_timeout=10,  # Макс. время выполнения запроса
            statement_cache_size=50  # Кэш планов запросов
        )
        print("✅ Пул соединений создан")
    except Exception as e:
        raise RuntimeError(f"❌ Ошибка подключения к БД: {e}") from e


async def close_db():
    """Безопасное закрытие пула. Вызывается при остановке бота."""
    global pool
    if pool:
        await pool.close()
        pool = None
        print("🔌 Пул соединений закрыт")


def _check_pool():
    """Защита от вызова БД до инициализации"""
    if pool is None:
        raise RuntimeError("🔌 БД не инициализирована. Вызовите await init_db() в main.py")


# ─── Пользователи ───
async def upsert_user(telegram_id: int, username: Optional[str] = None):
    """Добавляет или обновляет пользователя. Не затирает username, если пришёл None."""
    _check_pool()
    async with pool.acquire() as conn:
        try:
            await conn.execute("""
                INSERT INTO users (telegram_id, username, created_at)
                VALUES ($1, $2, NOW())
                ON CONFLICT (telegram_id) DO UPDATE
                SET username = COALESCE(EXCLUDED.username, users.username)
            """, telegram_id, username)
        except PostgresError as e:
            raise RuntimeError(f"Ошибка записи пользователя: {e}") from e


# ─── Вес ───
async def add_weight(telegram_id: int, weight: float, note: Optional[str] = None):
    """Сохраняет запись о весе. Вызов upsert_user УБРАН отсюда."""
    _check_pool()
    async with pool.acquire() as conn:
        try:
            await conn.execute("""
                INSERT INTO weight_logs (telegram_id, weight, note, recorded_at)
                VALUES ($1, $2, $3, NOW())
            """, telegram_id, weight, note)
        except PostgresError as e:
            raise RuntimeError(f"Ошибка записи веса: {e}") from e


async def get_weight_history(telegram_id: int, limit: int = 30) -> List[asyncpg.Record]:
    _check_pool()
    async with pool.acquire() as conn:
        try:
            return await conn.fetch("""
                SELECT id, weight, note, recorded_at
                FROM weight_logs
                WHERE telegram_id = $1
                ORDER BY recorded_at DESC
                LIMIT $2
            """, telegram_id, limit)
        except PostgresError as e:
            raise RuntimeError(f"Ошибка выборки веса: {e}") from e


# ─── Давление ───
async def add_pressure(telegram_id: int, systolic: int, diastolic: int, pulse: int, note: Optional[str] = None):
    _check_pool()
    async with pool.acquire() as conn:
        try:
            await conn.execute("""
                INSERT INTO pressure_logs (telegram_id, systolic, diastolic, pulse, note, recorded_at)
                VALUES ($1, $2, $3, $4, $5, NOW())
            """, telegram_id, systolic, diastolic, pulse, note)
        except PostgresError as e:
            raise RuntimeError(f"Ошибка записи давления: {e}") from e


async def get_pressure_history(telegram_id: int, limit: int = 30) -> List[asyncpg.Record]:
    _check_pool()
    async with pool.acquire() as conn:
        try:
            return await conn.fetch("""
                SELECT id, systolic, diastolic, pulse, note, recorded_at
                FROM pressure_logs
                WHERE telegram_id = $1
                ORDER BY recorded_at DESC
                LIMIT $2
            """, telegram_id, limit)
        except PostgresError as e:
            raise RuntimeError(f"Ошибка выборки давления: {e}") from e




async def get_profile(telegram_id: int) -> Optional[Dict[str, Any]]:
    """Возвращает профиль + последний записанный вес"""
    _check_pool()
    async with pool.acquire() as conn:
        profile = await conn.fetchrow("""
            SELECT telegram_id, username, full_name, gender, age, height_cm, target_weight_kg
            FROM users WHERE telegram_id = $1
        """, telegram_id)

        # Берём последний вес из логов
        last_weight = await conn.fetchval("""
            SELECT weight FROM weight_logs 
            WHERE telegram_id = $1 ORDER BY recorded_at DESC LIMIT 1
        """, telegram_id)

        if profile:
            data = dict(profile)
            data['current_weight'] = last_weight
            return data
        return None


async def update_profile_field(telegram_id: int, field: str, value) -> None:
    """Безопасно обновляет одно поле профиля"""
    _check_pool()
    allowed_fields = {'full_name', 'gender', 'age', 'height_cm', 'target_weight_kg'}
    if field not in allowed_fields:
        raise ValueError(f"Недопустимое поле: {field}")

    async with pool.acquire() as conn:
        await conn.execute(
            f"UPDATE users SET {field} = $2 WHERE telegram_id = $1",
            telegram_id, value
        )

