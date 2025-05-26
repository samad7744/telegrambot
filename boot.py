from telebot import TeleBot, types
from datetime import datetime
import os

# إعدادات البوت
TOKEN = '7537525596:AAHo5peL-JiabVhJpE7YUtQmMWLlc-6rKbg'  # تأكد من أن هذا التوكن صحيح
bot = TeleBot(TOKEN)
SUPPORT_USERNAME = "@jiinwoo777"
BOT_USERNAME = "@Cuentas_gratiss_bot"
PROMO_CODES_FILE = ".account/promo_codes.txt"
MESSAGES_LOG_FILE = ".account/messages_log.txt"
REFERRALS_FILE = ".account/referrals.txt"
POINTS_FILE = ".account/points.txt"
CHANNEL_USERNAME = "@membersb7757gbfbgsvdssdv"
NOTIFICATION_CHAT_ID = "@membersb7757gbfbgsvdssdv"

# المتغيرات العامة
points = {}
user_languages = {}
user_accounts_given = {}
user_referrals = {}
account_usage_count = {}
used_promo_codes = set()
accounts_data = {}
promo_codes = []

# ملفات الحسابات
accounts_files = {
    'Crunchyroll': '.account/crunchyroll.txt',
    'Paramount': '.account/paramount.txt',
    'Disney': '.account/disney.txt',
    'Netflix': '.account/netflix.txt',
    'Steam': '.account/steam.txt',
    'Xbox': '.account/xbox.txt',
    'VPN': '.account/vpn.txt',
}

# الرموز التعبيرية لكل نوع حساب
account_emojis = {
    'Crunchyroll': '📺',
    'Paramount': '🎬',
    'Disney': '🏰',
    'Netflix': '🍿',
    'Steam': '🎮',
    'Xbox': '🎮',
    'VPN': '🔒'
}

# الترجمات
translations = {
    'choose_language': {
        'ar': "اختر لغتك:",
        'en': "Choose your language:",
        'es': "Elige tu idioma:"
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
        'ar': (
            "🛒 طلبك تم بنجاح!\n\n"
            "📧 تفاصيل الحساب:\n"
            "📺 الخدمة: {}\n"
            "💌 البريد: {}\n"
            "🔑 كلمة المرور: {}\n"
            "🌍 البلد: {}\n"
            "📱 الجوال: {}\n\n"
            "🎊 شكرًا لاستخدامك البوت!\n"
            "⚠️ إذا واجهت أي مشكلة، راسل المشرف: {}"
        ),
        'en': (
            "🛒 Order Successfully Completed!\n\n"
            "📧 Account Details:\n"
            "📺 Service: {}\n"
            "💌 Email: {}\n"
            "🔑 Password: {}\n"
            "🌍 Country: {}\n"
            "📱 Mobile: {}\n\n"
            "🎊 Thanks for using our bot!\n"
            "⚠️ If you face any issues, contact the admin: {}"
        ),
        'es': (
            "🛒 ¡Orden completada con éxito!\n\n"
            "📧 Detalles de la cuenta:\n"
            "📺 Servicio: {}\n"
            "💌 Correo: {}\n"
            "🔑 Contraseña: {}\n"
            "🌍 País: {}\n"
            "📱 Teléfono: {}\n\n"
            "🎊 ¡Gracias por usar nuestro bot!\n"
            "⚠️ Si tienes algún problema, contacta al administrador: {}"
        )
    },
    'go_back': {
        'ar': "👍 تأكيد",
        'en': "👍 Confirm",
        'es': "👍 Confirmar"
    },
    'previous_menu': {
        'ar': "⬅️ العودة إلى القائمة السابقة",
        'en': "⬅️ Back",
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
        'ar': "🎉 الكود الترويجي صالح! اختر نوع الحساب الذي تريد:",
        'en': "🎉 Valid promo code! Choose the account type you want:",
        'es': "🎉 ¡Código promocional válido! Elige el tipo de cuenta que deseas:"
    },
    'invalid_promo_code': {
        'ar': "الكود الترويجي غير صالح أو تم استخدامه. حاول مرة أخرى أو تواصل مع {} للمساعدة.",
        'en': "Invalid or already used promo code. Try again or contact {} for help.",
        'es': "Código promocional inválido o ya usado. Inténtalo de nuevo o contacta a {} para ayuda."
    },
    'account_assigned_notification': {
        'ar': (
            "🎉 تم منح حساب {} للمستخدم {} (معرف: {}):\n"
            "📺 الخدمة: {}\n"
            "💌 البريد: {}\n"
            "🔑 كلمة المرور: {}\n"
            "🌍 البلد: {}\n"
            "📱 الجوال: {}"
        ),
        'en': (
            "🎉 Account {} assigned to user {} (ID: {}):\n"
            "📺 Service: {}\n"
            "💌 Email: {}\n"
            "🔑 Password: {}\n"
            "🌍 Country: {}\n"
            "📱 Mobile: {}"
        ),
        'es': (
            "🎉 Cuenta {} asignada al usuario {} (ID: {}):\n"
            "📺 Servicio: {}\n"
            "💌 Correo: {}\n"
            "🔑 Contraseña: {}\n"
            "🌍 País: {}\n"
            "📱 Teléfono: {}"
        )
    }
}

