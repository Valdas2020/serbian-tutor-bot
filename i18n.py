from __future__ import annotations

TEXTS: dict[str, dict[str, str]] = {
    "welcome": {
        "ru": (
            "Zdravo! Dobrodošli!\n\n"
            "Я — ваш репетитор сербского языка.\n"
            "Отправляйте мне голосовые сообщения на сербском, "
            "и я помогу вам с произношением и грамматикой.\n\n"
            "I'm your Serbian language tutor.\n"
            "Send me voice messages in Serbian, "
            "and I'll help you with pronunciation and grammar.\n\n"
            "Ich bin dein Serbisch-Tutor.\n"
            "Schick mir Sprachnachrichten auf Serbisch, "
            "und ich helfe dir mit Aussprache und Grammatik.\n\n"
            "Выберите язык / Choose language / Sprache wählen:"
        ),
        "en": (
            "Zdravo! Dobrodošli!\n\n"
            "I'm your Serbian language tutor.\n"
            "Send me voice messages in Serbian, "
            "and I'll help you with pronunciation and grammar.\n\n"
            "Я — ваш репетитор сербского языка.\n"
            "Отправляйте мне голосовые сообщения на сербском, "
            "и я помогу вам с произношением и грамматикой.\n\n"
            "Ich bin dein Serbisch-Tutor.\n"
            "Schick mir Sprachnachrichten auf Serbisch, "
            "und ich helfe dir mit Aussprache und Grammatik.\n\n"
            "Choose language / Выберите язык / Sprache wählen:"
        ),
        "de": (
            "Zdravo! Dobrodošli!\n\n"
            "Ich bin dein Serbisch-Tutor.\n"
            "Schick mir Sprachnachrichten auf Serbisch, "
            "und ich helfe dir mit Aussprache und Grammatik.\n\n"
            "I'm your Serbian language tutor.\n"
            "Send me voice messages in Serbian, "
            "and I'll help you with pronunciation and grammar.\n\n"
            "Я — ваш репетитор сербского языка.\n"
            "Отправляйте мне голосовые сообщения на сербском, "
            "и я помогу вам с произношением и грамматикой.\n\n"
            "Sprache wählen / Choose language / Выберите язык:"
        ),
    },
    "choose_language": {
        "ru": "Выберите язык интерфейса:",
        "en": "Choose interface language:",
        "de": "Sprache wählen:",
    },
    "language_set": {
        "ru": "Язык интерфейса установлен: Русский",
        "en": "Interface language set: English",
        "de": "Sprache eingestellt: Deutsch",
    },
    "choose_script": {
        "ru": (
            "Выберите письменность:\n\n"
            "🔤 *Кириллица* — Ћирилица\n"
            "Пример: Добар дан, како сте?\n\n"
            "🔡 *Латиница* — Latinica\n"
            "Пример: Dobar dan, kako ste?"
        ),
        "en": (
            "Choose writing script:\n\n"
            "🔤 *Cyrillic* — Ћирилица\n"
            "Example: Добар дан, како сте?\n\n"
            "🔡 *Latin* — Latinica\n"
            "Example: Dobar dan, kako ste?"
        ),
        "de": (
            "Schrift wählen:\n\n"
            "🔤 *Kyrillisch* — Ћирилица\n"
            "Beispiel: Добар дан, како сте?\n\n"
            "🔡 *Lateinisch* — Latinica\n"
            "Beispiel: Dobar dan, kako ste?"
        ),
    },
    "script_cyrillic": {
        "ru": "Письменность: Кириллица (Ћирилица) 🔤",
        "en": "Script set: Cyrillic (Ћирилица) 🔤",
        "de": "Schrift: Kyrillisch (Ћирилица) 🔤",
    },
    "script_latin": {
        "ru": "Письменность: Латиница (Latinica) 🔡",
        "en": "Script set: Latin (Latinica) 🔡",
        "de": "Schrift: Lateinisch (Latinica) 🔡",
    },
    "choose_dialect": {
        "ru": (
            "Выберите диалект сербского:\n\n"
            "🇷🇸 *Екавица* — стандартный сербский (Белград)\n"
            "Примеры: лепо, девојка, река\n\n"
            "🇲🇪 *Ијекавица* — черногорский/боснийский вариант\n"
            "Примеры: лијепо, дјевојка, ријека"
        ),
        "en": (
            "Choose a Serbian dialect:\n\n"
            "🇷🇸 *Ekavica* — Standard Serbian (Belgrade)\n"
            "Examples: lepo, devojka, reka\n\n"
            "🇲🇪 *Ijekavica* — Montenegrin/Bosnian style\n"
            "Examples: lijepo, djevojka, rijeka"
        ),
        "de": (
            "Serbischen Dialekt wählen:\n\n"
            "🇷🇸 *Ekavica* — Standard-Serbisch (Belgrad)\n"
            "Beispiele: lepo, devojka, reka\n\n"
            "🇲🇪 *Ijekavica* — Montenegrinisch/Bosnisch\n"
            "Beispiele: lijepo, djevojka, rijeka"
        ),
    },
    "dialect_ekavica": {
        "ru": "Диалект: Екавица (стандартный сербский) 🇷🇸",
        "en": "Dialect: Ekavica (Standard Serbian) 🇷🇸",
        "de": "Dialekt: Ekavica (Standard-Serbisch) 🇷🇸",
    },
    "dialect_ijekavica": {
        "ru": "Диалект: Ијекавица (черногорский вариант) 🇲🇪",
        "en": "Dialect: Ijekavica (Montenegrin style) 🇲🇪",
        "de": "Dialekt: Ijekavica (Montenegrinisch) 🇲🇪",
    },
    "choose_style": {
        "ru": (
            "Последний шаг! Как мне с вами общаться?\n\n"
            "📚 *Книжно* — грамотная, литературная речь\n"
            "🛒 *Повседневный* — обычный язык для магазина, кафе, водопроводчика\n"
            "🍺 *Как в кафане* — живой разговорный язык, сленг\n"
            "🐣 *Просто, как с новичком* — короткие фразы, базовая лексика"
        ),
        "en": (
            "Last step! How should I talk to you?\n\n"
            "📚 *Formal* — proper literary speech\n"
            "🛒 *Everyday* — natural language for the shop, café, plumber\n"
            "🍺 *Like in a kafana* — casual, slang, street talk\n"
            "🐣 *Simple, like a beginner* — short phrases, basic vocabulary"
        ),
        "de": (
            "Letzter Schritt! Wie soll ich mit dir sprechen?\n\n"
            "📚 *Formell* — korrektes, literarisches Serbisch\n"
            "🛒 *Alltäglich* — natürliche Sprache für Laden, Café, Handwerker\n"
            "🍺 *Kafana-Stil* — umgangssprachlich, Slang\n"
            "🐣 *Einfach für Anfänger* — kurze Sätze, Basisvokabular"
        ),
    },
    "style_formal": {
        "ru": "Стиль: Книжная речь 📚\n\nВсё настроено! Отправьте голосовое или текст на сербском.",
        "en": "Style: Formal speech 📚\n\nAll set! Send a voice message or text in Serbian.",
        "de": "Stil: Formell 📚\n\nAlles eingestellt! Schick eine Sprachnachricht oder Text auf Serbisch.",
    },
    "style_everyday": {
        "ru": "Стиль: Повседневный 🛒\n\nВсё настроено! Отправьте голосовое или текст на сербском.",
        "en": "Style: Everyday 🛒\n\nAll set! Send a voice message or text in Serbian.",
        "de": "Stil: Alltäglich 🛒\n\nAlles eingestellt! Schick eine Sprachnachricht oder Text auf Serbisch.",
    },
    "style_casual": {
        "ru": "Стиль: Как в кафане 🍺\n\nВсё настроено! Отправьте голосовое или текст на сербском.",
        "en": "Style: Kafana talk 🍺\n\nAll set! Send a voice message or text in Serbian.",
        "de": "Stil: Kafana-Stil 🍺\n\nAlles eingestellt! Schick eine Sprachnachricht oder Text auf Serbisch.",
    },
    "style_beginner": {
        "ru": "Стиль: Просто, как с новичком 🐣\n\nВсё настроено! Отправьте голосовое или текст на сербском.",
        "en": "Style: Simple beginner mode 🐣\n\nAll set! Send a voice message or text in Serbian.",
        "de": "Stil: Einfach für Anfänger 🐣\n\nAlles eingestellt! Schick eine Sprachnachricht oder Text auf Serbisch.",
    },
    "processing": {
        "ru": "⏳ Обрабатываю ваше сообщение...",
        "en": "⏳ Processing your message...",
        "de": "⏳ Deine Nachricht wird verarbeitet...",
    },
    "transcription": {
        "ru": "🎤 *Распознанный текст:*\n_{text}_",
        "en": "🎤 *Transcribed text:*\n_{text}_",
        "de": "🎤 *Transkription:*\n_{text}_",
    },
    "error_general": {
        "ru": "Произошла ошибка. Попробуйте ещё раз.",
        "en": "An error occurred. Please try again.",
        "de": "Ein Fehler ist aufgetreten. Bitte versuche es erneut.",
    },
    "error_no_voice": {
        "ru": "Пожалуйста, отправьте голосовое сообщение.",
        "en": "Please send a voice message.",
        "de": "Bitte sende eine Sprachnachricht.",
    },
    "error_transcription": {
        "ru": "Не удалось распознать речь. Попробуйте записать сообщение ещё раз.",
        "en": "Could not transcribe speech. Please try recording again.",
        "de": "Sprache konnte nicht erkannt werden. Bitte versuche es erneut.",
    },
    "error_not_configured": {
        "ru": "Сначала пройдите настройку: /start",
        "en": "Please complete setup first: /start",
        "de": "Bitte zuerst die Einrichtung abschließen: /start",
    },
    "settings": {
        "ru": "⚙️ *Настройки*\n\nДиалект: {dialect}\nПисьменность: {script}\nСтиль: {style}\nЯзык интерфейса: {lang}\n\nЧто хотите изменить?",
        "en": "⚙️ *Settings*\n\nDialect: {dialect}\nScript: {script}\nStyle: {style}\nInterface language: {lang}\n\nWhat would you like to change?",
        "de": "⚙️ *Einstellungen*\n\nDialekt: {dialect}\nSchrift: {script}\nStil: {style}\nSprache: {lang}\n\nWas möchtest du ändern?",
    },
    "help": {
        "ru": (
            "🎓 *Как пользоваться ботом:*\n\n"
            "1. Отправьте голосовое сообщение на сербском языке\n"
            "2. Бот распознает вашу речь\n"
            "3. Репетитор ответит на сербском и укажет ошибки\n"
            "4. Вы получите озвученный ответ\n\n"
            "*Команды:*\n"
            "/start — начать сначала\n"
            "/settings — настройки диалекта и языка\n"
            "/help — эта справка"
        ),
        "en": (
            "🎓 *How to use the bot:*\n\n"
            "1. Send a voice message in Serbian\n"
            "2. The bot will transcribe your speech\n"
            "3. The tutor will respond in Serbian and point out mistakes\n"
            "4. You'll receive a voiced response\n\n"
            "*Commands:*\n"
            "/start — start over\n"
            "/settings — dialect and language settings\n"
            "/help — this help message"
        ),
        "de": (
            "🎓 *So benutzt du den Bot:*\n\n"
            "1. Schick eine Sprachnachricht auf Serbisch\n"
            "2. Der Bot transkribiert deine Sprache\n"
            "3. Der Tutor antwortet auf Serbisch und zeigt Fehler\n"
            "4. Du erhältst eine Sprachantwort\n\n"
            "*Befehle:*\n"
            "/start — von vorne beginnen\n"
            "/settings — Dialekt und Spracheinstellungen\n"
            "/help — diese Hilfe"
        ),
    },
    "btn_russian": {
        "ru": "🇷🇺 Русский",
        "en": "🇷🇺 Русский",
        "de": "🇷🇺 Русский",
    },
    "btn_english": {
        "ru": "🇬🇧 English",
        "en": "🇬🇧 English",
        "de": "🇬🇧 English",
    },
    "btn_german": {
        "ru": "🇩🇪 Deutsch",
        "en": "🇩🇪 Deutsch",
        "de": "🇩🇪 Deutsch",
    },
    "btn_ekavica": {
        "ru": "🇷🇸 Екавица",
        "en": "🇷🇸 Ekavica",
        "de": "🇷🇸 Ekavica",
    },
    "btn_ijekavica": {
        "ru": "🇲🇪 Ијекавица",
        "en": "🇲🇪 Ijekavica",
        "de": "🇲🇪 Ijekavica",
    },
    "btn_cyrillic": {
        "ru": "🔤 Кириллица",
        "en": "🔤 Cyrillic",
        "de": "🔤 Kyrillisch",
    },
    "btn_latin": {
        "ru": "🔡 Латиница",
        "en": "🔡 Latin",
        "de": "🔡 Lateinisch",
    },
    "btn_formal": {
        "ru": "📚 Книжно",
        "en": "📚 Formal",
        "de": "📚 Formell",
    },
    "btn_everyday": {
        "ru": "🛒 Повседневный",
        "en": "🛒 Everyday",
        "de": "🛒 Alltäglich",
    },
    "btn_casual": {
        "ru": "🍺 Как в кафане",
        "en": "🍺 Kafana style",
        "de": "🍺 Kafana-Stil",
    },
    "btn_beginner": {
        "ru": "🐣 Просто, как с новичком",
        "en": "🐣 Simple / Beginner",
        "de": "🐣 Einfach / Anfänger",
    },
    "btn_change_dialect": {
        "ru": "Изменить диалект",
        "en": "Change dialect",
        "de": "Dialekt ändern",
    },
    "btn_change_script": {
        "ru": "Изменить письменность",
        "en": "Change script",
        "de": "Schrift ändern",
    },
    "btn_change_style": {
        "ru": "Изменить стиль общения",
        "en": "Change communication style",
        "de": "Kommunikationsstil ändern",
    },
    "btn_change_language": {
        "ru": "Изменить язык",
        "en": "Change language",
        "de": "Sprache ändern",
    },
    "support": {
        "ru": (
            "🆘 <b>Поддержка</b>\n\n"
            "Если у вас возникли проблемы или вы хотите сообщить об ошибке, "
            "напишите нам напрямую:\n\n"
            '👉 <a href="tg://user?id=485544391">Написать в поддержку</a>'
        ),
        "en": (
            "🆘 <b>Support</b>\n\n"
            "If you have any issues or want to report a bug, "
            "reach out to us directly:\n\n"
            '👉 <a href="tg://user?id=485544391">Contact support</a>'
        ),
        "de": (
            "🆘 <b>Support</b>\n\n"
            "Bei Problemen oder Fehlermeldungen, schreib uns direkt:\n\n"
            '👉 <a href="tg://user?id=485544391">Support kontaktieren</a>'
        ),
    },
    "send_voice_hint": {
        "ru": "Отправьте мне голосовое сообщение на сербском, и я помогу вам! Также можно отправить текст.",
        "en": "Send me a voice message in Serbian and I'll help you! You can also send text.",
        "de": "Schick mir eine Sprachnachricht auf Serbisch und ich helfe dir! Du kannst auch Text schicken.",
    },
}


def t(key: str, lang: str = "ru", **kwargs: str) -> str:
    """Get translated text by key and language."""
    text_dict = TEXTS.get(key, {})
    text = text_dict.get(lang, text_dict.get("en", text_dict.get("ru", f"[{key}]")))
    if kwargs:
        text = text.format(**kwargs)
    return text
