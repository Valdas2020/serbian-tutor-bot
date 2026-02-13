from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from i18n import t


def language_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for choosing interface language."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
            ]
        ]
    )


def script_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Keyboard for choosing writing script."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("btn_cyrillic", lang), callback_data="script:cyrillic"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t("btn_latin", lang), callback_data="script:latin"
                ),
            ],
        ]
    )


def dialect_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Keyboard for choosing Serbian dialect."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("btn_ekavica", lang), callback_data="dialect:ekavica"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t("btn_ijekavica", lang), callback_data="dialect:ijekavica"
                ),
            ],
        ]
    )


def settings_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Keyboard for settings menu."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("btn_change_dialect", lang),
                    callback_data="settings:dialect",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t("btn_change_script", lang),
                    callback_data="settings:script",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t("btn_change_language", lang),
                    callback_data="settings:language",
                ),
            ],
        ]
    )
