from telebot import TeleBot, types
from datetime import datetime
import uuid
import os

TOKEN = '8170096029:AAHUl6fktOfPyrFON-60H4n8hsSAsgRF8E0'
bot = TeleBot(TOKEN)

SUPPORT_USERNAME = "@jiinwoo777"
BOT_USERNAME = "Cuentas_gratiss_bot"
PROMO_CODES_FILE = ".account/promo_codes.txt"
MESSAGES_LOG_FILE = ".account/messages_log.txt"
REFERRALS_FILE = ".account/referrals.txt"
POINTS_FILE = ".account/points.txt"
CHANNEL_USERNAME = "@membersb7757gbfbgsvdssdv"
NOTIFICATION_CHAT_ID = "@membersb7757gbfbgsvdssdv"

points = {}
user_languages = {}
user_accounts_given = {}
user_referrals = {}
account_usage_count = {}
used_promo_codes = set()

accounts_files = {
    'Crunchyroll': '.account/crunchyroll.txt',
    'Paramount': '.account/paramount.txt',
    'Disney': '.account/disney.txt',
    'Netflix': '.account/netflix.txt',
    'Steam': '.account/steam.txt',
    'Xbox': '.account/xbox.txt',
    'Express VPN': '.account/expressvpn.txt',
    'Nord VPN': '.account/nordvpn.txt',
}

accounts_data = {}
promo_codes = []

