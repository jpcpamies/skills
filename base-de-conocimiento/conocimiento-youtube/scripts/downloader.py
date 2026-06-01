"""Descarga de transcripciones con rotación de estrategias.

Para cada vídeo, prueba varias estrategias en orden hasta conseguir la
transcripción o agotar todas las opciones. Devuelve resultado estructurado.
"""

import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from srt_parser import srt_to_plain_text


# Backoff exponencial dentro de una sesión (segundos)
BACKOFF_LADDER = [30, 120, 300, 900, 1800, 3600, 7200, 14400]

# Errores que indican fallo permanente
PERMANENT_ERROR_PATTERNS = [
    "Video unavailable",
    "This video has been removed",
    "Private video",
    "This video is no longer available",
    "Video has been removed",
    "This video is private",
    "Account has been terminated",
    "video has been deleted",
]

# Errores que indican necesidad de cooldown largo
COOLDOWN_ERROR_PATTERNS = [
    "Sign in to confirm you're not a bot",
    "Sign in to confirm",
    "captcha",
    "Too Many Requests",
    "HTTP Error 429",
]


@dataclass
class DownloadResult:
    success: bool
    transcript_text: Optional[str] = None
    language: Optional[str] = None
    error: Optional[str] = None
    is_permanent: bool = False
    needs_cooldown: bool = False
    no_transcript: bool = False


def _classify_error(stderr: str) -> tuple[bool, bool, bool]:
    """Clasifica el error. Devuelve (is_permanent, needs_cooldown, no_transcript)."""
    if not stderr:
        return (False, False, False)
    lower = stderr.lower()

    for pat in PERMANENT_ERROR_PATTERNS:
        if pat.lower() in lower:
            return (True, False, False)

    for pat in COOLDOWN_ERROR_PATTERNS:
        if pat.lower() in lower:
            return (False, True, False)

    if "no subtitles" in lower or "no automatic captions" in lower:
        return (False, False, True)

    return (False, False, False)


def _run_ytdlp(
    video_url: str,
    output_dir: Path,
    languages: list[str],
    extra_args: Optional[list[str]] = None,
    timeout: int = 180,
) -> tuple[bool, str, Optional[Path], Optional[str]]:
    """Ejecuta yt-dlp con flags para descargar solo subtítulos.

    Devuelve (success, error_message, srt_path, language_detected).
    """
    output_template = str(output_dir / "%(id)s.%(ext)s")
    lang_string = ",".join(languages)

    cmd = [
        "yt-dlp",
        "--write-auto-subs",
        "--write-subs",
        "--sub-lang",
        lang_string,
        "--skip-download",
        "--convert-subs",
        "srt",
        "--no-warnings",
        "--retries",
        "5",
        "--fragment-retries",
        "5",
        "--sleep-requests",
        "2",
        "--sleep-interval",
        "3",
        "--max-sleep-interval",
        "8",
        "-o",
        output_template,
    ]

    if extra_args:
        cmd.extend(extra_args)

    cmd.append(video_url)

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return (False, "Timeout en yt-dlp", None, None)

    if result.returncode != 0:
        return (False, result.stderr or result.stdout, None, None)

    srt_files = sorted(output_dir.glob("*.srt"))
    if not srt_files:
        return (False, "No se generó archivo .srt", None, None)

    srt_path = srt_files[0]
    detected_lang = None
    parts = srt_path.stem.rsplit(".", 1)
    if len(parts) == 2:
        detected_lang = parts[1]

    return (True, "", srt_path, detected_lang)


