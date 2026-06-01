"""Enumeración inicial de canales y playlists de YouTube.

El listado completo es el cimiento del harvest. Este módulo se encarga de:
- Detectar si una URL es canal o playlist.
- Listar todos los vídeos con yt-dlp --flat-playlist.
- Validar que el listado parece completo.
- Reintentar si falla.
"""

import json
import re
import subprocess
import time
from pathlib import Path
from typing import Optional


CHANNEL_URL_PATTERNS = [
    re.compile(r"youtube\.com/channel/([A-Za-z0-9_-]+)"),
    re.compile(r"youtube\.com/@([A-Za-z0-9_.-]+)"),
    re.compile(r"youtube\.com/c/([A-Za-z0-9_.-]+)"),
    re.compile(r"youtube\.com/user/([A-Za-z0-9_.-]+)"),
]

PLAYLIST_URL_PATTERN = re.compile(r"[?&]list=([A-Za-z0-9_-]+)")


def detect_url_type(url: str) -> tuple[str, str]:
    """Detecta si la URL es de canal o playlist.

    Devuelve una tupla (tipo, id) donde tipo es "channel" o "playlist".
    Lanza ValueError si no se reconoce.
    """
    playlist_match = PLAYLIST_URL_PATTERN.search(url)
    if playlist_match and "watch?v=" not in url.split("?")[0]:
        return ("playlist", playlist_match.group(1))

    for pattern in CHANNEL_URL_PATTERNS:
        match = pattern.search(url)
        if match:
            return ("channel", match.group(1))

    if playlist_match:
        return ("playlist", playlist_match.group(1))

    raise ValueError(f"URL no reconocida como canal ni playlist: {url}")


def normalize_channel_url(url: str) -> list[str]:
    """Para canales, devuelve las URLs a enumerar (videos, streams, shorts).

    YouTube divide el contenido de un canal en pestañas. Para cosechar todo,
    enumeramos cada pestaña por separado.
    """
    base = url.rstrip("/")
    if "/videos" in base or "/streams" in base or "/shorts" in base:
        return [base]
    return [
        f"{base}/videos",
        f"{base}/streams",
        f"{base}/shorts",
    ]


def enumerate_url(url: str, sleep_requests: int = 1) -> list[dict]:
    """Lista los vídeos de una URL usando yt-dlp --flat-playlist.

    Devuelve una lista de dicts con video_id, title, upload_date, duration.
    """
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--no-warnings",
        "--ignore-errors",
        "--print",
        "%(id)s|%(title)s|%(upload_date)s|%(duration)s",
        "--sleep-requests",
        str(sleep_requests),
        url,
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=600
        )
    except subprocess.TimeoutExpired:
        return []

    videos = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or "|" not in line:
            continue
        parts = line.split("|", 3)
        if len(parts) < 4:
            continue
        video_id, title, upload_date, duration = parts
        if not video_id or video_id == "NA":
            continue
        try:
            duration_int = int(duration) if duration and duration != "NA" else 0
        except ValueError:
            duration_int = 0

        published_at = None
        if upload_date and upload_date != "NA" and len(upload_date) == 8:
            published_at = (
                f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}T00:00:00Z"
            )

        videos.append({
            "video_id": video_id,
            "title": title,
            "published_at": published_at,
            "duration_seconds": duration_int,
            "url": f"https://www.youtube.com/watch?v={video_id}",
        })

    return videos


def enumerate_with_retries(
    url: str,
    is_channel: bool,
    max_retries: int = 3,
    retry_wait_seconds: int = 120,
    output_path: Optional[Path] = None,
) -> list[dict]:
    """Enumera con reintentos. Si es canal, fusiona resultados de videos/streams/shorts.

    Si output_path se proporciona, guarda el listado bruto allí inmediatamente.
    """
    urls_to_enumerate = normalize_channel_url(url) if is_channel else [url]

    all_videos: dict[str, dict] = {}

    for sub_url in urls_to_enumerate:
        attempt = 0
        videos = []
        while attempt < max_retries:
            attempt += 1
            videos = enumerate_url(sub_url)
            if videos:
                break
            if attempt < max_retries:
                time.sleep(retry_wait_seconds)

        for v in videos:
            if v["video_id"] not in all_videos:
                all_videos[v["video_id"]] = v

    result = list(all_videos.values())

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    return result


def fetch_source_metadata(url: str) -> dict:
    """Obtiene metadatos del canal o playlist (nombre, id) sin listar vídeos."""
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--playlist-items",
        "0",
        "--print",
        "%(channel)s|%(channel_id)s|%(playlist_title)s|%(playlist_id)s",
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return {"name": "Unknown", "id": ""}

    line = (result.stdout.strip().splitlines() or [""])[0]
    parts = line.split("|", 3)
    while len(parts) < 4:
        parts.append("")
    channel, channel_id, playlist_title, playlist_id = parts

    name = playlist_title or channel or "Unknown"
    source_id = playlist_id or channel_id or ""

    return {
        "name": name.strip() or "Unknown",
        "id": source_id.strip(),
    }