translations = {
    'choose_language': {
        'ar': "اختر لغتك:",
        'en': "Choose your language (We encourage using Arabic for better understanding):",
        'es': "Elige tu idioma (Te recomendamos usar árabe para una mejor comprensión):"
    },
    'language_chosen': {
        'ar': "تم اختيار اللغة: {}. كيف يمكنني مساعدتك؟",
        'en': "Language chosen: {}. How can I help you?",
        'es': "Idioma elegido: {}. ¿Cómo puedo ayudarte?"
    },
    'main_menu_options': {
        'ar': ["🚀 الدخول إلى القناة الخاصة", "🎁 الحصول على حساب", "📊 العروض المتاحة", "🔑 إدخال كود ترويجي", "📈 نقاطي", "🎉 الدخول إلى القناة العامة"],
        'en': ["🚀 Join Private Channel", "🎁 Get Account", "📊 Available Offers", "🔑 Enter Promo Code", "📈 My Points", "🎉 Join Public Channel"],
        'es': ["🚀 Unirse al canal privado", "🎁 Obtener cuenta", "📊 Ofertas disponibles", "🔑 Ingresar código promocional", "📈 Mis puntos", "🎉 Unirse al canal público"]
    },
    'join_private_channel': {
        'ar': (
            "🚀 للدخول إلى القناة الخاصة التي تحتوي على حسابات متعددة وشغالة، أكمل العرض التالي:\n"
            "🔗 رابط العرض: https://crunchyrolloferta.netlify.app/\n\n"
            "📋 تعليمات:\n"
            "- عند إكمال العرض، قد يُطلب منك تنزيل تطبيق، مشاهدة إعلان، أو استكمال استبيان.\n"
            "- الموقع سيوجهك تلقائيًا إلى القناة الخاصة بعد الإكمال.\n"
            "- العرض قد يستغرق دقيقتين كحد أقصى.\n"
            "ابدأ الآن واستمتع بالحسابات المميزة!"
        ),
        'en': (
            "🚀 To join the private channel with multiple active accounts, complete the following offer:\n"
            "🔗 Offer Link: https://crunchyrolloferta.netlify.app/\n\n"
            "📋 Instructions:\n"
            "- Upon completing the offer, you may need to download an app, watch an ad, or complete a survey.\n"
            "- The website will automatically redirect you to the private channel after completion.\n"
            "- The offer may take up to 2 minutes.\n"
            "Start now and enjoy premium accounts!"
        ),
        'es': (
            "🚀 Para unirte al canal privado con múltiples cuentas activas, completa la siguiente oferta:\n"
            "🔗 Enlace de la oferta: https://crunchyrolloferta.netlify.app/\n\n"
            "📋 Instrucciones:\n"
            "- Al completar la oferta, es posible que debas descargar una aplicación, ver un anuncio o completar una encuesta.\n"
            "- El sitio web te redirigirá automáticamente al canal privado después de completar.\n"
            "- La oferta puede tomar hasta 2 minutos.\n"
            "¡Empieza ahora y disfruta de cuentas premium!"
        )
    },
    'join_public_channel': {
        'ar': (
            "🎉 إذا أردت الدخول إلى القناة العامة، راسل مشرف القناة:\n"
            "@jiinwoo777\n\n"
            "هناك هدايا 🎁، جوائز، وحسابات مجانية! تواصل مع المشرف الآن."
        ),
        'en': (
            "🎉 To join the public channel, contact the channel admin:\n"
            "@jiinwoo777\n\n"
            "There are free gifts 🎁, prizes, and free accounts! Message the admin now."
        ),
        'es': (
            "🎉 Para unirte al canal público, contacta al administrador del canal:\n"
            "@jiinwoo777\n\n"
            "¡Hay regalos 🎁, premios y cuentas gratis! Envía un mensaje al administrador ahora."
        )
    },
    'my_points': {
        'ar': "📈 لديك {} نقاط بناءً على الإحالات. قم بدعوة المزيد من الأصدقاء باستخدام رابطك: {}",
        'en': "📈 You have {} points based on referrals. Invite more friends using your link: {}",
        'es': "📈 Tienes {} puntos basados en referidos. Invita a más amigos usando tu enlace: {}"
    },
    'not_enough_points': {
        'ar': (
            "لديك {} نقاط، تحتاج إلى 10 نقاط على الأقل للحصول على حساب.\n"
            "قم بدعوة أصدقائك باستخدام رابط الإحالة الخاص بك:\n"
            "{}\nكل شخص ينضم عبر رابطك يمنحك نقطة واحدة!"
        ),
        'en': (
            "You have {} points, you need at least 10 points to get an account.\n"
            "Invite your friends using your referral link:\n"
            "{}\nEach person who joins via your link gives you one point!"
        ),
        'es': (
            "Tienes {} puntos, necesitas al menos 10 puntos para obtener una cuenta.\n"
            "Invita a tus amigos usando tu enlace de referencia:\n"
            "{}\n¡Cada persona que se una a través de tu enlace te da un punto!"
        )
    },
    'choose_account_type': {
        'ar': "اختر نوع الحساب الذي تريد:",
        'en': "Choose the account type you want:",
        'es': "Elige el tipo de cuenta que deseas:"
    },
    'no_accounts_available': {
        'ar': "عذرًا، لا توجد حسابات متاحة لهذا النوع حاليًا.",
        'en': "Sorry, there are no accounts available for this type at the moment.",
        'es': "Lo siento, no hay cuentas disponibles para este tipo en este momento."
    },
    'account_given': {
        'ar': "إليك حساب {} الخاص بك:\n{}",
        'en': "Here is your {} account:\n{}",
        'es': "Aquí está tu cuenta de {}:\n{}"
    },
    'go_back': {
        'ar': "⬅️ رجوع",
        'en': "⬅️ Back",
        'es': "⬅️ Volver"
    },
    'previous_menu': {
        'ar': "⬅️ العودة إلى القائمة السابقة",
        'en': "⬅️ Return to Previous Menu",
        'es': "⬅️ Volver al Menú Anterior"
    },
    'back_to_main_menu': {
        'ar': "تم العودة إلى القائمة الرئيسية. كيف يمكنني مساعدتك؟",
        'en': "Returned to main menu. How can I help you?",
        'es': "Volviste al menú principal. ¿Cómo puedo ayudarte?"
    },
    'invalid_option': {
        'ar': "الرجاء اختيار خيار صحيح. للمساعدة، تواصل مع {}.",
        'en': "Please choose a valid option. For help, contact {}.",
        'es': "Por favor elige una opción válida. Para ayuda, contacta {}."
    },
    'available_offers': {
        'ar': "📋 العروض المتاحة:\n{}",
        'en': "📋 Available offers:\n{}",
        'es': "📋 Ofertas disponibles:\n{}"
    },
    'enter_promo_code': {
        'ar': "أدخل الكود الترويجي:",
        'en': "Enter your promo code:",
        'es': "Ingresa tu código promocional:"
    },
    'valid_promo_code': {
        'ar': "الكود الترويجي صالح! اختر نوع الحساب الذي تريد:",
        'en': "Valid promo code! Choose the account type you want:",
        'es': "¡Código promocional válido! Elige el tipo de cuenta que deseas:"
    },
    'invalid_promo_code': {
        'ar': "الكود الترويجي غير صالح أو تم استخدامه. حاول مرة أخرى أو تواصل مع {} للمساعدة.",
        'en': "Invalid or already used promo code. Try again or contact {} for help.",
        'es': "Código promocional inválido o ya usado. Inténtalo de nuevo o contacta a {} para ayuda."
    },
    'new_member_notification': {
        'ar': "عضو جديد انضم إلى القناة {}: معرف المستخدم: {}, الاسم: {}",
        'en': "New member joined the channel {}: User ID: {}, Name: {}",
        'es': "Nuevo miembro se unió al canal {}: ID de usuario: {}, Nombre: {}"
    },
    'account_assigned_notification': {
        'ar': "تم منح حساب {} للمستخدم {} (معرف: {}):\n{}",
        'en': "Account {} assigned to user {} (ID: {}):\n{}",
        'es': "Cuenta {} asignada al usuario {} (ID: {}):\n{}"
    }
}

