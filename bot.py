import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

# إعدادات تتبع الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دالة الترحيب /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'أهلاً بك! أنا بوت تحميل الفيديوهات 📥\n'
        'فقط قم بإرسال رابط فيديو من تيك توك أو إنستجرام وسأقوم بتحميله وإرساله لك فوراً!'
    )

# دالة التعامل مع الروابط وتحميل الفيديو
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # التحقق البسيط مما إذا كان الرسالة رابطاً
    if not url.startswith('http'):
        await update.message.reply_text('الرجاء إرسال رابط صحيح (من تيك توك أو إنستجرام).')
        return

    await update.message.reply_text('⏳ جاري المعالجة والتحميل، يرجى الانتظار قليلاً...')

    output_template = 'downloaded_video.mp4'

    # إعدادات مكتبة التحميل yt-dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
        'max_filesize': 50 * 1024 * 1024, # تحديد الحد الأقصى للحجم (50 ميجابايت لتناسب تيليجرام)
    }

    try:
        # تحميل الفيديو
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # إرسال الفيديو إلى المستخدم عبر تيليجرام
        with open(output_template, 'rb') as video_file:
            await update.message.reply_video(video=video_file)

        await update.message.reply_text('✅ تم إرسال الفيديو بنجاح!')

    except Exception as e:
        await update.message.reply_text(f'❌ حدث خطأ أثناء التحميل: تأكد من أن الرابط عام وصحيح.')
        print(f"Error: {e}")

    finally:
        # تنظيف الملف المؤقت من الجهاز بعد الإرسال
        if os.path.exists(output_template):
            os.remove(output_template)

if __name__ == '__main__':
    # ضع الـ Token الخاص بك هنا
    TOKEN = "8814413715:AAEOt1Nz_T78awGVnm9szvkRxhy08KQ7WO4"

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))

    print("بوت تحميل الفيديوهات يعمل الآن...")
    application.run_polling()