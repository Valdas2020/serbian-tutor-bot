from __future__ import annotations

import logging
import tempfile
from pathlib import Path

from openai import AsyncOpenAI

from config import (
    LLM_API_KEY, LLM_BASE_URL, OPENAI_API_KEY,
    WHISPER_MODEL, CHAT_MODEL, TTS_MODEL, TTS_VOICE,
)

logger = logging.getLogger(__name__)

# RouteLLM/Abacus — for chat completions
llm_client = AsyncOpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

# OpenAI direct — for Whisper (STT) and TTS
audio_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT_TEMPLATE = """You are a patient and encouraging Serbian language tutor.

The student is learning Serbian and has chosen the **{dialect_name}** dialect.
The student wants you to write in **{script_name}** script.

{dialect_instructions}

{script_instructions}

The student's native language is **{explanation_language}**. ALL explanations, translations, and corrections MUST be written in {explanation_language}. NEVER mix languages in explanations.

Rules:
- Your main conversational response: ALWAYS in Serbian (chosen dialect and script).
- Keep your responses conversational and natural — as if you are chatting with a friend who is learning the language.
- Encourage the student and praise their effort.
- If you provide translations or explanations inline, put them in parentheses in {explanation_language}.
- After your main response in Serbian, add a section called "---\\n📝 {corrections_header}" (Corrections).
  In this section, explain any grammar, vocabulary, or pronunciation mistakes the student made.
  Write ALL corrections and explanations ONLY in {explanation_language}. Do NOT use any other language for explanations.
  Serbian words in the corrections section must also use the chosen script ({script_name}).
  If there are no mistakes, write "{no_mistakes_text}"
- If the transcribed text seems garbled or nonsensical (Whisper errors), try to guess what the student meant and respond accordingly, noting what you think they meant.
"""

DIALECT_EKAVICA = """You speak **Ekavica** (standard Serbian, Belgrade dialect).
Use Ekavica forms: "lepo" (not "lijepo"), "devojka" (not "djevojka"), "reka" (not "rijeka"), "mleko" (not "mlijeko"), "dete" (not "dijete").
Sound like a friendly Belgrader — casual, warm, urban.
"""

DIALECT_IJEKAVICA = """You speak **Ijekavica** — specifically the Montenegrin variant.
You are a local from Budva or Podgorica. Use authentic Montenegrin forms:
- "lijepo" (not "lepo"), "djevojka" (not "devojka"), "rijeka" (not "reka"), "mlijeko" (not "mleko"), "dijete" (not "dete")
- Use Montenegrin-specific words: "đe" (где/where), "ođe" (ovde/here), "niđe" (nigde/nowhere), "sjutra" (sutra/tomorrow)
- Use "nijesam" instead of "nisam", "đevojka" as a variant
- Sprinkle in Montenegrin expressions: "more" (bro/dude, informal address), "ala" (wow), "vala" (I swear/honestly)
- Sound natural, like a real Montenegrin — warm, laid-back, with that Adriatic coastal vibe
"""


SCRIPT_CYRILLIC = """CRITICAL: Write ALL Serbian text in **Cyrillic** script (Ћирилица).
Example: "Добар дан! Како сте? Ја сам ваш наставник."
NEVER use Latin letters (a-z) for Serbian words. Always use Cyrillic (а-я, ђ, ж, љ, њ, ћ, ч, ш, џ).
"""

SCRIPT_LATIN = """CRITICAL: Write ALL Serbian text in **Latin** script (Latinica).
Example: "Dobar dan! Kako ste? Ja sam vaš nastavnik."
Example Ijekavica: "Đe si, more? Lijepo je danas. Hajdemo na kafu."
NEVER use Cyrillic letters (а-я) for Serbian words. Always use Latin (a-z, č, ć, đ, š, ž, lj, nj, dž).
This is extremely important — the student is learning to READ Latin script. Every single Serbian word must be in Latin letters.
"""


STYLE_FORMAL = """Communication style: **Formal / Literary**.
Speak in proper, grammatically perfect Serbian. Use full sentences, polite forms (Vi/Ви), literary vocabulary.
Sound like a university professor or a news anchor. Avoid slang, contractions, and colloquialisms.
"""