account_emojis = {
    'Crunchyroll': '📺',
    'Paramount': '🎬',
    'Disney': '🏰',
    'Netflix': '🍿',
    'Steam': '🎮',
    'Xbox': '🎮',
    'Express VPN': '🔒',
    'Nord VPN': '🔒'
}

def t(key, lang='en', *args):
    """Translation function: Returns the appropriate text based on the key and language."""
    text = translations.get(key, {}).get(lang, '')
    if args:
        text = text.format(*args)
    return text

def log_message(user_id, username, message_text, extra_info=None):
    """Log user messages and extra info to a file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] User ID: {user_id}, Username: {username or 'N/A'}, Message: {message_text}"
    if extra_info:
        log_entry += f", Extra: {extra_info}"
    log_entry += "\n"
    try:
        with open(MESSAGES_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error logging message: {e}")

def notify_admin(message, user_id, username, message_text, extra_info=None):
    """Send notification to channel about user interaction."""
    notification = f"User Interaction:\nUser ID: {user_id}\nUsername: {username or 'N/A'}\nMessage: {message_text}"
    if extra_info:
        notification += f"\nExtra: {extra_info}"
    try:
        bot.send_message(NOTIFICATION_CHAT_ID, notification)
    except Exception as e:
        print(f"Error sending notification to channel: {e}")

def notify_new_member(chat_id, user_id, username, first_name):
    """Send notification to channel about new channel member."""
    lang = 'en'  # Default language for notifications
    notification = t('new_member_notification', lang, CHANNEL_USERNAME, user_id, first_name or username or 'N/A')
    try:
        bot.send_message(NOTIFICATION_CHAT_ID, notification)
    except Exception as e:
        print(f"Error sending new member notification: {e}")

def notify_account_assigned(user_id, username, account_type, account):
    """Send notification to channel when an account is assigned."""
    lang = 'en'  # Default language for notifications
    notification = t('account_assigned_notification', lang, account_type, username or 'N/A', user_id, account)
    try:
        bot.send_message(NOTIFICATION_CHAT_ID, notification)
    except Exception as e:
        print(f"Error sending account assigned notification: {e}")

def load_accounts():
    """Load account data from files into accounts_data."""
    for name, filepath in accounts_files.items():
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
                accounts_data[name] = lines
                for acc in lines:
                    account_usage_count.setdefault(acc, 0)
        except FileNotFoundError:
            accounts_data[name] = []

def load_promo_codes():
    """Load promo codes from file."""
    global promo_codes
    try:
        with open(PROMO_CODES_FILE, 'r', encoding='utf-8') as f:
            promo_codes = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        promo_codes = []

def load_referrals():
    """Load referral data from file into user_referrals and points."""
    try:
        with open(REFERRALS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    referrer_id, user_id = line.split(',')
                    user_referrals.setdefault(referrer_id, set()).add(int(user_id))
                    points[referrer_id] = points.get(referrer_id, 0) + 1
    except FileNotFoundError:
        pass  # File will be created when first referral is saved

def load_points():
    """Load points data from file."""
    try:
        with open(POINTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    user_id, point_count = line.split(',')
                    points[user_id] = int(point_count)
    except FileNotFoundError:
        pass  # File will be created when points are saved

def save_referral(referrer_id, user_id):
    """Save a referral to the referrals file."""
    try:
        with open(REFERRALS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{referrer_id},{user_id}\n")
    except Exception as e:
        print(f"Error saving referral: {e}")

def save_points():
    """Save points data to file."""
    try:
        with open(POINTS_FILE, 'w', encoding='utf-8') as f:
            for user_id, point_count in points.items():
                f.write(f"{user_id},{point_count}\n")
    except Exception as e:
        print(f"Error saving points: {e}")

def mark_account_as_used(account_type, account_value):
    """Mark an account as used and update the file."""
    if account_value in accounts_data.get(account_type, []):
        accounts_data[account_type].remove(account_value)
        filepath = accounts_files[account_type]
        with open(filepath, 'w', encoding='utf-8') as f:
            for acc in accounts_data[account_type]:
                f.write(acc + "\n")

def mark_promo_code_as_used(code):
    """Mark a promo code as used and update the file."""
    if code in promo_codes:
        promo_codes.remove(code)
        with open(PROMO_CODES_FILE, 'w', encoding='utf-8') as f:
            for pc in promo_codes:
                f.write(pc + "\n")
    used_promo_codes.add(code)

def get_unused_account(user_id, account_type):
    """Get an unused account for the user."""
    given = user_accounts_given.get(user_id, set())
    for acc in accounts_data.get(account_type, []):
        if acc not in given and account_usage_count.get(acc, 0) < 5:
            return acc
    return None

def get_referral_link(user_id):
    """Generate a referral link for the user."""
    return f"https://t.me/{BOT_USERNAME}?start={user_id}"

def get_available_offers(lang):
    """Get a list of available offers."""
    offers = []
    for acc_type, accounts in accounts_data.items():
        emoji = account_emojis.get(acc_type, '📦')
        if lang == 'ar':
            offers.append(f"{emoji} {acc_type}: {len(accounts)} حسابات متاحة")
        elif lang == 'en':
            offers.append(f"{emoji} {acc_type}: {len(accounts)} accounts available")
        else:  # es
            offers.append(f"{emoji} {acc_type}: {len(accounts)} cuentas disponibles")
    return "\n".join(offers) if offers else t('no_accounts_available', lang)

def show_main_menu(user_id, lang):
    """Show the main menu to the user."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    options = t('main_menu_options', lang)
    markup.row(options[0], options[1], options[2])
    markup.row(options[3], options[4], options[5])
    bot.send_message(user_id, t('back_to_main_menu', lang), reply_markup=markup)