def _try_youtube_transcript_api(
    video_id: str, languages: list[str]
) -> tuple[bool, str, Optional[str], Optional[str]]:
    """Intenta descargar via youtube-transcript-api como último recurso."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import (
            TranscriptsDisabled,
            NoTranscriptFound,
            VideoUnavailable,
        )
    except ImportError:
        return (False, "youtube-transcript-api no instalado", None, None)

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Buscar primero en idiomas preferidos manuales, luego automáticos
        transcript = None
        for lang in languages:
            try:
                transcript = transcript_list.find_manually_created_transcript([lang])
                break
            except NoTranscriptFound:
                continue
        if transcript is None:
            for lang in languages:
                try:
                    transcript = transcript_list.find_generated_transcript([lang])
                    break
                except NoTranscriptFound:
                    continue
        if transcript is None:
            available = list(transcript_list)
            if available:
                transcript = available[0]
            else:
                return (False, "No transcripts available", None, None)

        data = transcript.fetch()
        text_parts = [item["text"] for item in data if item.get("text")]
        text = " ".join(text_parts).strip()
        return (True, "", text, transcript.language_code)

    except TranscriptsDisabled:
        return (False, "Transcripts disabled", None, None)
    except NoTranscriptFound as e:
        return (False, f"No transcript found: {e}", None, None)
    except VideoUnavailable as e:
        return (False, f"Video unavailable: {e}", None, None)
    except Exception as e:
        return (False, f"transcript-api error: {e}", None, None)


def download_transcript(
    video_id: str,
    video_url: str,
    languages: list[str],
    use_cookies_browser: Optional[str] = None,
) -> DownloadResult:
    """Intenta descargar la transcripción probando múltiples estrategias.

    Estrategias en orden:
      A. yt-dlp estándar
      B. yt-dlp con cookies del navegador (si está activado)
      C. yt-dlp con player_client=android,web
      D. youtube-transcript-api
    """
    last_error = ""

    strategies: list[tuple[str, Optional[list[str]]]] = [
        ("yt-dlp estándar", None),
    ]
    if use_cookies_browser:
        strategies.append(
            (
                f"yt-dlp con cookies de {use_cookies_browser}",
                ["--cookies-from-browser", use_cookies_browser],
            )
        )
    strategies.append(
        (
            "yt-dlp con player_client=android,web",
            ["--extractor-args", "youtube:player_client=android,web"],
        )
    )

    cooldown_signal = False

    for name, extra_args in strategies:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            success, error, srt_path, language = _run_ytdlp(
                video_url, tmp_path, languages, extra_args=extra_args
            )
            if success and srt_path:
                text = srt_to_plain_text(
                    srt_path.read_text(encoding="utf-8", errors="replace")
                )
                if text.strip():
                    return DownloadResult(
                        success=True,
                        transcript_text=text,
                        language=language,
                    )
                last_error = "SRT vacío tras parsear"
            else:
                last_error = error
                is_perm, needs_cool, no_trans = _classify_error(error)
                if is_perm:
                    return DownloadResult(
                        success=False,
                        error=error,
                        is_permanent=True,
                    )
                if needs_cool:
                    cooldown_signal = True
                if no_trans:
                    # Aún probaremos transcript-api por si tiene
                    pass

        time.sleep(60)  # Pausa de 1 minuto entre estrategias

    # Estrategia D: youtube-transcript-api
    success, error, text, language = _try_youtube_transcript_api(video_id, languages)
    if success and text:
        return DownloadResult(
            success=True,
            transcript_text=text,
            language=language,
        )

    last_error = error or last_error

    is_perm, needs_cool, no_trans = _classify_error(last_error)
    if no_trans or "no transcript" in (last_error or "").lower() or "transcripts disabled" in (last_error or "").lower():
        return DownloadResult(
            success=False,
            error=last_error,
            no_transcript=True,
        )

    return DownloadResult(
        success=False,
        error=last_error,
        needs_cooldown=cooldown_signal,
    )


def get_backoff_seconds(attempt_number: int) -> int:
    """Devuelve los segundos de espera para un número de intento (1-indexed)."""
    idx = min(attempt_number - 1, len(BACKOFF_LADDER) - 1)
    return BACKOFF_LADDER[max(0, idx)]


def check_yt_dlp_available() -> bool:
    """Verifica que yt-dlp está instalado y accesible."""
    return shutil.which("yt-dlp") is not None


def check_transcript_api_available() -> bool:
    """Verifica que youtube-transcript-api (el fallback) está instalado."""
    try:
        import youtube_transcript_api  # noqa: F401
        return True
    except ImportError:
        return False


def check_dependencies() -> list[str]:
    """Devuelve la lista de dependencias que faltan (vacía si todo OK)."""
    missing = []
    if not check_yt_dlp_available():
        missing.append("yt-dlp")
    if not check_transcript_api_available():
        missing.append("youtube-transcript-api")
    return missing


def update_yt_dlp() -> tuple[bool, str]:
    """Auto-actualiza yt-dlp. yt-dlp se rompe seguido cuando YouTube cambia;
    actualizarlo es la causa nº1 de desatascar un canal en failed_retriable.

    Devuelve (success, mensaje).
    """
    cmd = [sys.executable, "-m", "pip", "install", "-U", "yt-dlp"]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300
        )
    except subprocess.TimeoutExpired:
        return (False, "Timeout actualizando yt-dlp")
    except Exception as e:  # noqa: BLE001
        return (False, f"Error actualizando yt-dlp: {e}")

    if result.returncode != 0:
        return (False, (result.stderr or result.stdout or "").strip()[:200])
    return (True, "yt-dlp actualizado a la última versión")