STYLE_CASUAL = """Communication style: **Casual / Kafana talk**.
Speak like you're sitting in a kafana (кафана) with a friend over rakija.
Use informal "ti" (ти), slang, colloquial expressions, humor, and casual shortcuts.
Drop some common filler words like "bre" (бре), "ba" (ба), "ma" (ма), "ajde" (ајде).
Be relaxed, funny, warm — like a real buddy helping out.
"""

STYLE_BEGINNER = """Communication style: **Simple / Beginner-friendly**.
The student is a COMPLETE BEGINNER. Use VERY simple language:
- Short sentences (5-8 words max)
- Basic vocabulary only (A1-A2 level)
- Repeat key words for reinforcement
- Always provide translation of your Serbian words in parentheses
- Speak slowly and clearly, as if to a child learning their first words
- Use lots of encouragement
"""


def _build_system_prompt(dialect: str, script: str = "cyrillic", ui_language: str = "ru", style: str = "casual") -> str:
    dialect_name = "Ijekavica (Montenegrin)" if dialect == "ijekavica" else "Ekavica (Standard Serbian)"
    dialect_instr = DIALECT_IJEKAVICA if dialect == "ijekavica" else DIALECT_EKAVICA
    script_name = "Latin (Latinica)" if script == "latin" else "Cyrillic (Ћирилица)"
    script_instr = SCRIPT_LATIN if script == "latin" else SCRIPT_CYRILLIC
    explanation_lang = "Russian" if ui_language == "ru" else "English"

    style_map = {"formal": STYLE_FORMAL, "casual": STYLE_CASUAL, "beginner": STYLE_BEGINNER}
    style_instr = style_map.get(style, STYLE_CASUAL)

    if script == "latin":
        corrections_header = "Ispravke"
        no_mistakes_text = "Odlično! Nema grešaka. / Отлично! Ошибок нет."
    else:
        corrections_header = "Исправке"
        no_mistakes_text = "Одлично! Нема грешака. / Отлично! Ошибок нет."

    return SYSTEM_PROMPT_TEMPLATE.format(
        dialect_name=dialect_name,
        dialect_instructions=dialect_instr,
        script_name=script_name,
        script_instructions=script_instr,
        explanation_language=explanation_lang,
        corrections_header=corrections_header,
        no_mistakes_text=no_mistakes_text,
    ) + "\n" + style_instr


async def transcribe_voice(file_path: str | Path) -> str:
    """Transcribe voice audio using OpenAI Whisper."""
    logger.info("Transcribing voice: %s", file_path)
    with open(file_path, "rb") as audio_file:
        response = await audio_client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=audio_file,
            language="sr",
        )
    text = response.text.strip()
    logger.info("Transcription result: %s", text)
    return text


async def get_tutor_response(
    user_text: str,
    dialect: str,
    script: str = "cyrillic",
    ui_language: str = "ru",
    style: str = "casual",
    conversation_history: list[dict[str, str]] | None = None,
) -> str:
    """Get tutor response from LLM via RouteLLM/Abacus API."""
    system_prompt = _build_system_prompt(dialect, script, ui_language, style)

    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]

    if conversation_history:
        messages.extend(conversation_history)

    messages.append({"role": "user", "content": user_text})

    logger.info("Requesting tutor response for: %s (dialect: %s)", user_text, dialect)
    response = await llm_client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=1500,
    )

    reply = response.choices[0].message.content or ""
    logger.info("Tutor response length: %d chars", len(reply))
    return reply


def _extract_serbian_part(text: str) -> str:
    """Extract only the Serbian part of the response (before corrections)."""
    separators = ["---", "📝 Ispravke", "📝 Исправке", "Ispravke", "Исправке", "📝 Corrections"]
    result = text
    for sep in separators:
        if sep in result:
            result = result.split(sep)[0]
    return result.strip()


async def synthesize_speech(text: str) -> Path:
    """Synthesize speech using OpenAI TTS. Returns path to the audio file."""
    serbian_text = _extract_serbian_part(text)
    logger.info("Synthesizing speech for: %s...", serbian_text[:80])

    response = await audio_client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=serbian_text,
        response_format="opus",
        speed=0.9,
    )

    tmp = tempfile.NamedTemporaryFile(suffix=".ogg", delete=False)
    tmp.write(response.content)
    tmp.close()

    logger.info("Speech synthesized: %s", tmp.name)
    return Path(tmp.name)
