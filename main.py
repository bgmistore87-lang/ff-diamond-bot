import telebot
from telebot import types

BOT_TOKEN = "8859528898:AAFp96UIA3T2iH8ri1BF-kUnrjit_O1JIvE"
ADMIN_ID = 8859528898
QR_CODE_URL = "https://ibb.co/SXPpkLjG"

bot = telebot.TeleBot(BOT_TOKEN)
bot.remove_webhook()

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("💎 Buy Free Fire Diamonds")
    btn2 = types.KeyboardButton("📜 Pricing & Offers")
    btn3 = types.KeyboardButton("📞 Customer Support")
    btn4 = types.KeyboardButton("ℹ️ How It Works")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 <b>Welcome to Official Free Fire Diamond Store!</b>\n\n"
        "⚡ <i>Fast & Secure Top-Up Service</i>\n"
        "🛡️ 100% Safe & Verified Direct Top-Up\n\n"
        "Please select an option from the menu below to proceed:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text in ["💎 Buy Free Fire Diamonds", "📜 Pricing & Offers"])
def show_plans(message):
    plans_text = (
        "💎 <b>OFFICIAL TOP-UP PACKAGES</b> 💎\n"
        "────────────────────────\n\n"
        "🔹 <b>Pack 1:</b> 800 Diamonds ➔ <b>₹200</b>\n"
        "🔹 <b>Pack 2:</b> 1900 Diamonds ➔ <b>₹400</b>\n"
        "🔥 <b>Mega Deal:</b> 7500 Diamonds ➔ <b>₹600</b>\n\n"
        "<i>Select a package below to get payment details:</i>"
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("💳 Buy 800 Diamonds (₹200)", callback_data="plan_200")
    btn2 = types.InlineKeyboardButton("💳 Buy 1900 Diamonds (₹400)", callback_data="plan_400")
    btn3 = types.InlineKeyboardButton("🔥 Buy 7500 Diamonds (₹600)", callback_data="plan_600")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, plans_text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📞 Customer Support")
def customer_support(message):
    support_text = (
        "🎧 <b>CUSTOMER SUPPORT</b>\n"
        "────────────────────────\n\n"
        "Agar aapko payment ya top-up me koi help chahiye, toh aap direct message/screenshot yahan bhej sakte hain.\n\n"
        "⏱️ <b>Working Hours:</b> 24x7 Active\n"
        "📩 <b>Response Time:</b> Within 10-30 minutes"
    )
    bot.send_message(message.chat.id, support_text, parse_mode="HTML")

@bot.message_handler(func=lambda message: message.text == "ℹ️ How It Works")
def how_it_works(message):
    guide_text = (
        "📖 <b>HOW TO BUY DIAMONDS</b>\n"
        "────────────────────────\n\n"
        "1️⃣ Click on <b>'💎 Buy Free Fire Diamonds'</b>\n"
        "2️⃣ Select your desired diamond pack.\n"
        "3️⃣ Scan the QR code and complete the payment.\n"
        "4️⃣ Send payment screenshot & your <b>Game Player ID (UID)</b> here.\n"
        "5️⃣ Diamonds will be credited within <b>15-30 minutes</b>."
    )
    bot.send_message(message.chat.id, guide_text, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data.startswith('plan_'))
def handle_plan_selection(call):
    plan_details = ""
    if call.data == "plan_200":
        plan_details = "800 Diamonds (₹200)"
    elif call.data == "plan_400":
        plan_details = "1900 Diamonds (₹400)"
    elif call.data == "plan_600":
        plan_details = "7500 Diamonds (₹600 - Mega Deal)"

    payment_text = (
        f"🛍️ <b>ORDER SUMMARY</b>\n"
        f"────────────────────────\n"
        f"📦 <b>Selected Package:</b> {plan_details}\n"
        f"🛡️ <b>Security Status:</b> Verified & Secure Payment\n\n"
        f"📝 <b>INSTRUCTIONS:</b>\n"
        f"1. Scan the QR Code given above to complete payment.\n"
        f"2. After payment, send <b>Payment Screenshot</b> and <b>Game UID</b> in this chat.\n"
        f"3. Top-up processing time: <b>15 to 30 Minutes</b>.\n\n"
        f"⚠️ <i>Note: Fake screenshots are strictly prohibited and will lead to an immediate ban.</i>"
    )
    bot.send_photo(call.message.chat.id, photo=QR_CODE_URL, caption=payment_text, parse_mode="HTML")

@bot.message_handler(content_types=['photo', 'text'])
def forward_to_admin(message):
    if message.chat.id != ADMIN_ID:
        user_info = (
            f"📥 <b>NEW ORDER / PAYMENT RECEIVED</b>\n"
            f"────────────────────────\n"
            f"👤 <b>Customer Name:</b> {message.from_user.first_name}\n"
            f"🆔 <b>User ID:</b> <code>{message.from_user.id}</code>\n"
            f"🌐 <b>Username:</b> @{message.from_user.username if message.from_user.username else 'N/A'}"
        )
        bot.send_message(ADMIN_ID, user_info, parse_mode="HTML")
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        
        confirmation_msg = (
            "✅ <b>Details Received Successfully!</b>\n\n"
            "Aapki payment receipt aur UID verification ke liye submit ho gayi hai.\n"
            "⏳ <b>Processing Time:</b> 15 - 30 Minutes.\n\n"
            "<i>Kripya thoda wait karein, Admin aapka order jald hi complete kar dega.</i>"
        )
        bot.reply_to(message, confirmation_msg, parse_mode="HTML")

bot.infinity_polling()
