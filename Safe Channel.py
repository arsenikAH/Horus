from telegram.ext import Updater, MessageHandler, Filters
from telegram.error import TelegramError

TOKEN = "6157765553:AAE6rmFpm3zi6XxPlDz_9nNKfTs85EH99jo"
OWNER_ID = 5568171362  # رقمك الشخصي
REQUIRED_TEXT = "S_L_V_0"
REQUIRED_TITLE = "AH Army"

def handle_channel_post(update, context):
    if update.channel_post:
        message = update.channel_post
        chat_id = message.chat_id
        msg_id = message.message_id

        # النص سواء من text أو caption
        text = message.text or message.caption or ""

        # إذا الرسالة لا تحتوي على النص المطلوب
        if REQUIRED_TEXT not in text:
            try:
                context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
                context.bot.send_message(chat_id=OWNER_ID, text="🗑️ تم حذف رسالة لا تحتوي على النص المطلوب.")
            except Exception as e:
                context.bot.send_message(chat_id=OWNER_ID, text=f"❌ خطأ أثناء حذف الرسالة:\n{e}")
        else:
            context.bot.send_message(chat_id=OWNER_ID, text="✅ تم السماح برسالة تحتوي على النص المطلوب.")

        # التحقق وتغيير اسم القناة إذا لزم
        try:
            chat = context.bot.get_chat(chat_id)
            if chat.title != REQUIRED_TITLE:
                context.bot.set_chat_title(chat_id=chat_id, title=REQUIRED_TITLE)
                context.bot.send_message(chat_id=OWNER_ID, text=f"✏️ تم تعديل اسم القناة إلى: {REQUIRED_TITLE}")
        except TelegramError as e:
            context.bot.send_message(chat_id=OWNER_ID, text=f"⚠️ تعذر تعديل اسم القناة:\n{e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.update.channel_posts, handle_channel_post))

    updater.start_polling()
    updater.bot.send_message(chat_id=OWNER_ID, text="🤖 البوت بدأ العمل بنجاح!")
    updater.idle()

if __name__ == '__main__':
    main()