@bot.message_handler(commands=['start'])
def handle_start(message):
    """Handle the /start command."""
    user_id = message.from_user.id
    username = message.from_user.username
    message_text = message.text
    args = message_text.split()

    # Log the /start command
    extra_info = None
    if len(args) > 1:
        referrer_id = args[1]
        extra_info = f"Referral attempt from {referrer_id}"
        if str(referrer_id) != str(user_id):  # Prevent self-referral
            user_referrals.setdefault(str(referrer_id), set())
            if user_id not in user_referrals[str(referrer_id)]:
                user_referrals[str(referrer_id)].add(user_id)
                points[str(referrer_id)] = points.get(str(referrer_id), 0) + 1
                save_referral(referrer_id, user_id)
                save_points()
                extra_info += f" - Point awarded to {referrer_id}"

    log_message(user_id, username, message_text, extra_info)
    notify_admin(message, user_id, username, message_text, extra_info)

    user_languages[user_id] = 'en'  # Default language
    points.setdefault(str(user_id), 0)
    user_accounts_given.setdefault(user_id, set())

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🇲🇦 العربية", "🇬🇧 English", "🇪🇸 Español")
    bot.send_message(user_id, t('choose_language', 'en'), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["🇲🇦 العربية", "🇬🇧 English", "🇪🇸 Español"])
def handle_set_language(message):
    """Handle language selection."""
    user_id = message.from_user.id
    username = message.from_user.username
    log_message(user_id, username, message.text)
    notify_admin(message, user_id, username, message.text)

    lang_map = {"🇲🇦 العربية": "ar", "🇬🇧 English": "en", "🇪🇸 Español": "es"}
    lang = lang_map.get(message.text, 'en')
    user_languages[user_id] = lang

    show_main_menu(user_id, lang)

