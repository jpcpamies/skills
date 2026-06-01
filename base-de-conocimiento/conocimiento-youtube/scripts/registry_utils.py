"""Lectura y escritura atómica del registry.json.

El registry es la fuente de verdad del estado del harvest. Se reescribe
después de cada vídeo procesado, así que tiene que ser barato y seguro.
"""

import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


VALID_STATES = {
    "pending",
    "downloaded",
    "failed_retriable",
    "failed_permanent",
    "no_transcript",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def empty_registry(source_type: str, name: str, slug: str, url: str, source_id: str) -> dict:
    """Crea un registry vacío con la estructura canónica."""
    return {
        "source": {
            "type": source_type,
            "name": name,
            "slug": slug,
            "url": url,
            "id": source_id,
            "first_harvest": now_iso(),
            "last_harvest": None,
            "last_incremental_check": None,
        },
        "stats": {
            "total_videos": 0,
            "downloaded": 0,
            "failed_retriable": 0,
            "failed_permanent": 0,
            "no_transcript_available": 0,
            "pending": 0,
        },
        "videos": {},
    }


def load_registry(path: Path) -> Optional[dict]:
    """Carga el registry. Devuelve None si no existe.

    Si el archivo principal está corrupto, intenta cargar el backup.
    """
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        backup = path.with_suffix(".json.backup")
        if backup.exists():
            print(f"[WARN] {path} corrupto, cargando backup")
            with open(backup, "r", encoding="utf-8") as f:
                return json.load(f)
        raise


def save_registry(path: Path, registry: dict) -> None:
    """Escritura atómica: escribe a tmp y renombra."""
    path.parent.mkdir(parents=True, exist_ok=True)
    recompute_stats(registry)

    fd, tmp_path = tempfile.mkstemp(
        prefix=".registry_", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def backup_registry(path: Path) -> None:
    """Copia el registry a registry.json.backup."""
    if path.exists():
        backup = path.with_suffix(".json.backup")
        shutil.copy2(path, backup)


def recompute_stats(registry: dict) -> None:
    """Recalcula las stats agregadas a partir del estado de los vídeos."""
    counts = {
        "downloaded": 0,
        "failed_retriable": 0,
        "failed_permanent": 0,
        "no_transcript_available": 0,
        "pending": 0,
    }
    for v in registry["videos"].values():
        status = v.get("status", "pending")
        if status == "downloaded":
            counts["downloaded"] += 1
        elif status == "failed_retriable":
            counts["failed_retriable"] += 1
        elif status == "failed_permanent":
            counts["failed_permanent"] += 1
        elif status == "no_transcript":
            counts["no_transcript_available"] += 1
        else:
            counts["pending"] += 1

    registry["stats"] = {
        "total_videos": len(registry["videos"]),
        **counts,
    }


def add_video(registry: dict, video_id: str, video_data: dict) -> bool:
    """Añade un vídeo al registry si no existe ya. Devuelve True si era nuevo."""
    if video_id in registry["videos"]:
        return False

    registry["videos"][video_id] = {
        "title": video_data.get("title", ""),
        "url": video_data.get("url", f"https://www.youtube.com/watch?v={video_id}"),
        "published_at": video_data.get("published_at"),
        "duration_seconds": video_data.get("duration_seconds", 0),
        "status": "pending",
        "attempts": 0,
        "last_attempt": None,
        "last_error": None,
        "transcript_filename": None,
        "language_detected": None,
    }
    return True


def update_video_status(
    registry: dict,
    video_id: str,
    status: str,
    error: Optional[str] = None,
    transcript_filename: Optional[str] = None,
    language: Optional[str] = None,
) -> None:
    """Actualiza el estado de un vídeo."""
    if status not in VALID_STATES:
        raise ValueError(f"Estado inválido: {status}")

    if video_id not in registry["videos"]:
        raise KeyError(f"Vídeo {video_id} no está en el registry")

    v = registry["videos"][video_id]
    v["status"] = status
    v["last_attempt"] = now_iso()
    v["attempts"] = v.get("attempts", 0) + 1

    if error is not None:
        v["last_error"] = error
    elif status == "downloaded":
        v["last_error"] = None

    if transcript_filename:
        v["transcript_filename"] = transcript_filename
    if language:
        v["language_detected"] = language


def get_pending_videos(registry: dict, include_retriable: bool = True) -> list:
    """Devuelve la lista de video_ids pendientes de procesar."""
    pending = []
    for vid, data in registry["videos"].items():
        status = data.get("status", "pending")
        if status == "pending":
            pending.append(vid)
        elif include_retriable and status == "failed_retriable":
            pending.append(vid)
    return pending


def reset_retriable_attempts(registry: dict, hours_threshold: int = 24) -> int:
    """Resetea el contador de intentos para vídeos failed_retriable cuya última
    tentativa fue hace más de N horas. Devuelve el número de vídeos reseteados.
    """
    from datetime import timedelta

    threshold = datetime.now(timezone.utc) - timedelta(hours=hours_threshold)
    count = 0
    for v in registry["videos"].values():
        if v.get("status") != "failed_retriable":
            continue
        last = v.get("last_attempt")
        if not last:
            continue
        try:
            last_dt = datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )
            if last_dt < threshold:
                v["attempts"] = 0
                count += 1
        except ValueError:
            continue
    return count
