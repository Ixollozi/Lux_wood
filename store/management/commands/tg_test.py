from django.core.management.base import BaseCommand
from django.conf import settings

from store.telegram_notify import send_telegram_message_debug

import asyncio


class Command(BaseCommand):
    help = "Test Telegram notifications (AsyncTeleBot). Usage: python manage.py tg_test \"hello\""

    def add_arguments(self, parser):
        parser.add_argument("text", nargs="?", default="✅ TG test message from LuxWood")

    def handle(self, *args, **options):
        token = getattr(settings, "TELEGRAM_BOT_TOKEN", "") or ""
        chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "") or ""

        self.stdout.write(f"TELEGRAM_BOT_TOKEN set: {'yes' if bool(token) else 'no'}")
        self.stdout.write(f"TELEGRAM_CHAT_ID: {chat_id!r}")

        if not token or not chat_id:
            self.stdout.write(self.style.ERROR("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in environment/.env first."))
            return

        ok, err = asyncio.run(send_telegram_message_debug(options["text"]))
        if ok:
            self.stdout.write(self.style.SUCCESS("Sent successfully"))
        else:
            self.stdout.write(self.style.ERROR(f"Send failed: {err}"))