@bot.chat_member_handler()
def handle_chat_member_update(update):
    """Handle new chat member updates."""
    new_member = update.new_chat_member
    if new_member.status == "member":
        user_id = new_member.user.id
        username = new_member.user.username
        first_name = new_member.user.first_name
        chat_id = update.chat.id
        chat_username = update.chat.username
        if chat_username == CHANNEL_USERNAME:
            notify_new_member(chat_id, user_id, username, first_name)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle all other messages."""
    user_id = message.from_user.id
    username = message.from_user.username
    lang = user_languages.get(user_id, 'en')
    text = message.text

    # Log every message
    log_message(user_id, username, text)
    notify_admin(message, user_id, username, text)

    if text == t('main_menu_options', lang)[0]:  # Join Private Channel
        bot.send_message(user_id, t('join_private_channel', lang))

    elif text == t('main_menu_options', lang)[1]:  # Get Account
        user_points = points.get(str(user_id), 0)
        if user_points < 10:
            referral_link = get_referral_link(user_id)
            bot.send_message(user_id, t('not_enough_points', lang, user_points, referral_link))
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for acc_type in accounts_data.keys():
            emoji = account_emojis.get(acc_type, '📦')
            markup.row(f"{emoji} {acc_type}")
        markup.row(t('previous_menu', lang))
        bot.send_message(user_id, t('choose_account_type', lang), reply_markup=markup)

    elif text == t('main_menu_options', lang)[2]:  # Available Offers
        offers = get_available_offers(lang)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(t('previous_menu', lang))
        bot.send_message(user_id, t('available_offers', lang, offers), reply_markup=markup)

    elif text == t('main_menu_options', lang)[3]:  # Enter Promo Code
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(t('previous_menu', lang))
        bot.send_message(user_id, t('enter_promo_code', lang), reply_markup=markup)

    elif text == t('main_menu_options', lang)[4]:  # My Points
        user_points = points.get(str(user_id), 0)
        referral_link = get_referral_link(user_id)
        bot.send_message(user_id, t('my_points', lang, user_points, referral_link))
        show_main_menu(user_id, lang)

    elif text == t('main_menu_options', lang)[5]:  # Join Public Channel
        bot.send_message(user_id, t('join_public_channel', lang))

    elif text in accounts_data.keys() or text.lstrip('📺🎬🏰🍿🎮🔒📦 ') in accounts_data.keys():
        account_type = text.lstrip('📺🎬🏰🍿🎮🔒📦 ')
        user_points = points.get(str(user_id), 0)
        if user_points < 10 and user_id not in used_promo_codes:
            referral_link = get_referral_link(user_id)
            bot.send_message(user_id, t('not_enough_points', lang, user_points, referral_link))
            return

        account = get_unused_account(user_id, account_type)
        if account is None:
            bot.send_message(user_id, t('no_accounts_available', lang))
            return

        bot.send_message(user_id, t('account_given', lang, account_type, account))
        notify_account_assigned(user_id, username, account_type, account)
        mark_account_as_used(account_type, account)
        user_accounts_given.setdefault(user_id, set()).add(account)
        account_usage_count[account] = account_usage_count.get(account, 0) + 1
        if user_id in used_promo_codes:
            used_promo_codes.remove(user_id)
        else:
            points[str(user_id)] = max(points[str(user_id)] - 10, 0)
            save_points()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(t('previous_menu', lang))
        bot.send_message(user_id, t('back_to_main_menu', lang), reply_markup=markup)

    elif text in [t('go_back', lang), t('previous_menu', lang)]:
        show_main_menu(user_id, lang)

    else:  # Check for promo code
        if text in promo_codes and text not in used_promo_codes:
            mark_promo_code_as_used(text)
            used_promo_codes.add(user_id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for acc_type in accounts_data.keys():
                emoji = account_emojis.get(acc_type, '📦')
                markup.row(f"{emoji} {acc_type}")
            markup.row(t('previous_menu', lang))
            bot.send_message(user_id, t('valid_promo_code', lang), reply_markup=markup)
        else:
            bot.send_message(user_id, t('invalid_promo_code', lang, SUPPORT_USERNAME))
            show_main_menu(user_id, lang)

if __name__ == "__main__":
    # Create .account directory if it doesn't exist
    os.makedirs(".account", exist_ok=True)
    load_accounts()
    load_promo_codes()
    load_referrals()
    load_points()
    print("The bot is running now...")
    bot.polling()