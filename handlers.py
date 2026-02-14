from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

from aiogram import Router, Bot, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.filters.command import CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile

from config import ADMIN_ID, PROMO_CODES
from database import (
    get_or_create_user, reset_user_settings, update_user_dialect,
    update_user_language, update_user_script, update_user_style,
    log_voice_message, activate_promo, get_admin_stats,
)
from i18n import t
from keyboards import (
    language_keyboard, script_keyboard, dialect_keyboard,
    style_keyboard, settings_keyboard,
)
from services import transcribe_voice, get_tutor_response, synthesize_speech

logger = logging.getLogger(__name__)
router = Router()


def _user_configured(user) -> bool:
    """Check if user completed all onboarding steps."""
    return bool(user.dialect and user.script and user.style)


# --- Commands ---


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject) -> None:
    """Handle /start — welcome and language selection (resets settings).
    Supports deep links: /start CHURCH -> ref_source='CHURCH'
    """
    ref_source = command.args or None
    await reset_user_settings(message.from_user.id, ref_source=ref_source)
    await message.answer(
        t("welcome", "ru"),
        reply_markup=language_keyboard(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Handle /help — show help text."""
    user = await get_or_create_user(message.from_user.id)
    await message.answer(
        t("help", user.ui_language),
        parse_mode="Markdown",
    )


@router.message(Command("settings"))
async def cmd_settings(message: Message) -> None:
    """Handle /settings — show current settings."""
    user = await get_or_create_user(message.from_user.id)
    lang = user.ui_language

    dialect_display = "Екавица 🇷🇸" if user.dialect == "ekavica" else "Ијекавица 🇲🇪" if user.dialect else "—"
    script_display = "Кириллица 🔤" if user.script == "cyrillic" else "Латиница 🔡" if user.script else "—"
    style_map = {"formal": "📚 Книжно", "casual": "🍺 Как в кафане", "beginner": "🐣 Просто"}
    style_display = style_map.get(user.style, "—")
    lang_display = "Русский 🇷🇺" if lang == "ru" else "English 🇬🇧"

    await message.answer(
        t("settings", lang, dialect=dialect_display, script=script_display, style=style_display, lang=lang_display),
        parse_mode="Markdown",
        reply_markup=settings_keyboard(lang),
    )


@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: Message) -> None:
    """Handle /admin_stats — show bot statistics (admin only)."""
    if message.from_user.id != ADMIN_ID:
        return

    stats = await get_admin_stats()

    ref_lines = []
    for source, count in stats["ref_stats"]:
        ref_lines.append(f"  {source} — {count}")
    ref_text = "\n".join(ref_lines) if ref_lines else "  (нет данных)"

    text = (
        f"📊 *Статистика бота*\n\n"
        f"👥 Всего юзеров: {stats['total']}\n"
        f"📈 Новых за 24ч: {stats['new_24h']}\n"
        f"📅 Новых за 7 дней: {stats['new_7d']}\n"
        f"⭐ Pro-юзеров: {stats['pro_count']}\n\n"
        f"📣 *Топ источников:*\n{ref_text}\n\n"
        f"🎤 Голосовых сегодня: {stats['voices_today']}"
    )

    await message.answer(text, parse_mode="Markdown")


# --- Callbacks: Language ---


@router.callback_query(F.data.startswith("lang:"))
async def cb_language(callback: CallbackQuery) -> None:
    """Handle language selection. Onboarding → script. Settings → confirm."""
    lang = callback.data.split(":")[1]
    user = await update_user_language(callback.from_user.id, lang)

    await callback.message.edit_text(t("language_set", lang))

    if _user_configured(user):
        await callback.message.answer(t("send_voice_hint", lang))
    else:
        await callback.message.answer(
            t("choose_script", lang),
            parse_mode="Markdown",
            reply_markup=script_keyboard(lang),
        )
    await callback.answer()


# --- Callbacks: Script ---


@router.callback_query(F.data.startswith("script:"))
async def cb_script(callback: CallbackQuery) -> None:
    """Handle script selection. Onboarding → dialect. Settings → confirm."""
    script = callback.data.split(":")[1]
    user = await update_user_script(callback.from_user.id, script)
    lang = user.ui_language

    key = f"script_{script}"
    await callback.message.edit_text(t(key, lang))

    if _user_configured(user):
        await callback.message.answer(t("send_voice_hint", lang))
    else:
        await callback.message.answer(
            t("choose_dialect", lang),
            parse_mode="Markdown",
            reply_markup=dialect_keyboard(lang),
        )
    await callback.answer()


# --- Callbacks: Dialect ---


@router.callback_query(F.data.startswith("dialect:"))
async def cb_dialect(callback: CallbackQuery) -> None:
    """Handle dialect selection. Onboarding → style. Settings → confirm."""
    dialect = callback.data.split(":")[1]
    user = await update_user_dialect(callback.from_user.id, dialect)
    lang = user.ui_language

    key = f"dialect_{dialect}"
    await callback.message.edit_text(t(key, lang))

    if _user_configured(user):
        await callback.message.answer(t("send_voice_hint", lang))
    else:
        await callback.message.answer(
            t("choose_style", lang),
            parse_mode="Markdown",
            reply_markup=style_keyboard(lang),
        )
    await callback.answer()


# --- Callbacks: Style ---


@router.callback_query(F.data.startswith("style:"))
async def cb_style(callback: CallbackQuery) -> None:
    """Handle style selection."""
    style = callback.data.split(":")[1]
    user = await update_user_style(callback.from_user.id, style)
    lang = user.ui_language

    key = f"style_{style}"
    await callback.message.edit_text(t(key, lang))

    # After settings change, show hint if fully configured
    if _user_configured(user):
        await callback.message.answer(t("send_voice_hint", lang))
    await callback.answer()


# --- Callbacks: Settings ---


@router.callback_query(F.data == "settings:dialect")
async def cb_settings_dialect(callback: CallbackQuery) -> None:
    user = await get_or_create_user(callback.from_user.id)
    await callback.message.edit_text(
        t("choose_dialect", user.ui_language),
        parse_mode="Markdown",
        reply_markup=dialect_keyboard(user.ui_language),
    )
    await callback.answer()


@router.callback_query(F.data == "settings:script")
async def cb_settings_script(callback: CallbackQuery) -> None:
    user = await get_or_create_user(callback.from_user.id)
    await callback.message.edit_text(
        t("choose_script", user.ui_language),
        parse_mode="Markdown",
        reply_markup=script_keyboard(user.ui_language),
    )
    await callback.answer()


@router.callback_query(F.data == "settings:style")
async def cb_settings_style(callback: CallbackQuery) -> None:
    user = await get_or_create_user(callback.from_user.id)
    await callback.message.edit_text(
        t("choose_style", user.ui_language),
        parse_mode="Markdown",
        reply_markup=style_keyboard(user.ui_language),
    )
    await callback.answer()


@router.callback_query(F.data == "settings:language")
async def cb_settings_language(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        t("choose_language", "ru"),
        reply_markup=language_keyboard(),
    )
    await callback.answer()


# --- Voice Messages ---


@router.message(F.voice)
async def handle_voice(message: Message, bot: Bot) -> None:
    """Handle voice messages: transcribe -> tutor -> TTS."""
    user = await get_or_create_user(message.from_user.id)
    lang = user.ui_language

    if not _user_configured(user):
        await message.answer(t("error_not_configured", lang))
        return

    processing_msg = await message.answer(t("processing", lang))

    voice_file = None
    tts_file = None

    try:
        file = await bot.get_file(message.voice.file_id)
        voice_file = Path(tempfile.mktemp(suffix=".ogg"))
        await bot.download_file(file.file_path, voice_file)

        transcription = await transcribe_voice(voice_file)

        if not transcription:
            await processing_msg.edit_text(t("error_transcription", lang))
            return

        safe_transcription = transcription.replace("_", "\\_").replace("*", "\\*")
        await processing_msg.edit_text(
            t("transcription", lang, text=safe_transcription),
            parse_mode="Markdown",
        )

        tutor_reply = await get_tutor_response(
            transcription, user.dialect, user.script, user.ui_language, user.style,
        )

        await message.answer(tutor_reply)

        # Log voice interaction
        await log_voice_message(message.from_user.id)

        try:
            tts_file = await synthesize_speech(tutor_reply)
            audio_input = FSInputFile(tts_file, filename="srpski_tutor.mp3")
            await message.answer_document(audio_input)
        except Exception:
            logger.exception("Error synthesizing/sending audio")

    except Exception:
        logger.exception("Error processing voice message")
        await message.answer(t("error_general", lang))
    finally:
        if voice_file and voice_file.exists():
            os.unlink(voice_file)
        if tts_file and tts_file.exists():
            os.unlink(tts_file)


# --- Text Messages ---


@router.message(F.text)
async def handle_text(message: Message) -> None:
    """Handle plain text messages — treat as Serbian text input or promo code."""
    user = await get_or_create_user(message.from_user.id)
    lang = user.ui_language

    # Check for promo code
    code = message.text.strip().upper()
    if code in PROMO_CODES:
        days = PROMO_CODES[code]
        await activate_promo(message.from_user.id, days)
        promo_msg = (
            f"🎉 Pro-доступ активирован на {days} дней!"
            if lang == "ru"
            else f"🎉 Pro access activated for {days} days!"
        )
        await message.answer(promo_msg)
        return

    if not _user_configured(user):
        await message.answer(t("error_not_configured", lang))
        return

    processing_msg = await message.answer(t("processing", lang))

    tts_file = None

    try:
        tutor_reply = await get_tutor_response(
            message.text, user.dialect, user.script, user.ui_language, user.style,
        )

        await processing_msg.edit_text(tutor_reply)

        try:
            tts_file = await synthesize_speech(tutor_reply)
            audio_input = FSInputFile(tts_file, filename="srpski_tutor.mp3")
            await message.answer_document(audio_input)
        except Exception:
            logger.exception("Error synthesizing/sending audio")

    except Exception:
        logger.exception("Error processing text message")
        await message.answer(t("error_general", lang))
    finally:
        if tts_file and tts_file.exists():
            os.unlink(tts_file)
