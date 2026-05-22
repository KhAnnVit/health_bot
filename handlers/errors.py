from aiogram import Router
from aiogram.types import ErrorEvent
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.errors()
async def global_error_handler(event: ErrorEvent):
    """Ловит ВСЕ необработанные ошибки"""
    logger.exception("Unhandled error in update %s: %s",
                     event.update.update_id, event.exception)