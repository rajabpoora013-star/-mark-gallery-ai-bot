import os
import time
import requests

TOKEN = os.environ["RUBIKA_BOT_TOKEN"]
API = f"https://botapi.rubika.ir/v3/{TOKEN}"
session = requests.Session()

def api(method, data=None):
    response = session.post(
        f"{API}/{method}",
        json=data or {},
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    return result.get("data", result)

def reply_for(text, event_type=""):
    text = (text or "").strip().lower()

    if event_type == "StartedBot" or text in ("/start", "شروع"):
        return (
            "سلام! به دستیار هوشمند گالری مارک خوش آمدید 🌸\n"
            "می‌توانید درباره عطرها، انتخاب رایحه و ثبت سفارش سؤال کنید.\n"
            "برای دیدن راهنما، بنویسید «راهنما»."
        )

    if text in ("/help", "راهنما", "کمک"):
        return (
            "راهنمای گالری مارک:\n"
            "• برای راهنمای انتخاب عطر، بنویسید «راهنمای انتخاب عطر».\n"
            "• برای پرسش درباره قیمت یا موجودی، نام عطر را بفرستید.\n"
            "• برای پیگیری سفارش، با پشتیبانی فروشگاه تماس بگیرید."
        )

    if "قیمت" in text or "موجود" in text:
        return (
            "برای اعلام قیمت و موجودی دقیق، لطفاً نام کامل عطر را بفرستید. "
            "اگر اطلاعات آن در دسترس نباشد، شما را به پشتیبانی فروشگاه راهنمایی می‌کنم."
        )

    if "انتخاب" in text or "چه عطری" in text or "پیشنهاد" in text:
        return (
            "برای پیشنهاد مناسب‌تر، بگویید عطر را برای چه موقعیتی می‌خواهید "
            "(روزمره، محل کار یا مهمانی) و چه نوع رایحه‌ای می‌پسندید "
            "(خنک، شیرین، تلخ یا گرم)."
        )

    if "سفارش" in text or "خرید" in text:
        return (
            "برای ثبت یا پیگیری سفارش، لطفاً نام عطر موردنظر را بفرستید. "
            "تأیید نهایی قیمت، موجودی و سفارش با پشتیبانی فروشگاه است."
        )

    if "سلام" in text or "درود" in text:
        return "سلام! چطور می‌توانم درباره عطرها کمکتان کنم؟"

    return (
        "پیامتان را دریافت کردم. درباره نام عطر، رایحه، قیمت یا موجودی سؤال کنید؛ "
        "برای اطلاعات قطعیِ محصول، ممکن است لازم باشد از پشتیبانی فروشگاه کمک بگیرید."
    )

def main():
    offset_id = None
    print("ربات شروع به کار کرد.")

    while True:
        try:
            payload = {"limit": 10}
            if offset_id:
                payload["offset_id"] = offset_id

            result = api("getUpdates", payload)

            for update in result.get("updates", []):
                offset_id = result.get("next_offset_id") or offset_id

                message = update.get("new_message") or {}
                chat_id = update.get("chat_id")
                text = message.get("text", "")

                if not chat_id:
                    continue
                if message.get("sender_type") == "Bot":
                    continue

                answer = reply_for(text, update.get("type", ""))
                api("sendMessage", {"chat_id": str(chat_id), "text": answer})

            offset_id = result.get("next_offset_id") or offset_id
            time.sleep(2)

        except Exception as error:
            print(f"خطا: {error}")
            time.sleep(5)

if __name__ == "__main__":
    main()
