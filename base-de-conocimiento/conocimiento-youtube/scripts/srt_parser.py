"""Conversión de archivos .srt a texto plano limpio.

El skill recibe transcripciones de YouTube en formato SRT (a través de yt-dlp
con --convert-subs srt). Esta utilidad las convierte a texto corrido
eliminando timestamps, números de fragmento y marcas técnicas.
"""

import re
from pathlib import Path


# Patrón para detectar líneas que son solo timestamps
TIMESTAMP_RE = re.compile(
    r"^\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}.*$"
)

# Patrón para detectar líneas que son solo un número de fragmento
FRAGMENT_NUMBER_RE = re.compile(r"^\d+$")

# Marcas técnicas a eliminar
TECHNICAL_MARKERS = [
    re.compile(r"\[Music\]", re.IGNORECASE),
    re.compile(r"\[Applause\]", re.IGNORECASE),
    re.compile(r"\[Laughter\]", re.IGNORECASE),
    re.compile(r"\[Música\]", re.IGNORECASE),
    re.compile(r"\[Aplausos\]", re.IGNORECASE),
    re.compile(r"\[Risas\]", re.IGNORECASE),
    re.compile(r"\[Inaudible\]", re.IGNORECASE),
    re.compile(r"\[Silence\]", re.IGNORECASE),
    re.compile(r"\[Silencio\]", re.IGNORECASE),
    # Tags HTML que a veces aparecen
    re.compile(r"<[^>]+>"),
    # Posiciones de subtítulos tipo {\an8}
    re.compile(r"\{\\[^}]+\}"),
]


def srt_to_plain_text(srt_content: str) -> str:
    """Convierte contenido SRT a texto plano limpio."""
    lines = srt_content.splitlines()
    text_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if TIMESTAMP_RE.match(stripped):
            continue
        if FRAGMENT_NUMBER_RE.match(stripped):
            continue
        for pattern in TECHNICAL_MARKERS:
            stripped = pattern.sub("", stripped)
        stripped = stripped.strip()
        if stripped:
            text_lines.append(stripped)

    # Deduplicación de líneas consecutivas idénticas
    # (YouTube a veces repite líneas en subtítulos automáticos)
    deduped = []
    for line in text_lines:
        if not deduped or deduped[-1] != line:
            deduped.append(line)

    text = " ".join(deduped)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def srt_file_to_plain(srt_path: Path) -> str:
    """Lee un archivo SRT y devuelve texto plano."""
    content = srt_path.read_text(encoding="utf-8", errors="replace")
    return srt_to_plain_text(content)