def t(key, lang='ar', *args):
    """ترجمة النصوص بناءً على اللغة."""
    text = translations.get(key, {}).get(lang, translations[key]['ar'])
    return text.format(*args) if args else text

def log_message(user_id, username, message_text, extra_info=None):
    """تسجيل رسائل المستخدم في ملف."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] User ID: {user_id}, Username: {username or 'N/A'}, Message: {message_text}"
    if extra_info:
        log_entry += f", Extra: {extra_info}"
    log_entry += "\n"
    try:
        with open(MESSAGES_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"خطأ في تسجيل الرسالة: {e}")

def notify_admin(message, user_id, username, message_text, extra_info=None):
    """إرسال إشعار إلى القناة عن تفاعل المستخدم."""
    notification = f"User Interaction:\nUser ID: {user_id}\nUsername: {username or 'N/A'}\nMessage: {message_text}"
    if extra_info:
        notification += f"\nExtra: {extra_info}"
    try:
        bot.send_message(NOTIFICATION_CHAT_ID, notification)
    except Exception as e:
        print(f"خطأ في إرسال إشعار إلى القناة: {e}")

def notify_account_assigned(user_id, username, account_type, service, login, password, country, mobile):
    """إرسال إشعار إلى القناة عند منح حساب."""
    lang = 'ar'  # اللغة الافتراضية للإشعارات
    notification = t('account_assigned_notification', lang, account_type, username or 'N/A', user_id, service, login, password, country, mobile)
    try:
        bot.send_message(NOTIFICATION_CHAT_ID, notification)
    except Exception as e:
        print(f"خطأ في إرسال إشعار منح الحساب: {e}")

def load_accounts():
    """تحميل الحسابات من الملفات."""
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
    """تحميل الأكواد الترويجية."""
    global promo_codes
    try:
        with open(PROMO_CODES_FILE, 'r', encoding='utf-8') as f:
            promo_codes = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        pass

def load_referrals():
    """تحميل بيانات الإحالات."""
    try:
        with open(REFERRALS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    referrer_id, user_id = line.split(',')
                    user_referrals.setdefault(referrer_id, set()).add(int(user_id))
                    points[referrer_id] = points.get(referrer_id, 0) + 1
    except FileNotFoundError:
        pass

def load_points():
    """تحميل النقاط."""
    try:
        with open(POINTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    user_id, point_count = line.split(',')
                    points[user_id] = int(point_count)
    except FileNotFoundError:
        pass

def save_referral(referrer_id, user_id):
    """حفظ إحالة جديدة."""
    try:
        with open(REFERRALS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{referrer_id},{user_id}\n")
        if user_id not in user_referrals.get(str(referrer_id), set()):
            user_referrals.setdefault(str(referrer_id), set()).add(user_id)
            points[str(referrer_id)] = points.get(str(referrer_id), 0) + 1
            save_points()
    except Exception as e:
        print(f"خطأ في حفظ الإحالة: {e}")

def save_points():
    """حفظ النقاط."""
    try:
        with open(POINTS_FILE, 'w', encoding='utf-8') as f:
            for user_id, point_count in points.items():
                f.write(f"{user_id},{point_count}\n")
    except Exception as e:
        print(f"خطأ في حفظ النقاط: {e}")

def mark_account_as_used(account_type, account_value):
    """تسجيل الحساب كمستخدم."""
    if account_value in accounts_data.get(account_type, []):
        accounts_data[account_type].remove(account_value)
        filepath = accounts_files[account_type]
        with open(filepath, 'w', encoding='utf-8') as f:
            for acc in accounts_data[account_type]:
                f.write(acc + "\n")

def mark_promo_code_as_used(code):
    """تسجيل الكود الترويجي كمستخدم."""
    if code in promo_codes:
        promo_codes.remove(code)
        with open(PROMO_CODES_FILE, 'w', encoding='utf-8') as f:
            for pc in promo_codes:
                f.write(pc + "\n")
    used_promo_codes.add(code)

def get_unused_account(user_id, account_type):
    """الحصول على حساب غير مستخدم."""
    given = user_accounts_given.get(user_id, set())
    for acc in accounts_data.get(account_type, []):
        if acc not in given and account_usage_count.get(acc, 0) < 5:
            return acc
    return None

def get_referral_link(user_id):
    """إنشاء رابط إحالة."""
    return f"https://t.me/{BOT_USERNAME}?start={user_id}"

def get_available_offers(lang):
    """الحصول على العروض المتاحة."""
    offers = []
    for acc_type, accounts in accounts_data.items():
        emoji = account_emojis.get(acc_type, '📦')
        offers.append(f"{emoji} {acc_type}: {len(accounts)} حسابات متاحة")
    return "\n".join(offers) if offers else t('no_accounts_available', lang)

def show_main_menu(user_id, lang):
    """عرض القائمة الرئيسية."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    options = t('main_menu_options', lang)
    markup.row(options[0], options[1], options[2])
    markup.row(options[3], options[4], options[5])
    bot.send_message(user_id, t('back_to_main_menu', lang), reply_markup=markup)

