"""Normalización de strings a nombres de archivo seguros."""

import re
import unicodedata


def slugify(text: str, max_length: int = 120) -> str:
    """Convierte un string a un slug seguro para nombres de archivo.

    - Normaliza unicode (NFKD) y elimina diacríticos.
    - Sustituye caracteres no alfanuméricos por guiones.
    - Colapsa guiones múltiples.
    - Limita la longitud.
    """
    if not text:
        return "untitled"

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")

    if len(text) > max_length:
        text = text[:max_length].rstrip("-")

    return text or "untitled"


def unique_filename(slug: str, video_id: str, existing: set) -> str:
    """Devuelve un nombre de archivo único.

    Si el slug ya existe en el set `existing`, le añade un sufijo con los
    últimos 6 caracteres del video_id.
    """
    base = f"{slug}.txt"
    if base not in existing:
        return base
    suffix = video_id[-6:] if len(video_id) >= 6 else video_id
    return f"{slug}-{suffix}.txt"
