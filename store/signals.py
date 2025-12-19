from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import escape

from .models import Order, ContactMessage
from .telegram_notify import send_telegram_message_bg


def _money(v) -> str:
    try:
        return f"{v} сум"
    except Exception:
        return str(v)


# Отключено: уведомления о заказах отправляются напрямую из views.py (checkout)
# @receiver(post_save, sender=Order)
# def notify_new_order(sender, instance: Order, created: bool, **kwargs):
#     # Уведомляем только при создании заказа (покупка)
#     if not created or not instance:
#         return
#
#     text = (
#         "🛒 <b>Новый заказ</b>\n"
#         f"№ <b>{escape(str(instance.id))}</b>\n\n"
#         f"👤 {escape(instance.full_name)}\n"
#         f"📞 {escape(instance.phone)}\n"
#         f"📧 {escape(instance.email)}\n\n"
#         f"📍 {escape(instance.city)}\n"
#         f"{escape(instance.address)}\n\n"
#         f"📦 Позиций: <b>{escape(str(instance.items_count))}</b>\n"
#         f"💰 Сумма: <b>{escape(_money(instance.total_price))}</b>"
#     )
#     send_telegram_message_bg(text)


@receiver(post_save, sender=ContactMessage)
def notify_contact_message(sender, instance: ContactMessage, created: bool, **kwargs):
    # Уведомляем только при создании обращения (обратная связь)
    if not created or not instance:
        return

    msg = (instance.message or "").strip()
    if len(msg) > 800:
        msg = msg[:800] + "..."

    phone = (instance.phone or "").strip()

    text = (
        "✉️ <b>Новое сообщение (обратная связь)</b>\n\n"
        f"👤 {escape(instance.name)}\n"
        f"📧 {escape(instance.email)}\n"
        + (f"📞 {escape(phone)}\n" if phone else "")
        + "\n"
        f"🧾 <b>Тема:</b> {escape(instance.subject)}\n"
        f"💬 <b>Сообщение:</b>\n<pre>{escape(msg)}</pre>"
    )
    send_telegram_message_bg(text)