@bot.message_handler(commands=['start'])
def handle_start(message):
    """معالجة أمر /start."""
    user_id = message.from_user.id
    username = message.from_user.username
    message_text = message.text
    args = message_text.split()

    extra_info = None
    if len(args) > 1:
        referrer_id = args[1]
        if str(referrer_id) != str(user_id):
            extra_info = f"إحالة من {referrer_id}"
            save_referral(referrer_id, user_id)
            extra_info += f" - تم منح نقطة لـ {referrer_id}"

    log_message(user_id, username, message_text, extra_info)
    if extra_info:
        notify_admin(message, user_id, username, message_text, extra_info)

    user_languages[user_id] = 'ar'
    points.setdefault(str(user_id), 0)
    user_accounts_given.setdefault(user_id, set())

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🇲🇲 العربية", "🇬🇧 English", "🇪🇸 Español")
    bot.send_message(user_id, t('choose_language', 'ar'), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["🇲🇲 العربية", "🇬🇧 English", "🇪🇸 Español"])
def handle_language_selection(message):
    """معالجة اختيار اللغة."""
    user_id = message.from_user.id
    username = message.from_user.username
    log_message(user_id, username, message.text)
    notify_admin(message, user_id, username, message.text)

    lang_map = {"🇲🇲 العربية": "ar", "🇬🇧 English": "en", "🇪🇸 Español": "es"}
    lang = lang_map.get(message.text, 'ar')
    user_languages[user_id] = lang

    show_main_menu(user_id, lang)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """معالجة جميع الرسائل."""
    user_id = message.from_user.id
    username = message.from_user.username
    lang = user_languages.get(user_id, 'ar')
    text = message.text

    log_message(user_id, username, text)
    notify_admin(message, user_id, username, text)

    if text == t('main_menu_options', lang)[0]:  # الدخول إلى القناة الخاصة
        bot.send_message(user_id, t('join_private_channel', lang))

    elif text == t('main_menu_options', lang)[1]:  # الحصول على حساب
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for acc_type in accounts_data.keys():
            emoji = account_emojis.get(acc_type, '📦')
            markup.row(f"{emoji} {acc_type}")
        markup.row(t('previous_menu', lang))
        bot.send_message(user_id, t('choose_account_type', lang), reply_markup=markup)

    elif text == t('main_menu_options', lang)[2]:  # العروض المتاحة
        offers = get_available_offers(lang)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(t('previous_menu', lang))
        bot.send_message(user_id, t('available_offers', lang, offers), reply_markup=markup)

    elif text == t('main_menu_options', lang)[3]:  # إدخال كود ترويجي
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(t('previous_menu', lang))
        bot.send_message(user_id, t('enter_promo_code', lang), reply_markup=markup)

    elif text == t('main_menu_options', lang)[4]:  # نقاطي
        user_points = points.get(str(user_id), 0)
        referral_link = get_referral_link(user_id)
        bot.send_message(user_id, t('my_points', lang, user_points, referral_link))
        show_main_menu(user_id, lang)

    elif text == t('main_menu_options', lang)[5]:  # الدخول إلى القناة العامة
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

        try:
            parts = account.split(' | ')
            service = parts[0].replace('Service: ', '') if len(parts) > 0 else 'Unknown'
            login = parts[1].replace('Login: ', '') if len(parts) > 1 else 'Unknown'
            password = parts[2].replace('Pass: ', '') if len(parts) > 2 else 'Unknown'
            country = parts[3].replace('Country: ', '') if len(parts) > 3 else 'Unknown'
            mobile = parts[4].replace('Mobile: ', '') if len(parts) > 4 else 'Unknown'

            markup = types.InlineKeyboardMarkup()
            if user_points >= 10 and user_id not in used_promo_codes:
                confirm_button = types.InlineKeyboardButton(
                    text=t('go_back', lang),
                    callback_data=f"confirm_account_{user_id}_{account_type}"
                )
                markup.add(confirm_button)

            formatted_message = t(
                'account_given',
                lang,
                service,
                login,
                password,
                country,
                mobile,
                SUPPORT_USERNAME
            )

            bot.send_message(user_id, formatted_message, reply_markup=markup)
            notify_account_assigned(
                user_id,
                username,
                account_type,
                service,
                login,
                password,
                country,
                mobile
            )

            if user_points < 10 or user_id in used_promo_codes:
                mark_account_as_used(account_type, account)
                user_accounts_given.setdefault(user_id, set()).add(account)
                account_usage_count[account] = account_usage_count.get(account, 0) + 1
                if user_id in used_promo_codes:
                    used_promo_codes.remove(user_id)
                else:
                    points[str(user_id)] = max(points[str(user_id)] - 10, 0)
                    save_points()

        except Exception as e:
            bot.send_message(user_id, f"خطأ في معالجة الحساب: {e}")
            show_main_menu(user_id, lang)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(t('previous_menu', lang))
        bot.send_message(user_id, t('back_to_main_menu', lang), reply_markup=markup)

    elif text == t('previous_menu', lang):
        show_main_menu(user_id, lang)

    else:  # التحقق من الكود الترويجي
        if text in promo_codes and user_id not in used_promo_codes:
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

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """معالجة أزرار التأكيد."""
    user_id = call.from_user.id
    lang = user_languages.get(user_id, 'ar')
    if call.data.startswith("confirm_account_"):
        _, _, account_type = call.data.split('_')
        account = get_unused_account(user_id, account_type)
        if account:
            mark_account_as_used(account_type, account)
            user_accounts_given.setdefault(user_id, set()).add(account)
            account_usage_count[account] = account_usage_count.get(account, 0) + 1
            points[str(user_id)] = max(points[str(user_id)] - 10, 0)
            save_points()
            bot.answer_callback_query(call.id, "تم تأكيد الحساب!")
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None
            )
        else:
            bot.answer_callback_query(call.id, "الحساب غير متوفر الآن!")

if __name__ == "__main__":
    os.makedirs(".account", exist_ok=True)
    load_accounts()
    load_promo_codes()
    load_referrals()
    load_points()
    print("البوت يعمل الآن...")
    try:
        bot.polling()
    except Exception as e:
        print(f"خطأ في تشغيل البوت: {e}")
