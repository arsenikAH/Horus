
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading
import time

TOKEN = "7604112467:AAEu1_yuAHXqtjk8xiWFZbiMlW6IFnhLIDI"
ADMIN_ID = 6314729119

CHANNELS = []

post_data = {
    "stage": None,
    "message": None,
    "interval": None,
    "broadcasting": False
}

def start(update, context):
    if update.message.from_user.id != ADMIN_ID:
        return
    update.message.reply_text("📢 هل القناة خاصة أم عامة؟

أرسل:
- 'خاصة' إذا كانت خاصة
- أو أرسل اسم القناة (مثلاً: @unkwoun159)")

def change(update, context):
    if update.message.from_user.id != ADMIN_ID:
        return
    post_data["stage"] = "waiting_for_post"
    update.message.reply_text("📩 أرسل الرسالة التي تريد إذاعتها في القنوات.")

def stop(update, context):
    if update.message.from_user.id != ADMIN_ID:
        return
    post_data["broadcasting"] = False
    update.message.reply_text("⛔ تم إيقاف الإذاعة التلقائية.")

def handle_message(update, context):
    if update.message.from_user.id != ADMIN_ID:
        return

    msg = update.message.text

    if post_data["stage"] is None and not CHANNELS:
        if msg.lower() == "خاصة":
            update.message.reply_text("✅ سيتم استخدام القناة الخاصة التي أنت مشرف بها.")
            CHANNELS.append(update.message.chat_id)
        elif msg.startswith("@"):
            CHANNELS.append(msg)
            update.message.reply_text(f"✅ تم تسجيل القناة: {msg}")
        return

    if post_data["stage"] == "waiting_for_post":
        post_data["message"] = update.message
        post_data["stage"] = "waiting_for_interval"
        update.message.reply_text("⏱️ أرسل عدد الدقائق بين كل نشر (مثلاً 2).")
    elif post_data["stage"] == "waiting_for_interval":
        try:
            interval = int(msg)
            post_data["interval"] = interval
            post_data["stage"] = None
            post_data["broadcasting"] = True
            update.message.reply_text(f"✅ سيتم إرسال المنشور كل {interval} دقيقة.")
            threading.Thread(target=broadcast_loop, args=(context.bot,)).start()
        except ValueError:
            update.message.reply_text("❌ أرسل رقم صحيح.")

def broadcast_loop(bot):
    while post_data["broadcasting"]:
        for channel in CHANNELS:
            try:
                bot.copy_message(
                    chat_id=channel,
                    from_chat_id=post_data["message"].chat_id,
                    message_id=post_data["message"].message_id
                )
                print(f"✅ تم النشر في {channel}")
            except Exception as e:
                print(f"⚠️ خطأ في النشر في {channel}: {e}")
        time.sleep(post_data["interval"] * 60)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("change", change))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(MessageHandler(Filters.all, handle_message))

    updater.start_polling()
    updater.idle()

main()
