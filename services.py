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

Rules:
- Always respond in Serbian using the chosen dialect and script.
- Keep your responses conversational and natural — as if you are chatting with a friend who is learning the language.
- Encourage the student and praise their effort.
- If the student makes mistakes, gently correct them.
- After your main response in Serbian, add a section called "---\\n📝 Ispravke / Исправке" (Corrections).
  In this section, explain any grammar, vocabulary, or pronunciation mistakes the student made.
  Write the corrections in Russian so the student can understand them.
  If there are no mistakes, write "Одлично! Нема грешака. / Отлично! Ошибок нет."
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


SCRIPT_CYRILLIC = """Write ALL your Serbian text in **Cyrillic** script (Ћирилица).
Example: "Добар дан! Како сте? Ја сам ваш наставник."
NEVER use Latin letters for Serbian words in your main response.
"""

SCRIPT_LATIN = """Write ALL your Serbian text in **Latin** script (Latinica).
Example: "Dobar dan! Kako ste? Ja sam vaš nastavnik."
NEVER use Cyrillic letters for Serbian words in your main response.
"""


def _build_system_prompt(dialect: str, script: str = "cyrillic") -> str:
    dialect_name = "Ijekavica (Montenegrin)" if dialect == "ijekavica" else "Ekavica (Standard Serbian)"
    dialect_instr = DIALECT_IJEKAVICA if dialect == "ijekavica" else DIALECT_EKAVICA
    script_name = "Latin (Latinica)" if script == "latin" else "Cyrillic (Ћирилица)"
    script_instr = SCRIPT_LATIN if script == "latin" else SCRIPT_CYRILLIC

    return SYSTEM_PROMPT_TEMPLATE.format(
        dialect_name=dialect_name,
        dialect_instructions=dialect_instr,
        script_name=script_name,
        script_instructions=script_instr,
    )


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
    conversation_history: list[dict[str, str]] | None = None,
) -> str:
    """Get tutor response from LLM via RouteLLM/Abacus API."""
    system_prompt = _build_system_prompt(dialect, script)

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
    separators = ["---", "📝 Ispravke", "📝 Исправке", "Ispravke", "Исправке"]
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
        response_format="mp3",
    )

    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp.write(response.content)
    tmp.close()

    logger.info("Speech synthesized: %s", tmp.name)
    return Path(tmp.name)
