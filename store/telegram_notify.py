import asyncio
import threading
from typing import Optional

from django.conf import settings

try:
    from telebot.async_telebot import AsyncTeleBot
except Exception:  # pragma: no cover
    AsyncTeleBot = None  # type: ignore


def _get_bot() -> Optional["AsyncTeleBot"]:
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "") or ""
    if not token or AsyncTeleBot is None:
        return None
    return AsyncTeleBot(token, parse_mode="HTML")


def _get_chat_id() -> str:
    # Can be group id like -100123... or @channelusername
    return str(getattr(settings, "TELEGRAM_CHAT_ID", "") or "").strip()


async def send_telegram_message(text: str) -> bool:
    """
    Async отправка сообщения в TG группу/канал.
    Возвращает True/False (успех/нет).
    """
    chat_id = _get_chat_id()
    bot = _get_bot()
    if not chat_id or bot is None or not text:
        return False

    try:
        await bot.send_message(chat_id, text, disable_web_page_preview=True)
        return True
    except Exception:
        # Не падаем в проде из-за Telegram
        return False
    finally:
        # pyTelegramBotAPI async uses aiohttp under the hood; close session to avoid warnings
        try:
            await bot.close_session()
        except Exception:
            pass


async def send_telegram_message_debug(text: str) -> tuple[bool, str]:
    """
    Как send_telegram_message, но возвращает (ok, error_text) для диагностики.
    """
    chat_id = _get_chat_id()
    bot = _get_bot()
    if not chat_id:
        return False, "TELEGRAM_CHAT_ID is empty"
    if bot is None:
        return False, "Bot is not configured (missing token or pyTelegramBotAPI not installed)"
    if not text:
        return False, "Message text is empty"

    try:
        await bot.send_message(chat_id, text, disable_web_page_preview=True)
        return True, ""
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"
    finally:
        try:
            await bot.close_session()
        except Exception:
            pass


def send_telegram_message_bg(text: str) -> None:
    """
    Максимально простой "не блокирующий" вызов из синхронного Django кода:
    запускает отдельный поток и внутри выполняет asyncio.run(...)
    """

    def runner() -> None:
        try:
            asyncio.run(send_telegram_message(text))
        except Exception:
            pass

    t = threading.Thread(target=runner, daemon=True)
    t.start()


