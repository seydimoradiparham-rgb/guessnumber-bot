import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions

TOKEN = os.environ["8529775830:AAHmRbz6XlustYqgnUjITkX8gSdq3hh-H8A"]  # توکن از Secret Replit یا GitHub Actions

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ====== تنظیمات مسابقه ======
game_running = False
target_number = 0
user_cooldowns = {}
COOLDOWN = 5  # ثانیه
admins = []  # اگه بخوای ایدی ادمین ها رو بذاری

# تابع شروع مسابقه
async def start_game(chat_id: int):
    global game_running, target_number, user_cooldowns
    game_running = True
    target_number = random.randint(1, 4000)
    user_cooldowns = {}
    await bot.send_message(chat_id, f"🎉 مسابقه حدس عدد شروع شد!\nیک عدد بین 1 تا 4000 حدس بزنید!")

# پردازش پیام‌ها
@dp.message_handler()
async def handle_guess(message: types.Message):
    global game_running
    if not game_running:
        return

    user_id = message.from_user.id

    # چک کردن تایمر ۵ ثانیه برای هر کاربر
    if user_id in user_cooldowns:
        remaining = COOLDOWN - (asyncio.get_event_loop().time() - user_cooldowns[user_id])
        if remaining > 0:
            await message.delete()
            return

    try:
        guess = int(str(message.text).replace("۰","0").replace("۱","1").replace("۲","2")
                        .replace("۳","3").replace("۴","4").replace("۵","5")
                        .replace("۶","6").replace("۷","7").replace("۸","8").replace("۹","9"))
    except ValueError:
        return

    user_cooldowns[user_id] = asyncio.get_event_loop().time()

    if guess == target_number:
        game_running = False
        await bot.send_message(message.chat.id,
                               f"🏆 تبریک {message.from_user.mention}!\nعدد درست {target_number} بود.\nمسابقه تمام شد!")
        # بستن گروه (میوت کردن همه)
        try:
            await bot.set_chat_permissions(message.chat.id, ChatPermissions(can_send_messages=False))
        except:
            pass
    elif guess < target_number:
        await message.reply("🔺 عدد بزرگتر است!")
    else:
        await message.reply("🔻 عدد کوچکتر است!")

# دستور شروع مسابقه توسط ادمین
@dp.message_handler(commands=["startgame"])
async def command_start(message: types.Message):
    if message.from_user.id in admins or message.chat.type == "private":
        await start_game(message.chat.id)
    else:
        await message.reply("❌ شما اجازه شروع مسابقه ندارید.")

# اجرای ربات
async def main():
    await dp.start_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
