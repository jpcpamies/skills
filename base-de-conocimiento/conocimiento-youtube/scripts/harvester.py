#!/usr/bin/env python3
"""YouTube Channel Harvester - Orquestador principal.

Uso:
    python harvester.py harvest <URL> [--lang <idioma>] [--cookies-from-browser <browser>] [--root <dir>]
    python harvester.py update <slug> [--root <dir>]
    python harvester.py status <slug> [--root <dir>]
    python harvester.py retry <slug> [--root <dir>]

Ejemplos:
    python harvester.py harvest https://www.youtube.com/@nombredelcanal
    python harvester.py harvest https://www.youtube.com/playlist?list=PLxxx --lang es
    python harvester.py update nombredelcanal
    python harvester.py status nombredelcanal
"""

import argparse
import logging
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from build_unified import build_status_md, build_unified
from downloader import (
    check_dependencies,
    download_transcript,
    get_backoff_seconds,
    update_yt_dlp,
)
from enumerator import (
    detect_url_type,
    enumerate_with_retries,
    fetch_source_metadata,
)
from registry_utils import (
    add_video,
    backup_registry,
    empty_registry,
    get_pending_videos,
    load_registry,
    now_iso,
    reset_retriable_attempts,
    save_registry,
    update_video_status,
)
from slugify import slugify, unique_filename


def configure_logging(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("harvester")
    logger.setLevel(logging.INFO)
    logger.handlers = []

    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)sZ [%(levelname)s] %(message)s",
                          datefmt="%Y-%m-%dT%H:%M:%S")
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("[%(levelname)s] %(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def get_root_for_type(base_root: Path, source_type: str) -> Path:
    """Devuelve la carpeta madre 'canales/' o 'playlists/'."""
    folder = "canales" if source_type == "channel" else "playlists"
    return base_root / folder


def require_dependencies() -> bool:
    """Verifica yt-dlp y youtube-transcript-api. Imprime guía si falta algo.

    Devuelve True si todo está disponible, False en caso contrario.
    """
    missing = check_dependencies()
    if missing:
        print(
            "ERROR: faltan dependencias: "
            + ", ".join(missing)
            + "\nInstálalas con: pip install -r requirements.txt"
        )
        return False
    return True


def get_batch_config(total_videos: int) -> tuple[int, int]:
    """Devuelve (tamaño_lote, pausa_min_entre_lotes_segundos)."""
    if total_videos < 200:
        return (50, 5 * 60)
    if total_videos < 500:
        return (30, 10 * 60)
    if total_videos < 1500:
        return (25, 20 * 60)
    if total_videos < 3000:
        return (20, 30 * 60)
    return (15, 45 * 60)


def harvest_initial(
    url: str,
    base_root: Path,
    languages: list[str],
    cookies_browser: Optional[str] = None,
) -> int:
    """Modo descarga inicial."""
    if not require_dependencies():
        return 1

    source_type, source_id_from_url = detect_url_type(url)
    print(f"[INFO] Detectado: {source_type} (id={source_id_from_url})")

    print(f"[INFO] Obteniendo metadatos...")
    metadata = fetch_source_metadata(url)
    name = metadata["name"]
    slug = slugify(name)
    print(f"[INFO] Nombre: {name} | slug: {slug}")

    type_root = get_root_for_type(base_root, source_type)
    target_dir = type_root / slug
    transcripts_dir = target_dir / "transcripts"
    logs_dir = target_dir / "logs"
    registry_path = target_dir / "registry.json"

    target_dir.mkdir(parents=True, exist_ok=True)
    transcripts_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)

    logger = configure_logging(logs_dir / "harvest.log")
    logger.info(f"=== INICIO HARVEST ({source_type}) ===")
    logger.info(f"URL: {url}")
    logger.info(f"Nombre: {name} | slug: {slug}")

    registry = load_registry(registry_path)
    if registry is None:
        logger.info("Sin registry previo. Creando uno nuevo.")
        registry = empty_registry(
            source_type=source_type,
            name=name,
            slug=slug,
            url=url,
            source_id=metadata["id"] or source_id_from_url,
        )
    else:
        logger.info(f"Registry existente cargado: {len(registry['videos'])} vídeos.")

    # Enumeración inicial
    logger.info("Enumerando vídeos del origen...")
    enum_path = target_dir / "enumeration_raw.json"
    videos_in_source = enumerate_with_retries(
        url,
        is_channel=(source_type == "channel"),
        max_retries=3,
        retry_wait_seconds=120,
        output_path=enum_path,
    )
    logger.info(f"Detectados {len(videos_in_source)} vídeos.")

    if not videos_in_source:
        logger.error("Enumeración devolvió 0 vídeos. Abortando.")
        return 2

    # Añadir nuevos vídeos al registry
    new_count = 0
    for v in videos_in_source:
        if add_video(registry, v["video_id"], v):
            new_count += 1
    if new_count:
        logger.info(f"Añadidos {new_count} vídeos nuevos al registry.")
    save_registry(registry_path, registry)

    # Procesar
    return _process_pending(
        registry_path=registry_path,
        target_dir=target_dir,
        languages=languages,
        cookies_browser=cookies_browser,
        logger=logger,
    )


def harvest_update(
    slug: str,
    base_root: Path,
    languages: list[str],
    cookies_browser: Optional[str] = None,
) -> int:
    """Modo incremental: busca canal/playlist por slug, comprueba novedades."""
    if not require_dependencies():
        return 1

    target_dir = _find_target_dir(base_root, slug)
    if target_dir is None:
        print(f"ERROR: No encuentro un canal o playlist con slug '{slug}'")
        return 1

    registry_path = target_dir / "registry.json"
    logs_dir = target_dir / "logs"
    logger = configure_logging(logs_dir / "harvest.log")
    logger.info(f"=== INICIO UPDATE ({slug}) ===")

    registry = load_registry(registry_path)
    if registry is None:
        logger.error("No existe registry. Usa 'harvest <URL>' para empezar.")
        return 2

    url = registry["source"]["url"]
    is_channel = registry["source"]["type"] == "channel"

    # Re-enumerar
    logger.info("Re-enumerando origen...")
    videos_in_source = enumerate_with_retries(
        url,
        is_channel=is_channel,
        max_retries=3,
        retry_wait_seconds=120,
    )

    new_count = 0
    for v in videos_in_source:
        if add_video(registry, v["video_id"], v):
            new_count += 1
    logger.info(f"Vídeos nuevos detectados: {new_count}")

    # Resetear failed_retriable antiguos
    reset_count = reset_retriable_attempts(registry, hours_threshold=24)
    if reset_count:
        logger.info(f"Reseteados {reset_count} vídeos failed_retriable para reintento.")

    registry["source"]["last_incremental_check"] = now_iso()
    save_registry(registry_path, registry)

    return _process_pending(
        registry_path=registry_path,
        target_dir=target_dir,
        languages=languages,
        cookies_browser=cookies_browser,
        logger=logger,
    )


def harvest_status(slug: str, base_root: Path) -> int:
    target_dir = _find_target_dir(base_root, slug)
    if target_dir is None:
        print(f"ERROR: No encuentro slug '{slug}'")
        return 1
    status_path = target_dir / "logs" / "status.md"
    if not status_path.exists():
        registry = load_registry(target_dir / "registry.json")
        if registry is None:
            print(f"ERROR: No hay registry para '{slug}'")
            return 2
        build_status_md(registry, status_path)
    print(status_path.read_text(encoding="utf-8"))
    return 0


def harvest_retry(
    slug: str,
    base_root: Path,
    languages: list[str],
    cookies_browser: Optional[str] = None,
) -> int:
    """Fuerza reintento de los failed_retriable, ignorando el cooldown de 24h."""
    if not require_dependencies():
        return 1

    target_dir = _find_target_dir(base_root, slug)
    if target_dir is None:
        print(f"ERROR: No encuentro slug '{slug}'")
        return 1

    registry_path = target_dir / "registry.json"
    logger = configure_logging(target_dir / "logs" / "harvest.log")
    logger.info(f"=== INICIO RETRY FORZADO ({slug}) ===")

    # yt-dlp obsoleto es la causa nº1 de un canal atascado: actualizar primero.
    logger.info("Auto-actualizando yt-dlp antes de reintentar...")
    ok, msg = update_yt_dlp()
    logger.info(msg if ok else f"No se pudo actualizar yt-dlp: {msg}")

    registry = load_registry(registry_path)
    if registry is None:
        logger.error("Sin registry.")
        return 2

    # Resetear todos los failed_retriable
    count = 0
    for v in registry["videos"].values():
        if v.get("status") == "failed_retriable":
            v["attempts"] = 0
            count += 1
    logger.info(f"Reseteados {count} vídeos para reintento forzado.")
    save_registry(registry_path, registry)

    return _process_pending(
        registry_path=registry_path,
        target_dir=target_dir,
        languages=languages,
        cookies_browser=cookies_browser,
        logger=logger,
    )


def _find_target_dir(base_root: Path, slug: str) -> Optional[Path]:
    """Busca el directorio del canal/playlist por slug."""
    for parent_name in ("canales", "playlists"):
        candidate = base_root / parent_name / slug
        if candidate.exists():
            return candidate
    return None


def _process_pending(
    registry_path: Path,
    target_dir: Path,
    languages: list[str],
    cookies_browser: Optional[str],
    logger: logging.Logger,
) -> int:
    """Bucle principal de descarga con batching y backoff."""
    transcripts_dir = target_dir / "transcripts"
    logs_dir = target_dir / "logs"
    transcripts_dir.mkdir(exist_ok=True)

    registry = load_registry(registry_path)
    pending = get_pending_videos(registry, include_retriable=True)
    total_pending = len(pending)
    logger.info(f"Vídeos pendientes en esta sesión: {total_pending}")

    if not pending:
        logger.info("No hay nada pendiente.")
        registry["source"]["last_harvest"] = now_iso()
        save_registry(registry_path, registry)
        _finalize(registry_path, target_dir, logger)
        return 0

    total_videos = registry["stats"]["total_videos"]
    batch_size, batch_pause_s = get_batch_config(total_videos)
    logger.info(f"Configuración de lote: {batch_size} vídeos / pausa {batch_pause_s//60}min")

    # Para detectar bloqueos persistentes
    consecutive_cooldown_signals = 0
    consecutive_failures = 0
    backup_counter = 0

    # Existing filenames para evitar colisiones
    existing_filenames = set()
    for v in registry["videos"].values():
        fname = v.get("transcript_filename")
        if fname:
            existing_filenames.add(fname)

    processed_in_session = 0

    for batch_start in range(0, len(pending), batch_size):
        batch = pending[batch_start:batch_start + batch_size]
        batch_num = batch_start // batch_size + 1
        total_batches = (len(pending) + batch_size - 1) // batch_size
        logger.info(f"--- Lote {batch_num}/{total_batches} ({len(batch)} vídeos) ---")

        for video_id in batch:
            v_data = registry["videos"].get(video_id)
            if not v_data:
                continue
            if v_data["status"] == "downloaded":
                continue

            title = v_data.get("title", video_id)
            url = v_data.get("url", f"https://www.youtube.com/watch?v={video_id}")

            # Determinar attempts actuales
            current_attempts = v_data.get("attempts", 0)

            # Aplicar backoff si ha fallado antes en esta sesión
            if current_attempts >= 1 and v_data.get("status") == "failed_retriable":
                backoff = get_backoff_seconds(current_attempts)
                if backoff > 60:
                    logger.info(f"Backoff de {backoff}s antes de reintentar {video_id}")
                    time.sleep(backoff)

            logger.info(f"Descargando: {title[:80]} (id={video_id})")

            result = download_transcript(
                video_id=video_id,
                video_url=url,
                languages=languages,
                use_cookies_browser=cookies_browser,
            )

            if result.success and result.transcript_text:
                # Guardar archivo
                slug_title = slugify(title)
                filename = unique_filename(slug_title, video_id, existing_filenames)
                existing_filenames.add(filename)
                txt_path = transcripts_dir / filename
                txt_path.write_text(result.transcript_text, encoding="utf-8")

                update_video_status(
                    registry,
                    video_id,
                    status="downloaded",
                    transcript_filename=filename,
                    language=result.language,
                )
                logger.info(f"[OK] {title[:60]} -> {filename}")
                consecutive_failures = 0
                consecutive_cooldown_signals = 0

            elif result.is_permanent:
                update_video_status(
                    registry,
                    video_id,
                    status="failed_permanent",
                    error=result.error,
                )
                logger.warning(f"[FAIL_PERM] {video_id}: {result.error[:120] if result.error else ''}")
                consecutive_failures = 0

            elif result.no_transcript:
                update_video_status(
                    registry,
                    video_id,
                    status="no_transcript",
                    error=result.error,
                )
                logger.info(f"[NO_TRANS] {video_id}: sin transcripción")
                consecutive_failures = 0

            else:
                update_video_status(
                    registry,
                    video_id,
                    status="failed_retriable",
                    error=result.error,
                )
                logger.warning(f"[FAIL_RETRY] {video_id}: {(result.error or '')[:120]}")
                consecutive_failures += 1
                if result.needs_cooldown:
                    consecutive_cooldown_signals += 1

            processed_in_session += 1
            save_registry(registry_path, registry)

            backup_counter += 1
            if backup_counter >= 100:
                backup_registry(registry_path)
                backup_counter = 0

            # Detección de cooldown nocturno
            if consecutive_cooldown_signals >= 3:
                logger.error(
                    "Rate limit persistente detectado (3 señales consecutivas). "
                    "Activando cooldown nocturno. Reanuda con 'harvest update <slug>' "
                    "en 6-12h."
                )
                registry["source"]["last_harvest"] = now_iso()
                save_registry(registry_path, registry)
                _finalize(registry_path, target_dir, logger)
                return 3

            if consecutive_failures >= 5:
                logger.warning(
                    f"5 fallos consecutivos. Pausa de 1h y cambio de ritmo."
                )
                time.sleep(3600)
                consecutive_failures = 0

        # Fin del lote
        if batch_start + batch_size < len(pending):
            logger.info(
                f"Lote {batch_num} completado. "
                f"Procesados en sesión: {processed_in_session}/{total_pending}. "
                f"Pausa de {batch_pause_s//60}min antes del siguiente lote."
            )
            time.sleep(batch_pause_s)

    registry["source"]["last_harvest"] = now_iso()
    save_registry(registry_path, registry)
    _finalize(registry_path, target_dir, logger)
    logger.info(f"=== FIN HARVEST. Procesados en sesión: {processed_in_session} ===")
    return 0


def _finalize(registry_path: Path, target_dir: Path, logger: logging.Logger) -> None:
    """Regenera unified.md y status.md al final de cada sesión."""
    registry = load_registry(registry_path)
    if registry is None:
        return

    transcripts_dir = target_dir / "transcripts"
    unified_path = target_dir / "unified.md"
    status_path = target_dir / "logs" / "status.md"

    included = build_unified(transcripts_dir, unified_path, registry)
    logger.info(f"unified.md regenerado con {included} vídeos.")

    last_check = registry["source"].get("last_incremental_check") or registry["source"].get("last_harvest")
    next_check = None
    if last_check:
        try:
            dt = datetime.strptime(last_check, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            next_check = (dt + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            pass

    build_status_md(registry, status_path, next_check_iso=next_check)
    logger.info(f"status.md regenerado.")


def main():
    parser = argparse.ArgumentParser(description="YouTube Channel Harvester")
    sub = parser.add_subparsers(dest="command", required=True)

    p_harvest = sub.add_parser("harvest", help="Descarga inicial de canal/playlist")
    p_harvest.add_argument("url")
    p_harvest.add_argument("--lang", default="es,en", help="Idiomas separados por coma (default: es,en)")
    p_harvest.add_argument("--cookies-from-browser", default=None)
    p_harvest.add_argument("--root", default=".", help="Directorio raíz (default: cwd)")

    p_update = sub.add_parser("update", help="Modo incremental")
    p_update.add_argument("slug")
    p_update.add_argument("--lang", default="es,en")
    p_update.add_argument("--cookies-from-browser", default=None)
    p_update.add_argument("--root", default=".")

    p_status = sub.add_parser("status", help="Muestra status.md")
    p_status.add_argument("slug")
    p_status.add_argument("--root", default=".")

    p_retry = sub.add_parser("retry", help="Fuerza reintento de failed_retriable")
    p_retry.add_argument("slug")
    p_retry.add_argument("--lang", default="es,en")
    p_retry.add_argument("--cookies-from-browser", default=None)
    p_retry.add_argument("--root", default=".")

    args = parser.parse_args()
    base_root = Path(args.root).resolve()

    if args.command == "harvest":
        languages = [x.strip() for x in args.lang.split(",") if x.strip()]
        return harvest_initial(args.url, base_root, languages, args.cookies_from_browser)
    elif args.command == "update":
        languages = [x.strip() for x in args.lang.split(",") if x.strip()]
        return harvest_update(args.slug, base_root, languages, args.cookies_from_browser)
    elif args.command == "status":
        return harvest_status(args.slug, base_root)
    elif args.command == "retry":
        languages = [x.strip() for x in args.lang.split(",") if x.strip()]
        return harvest_retry(args.slug, base_root, languages, args.cookies_from_browser)


if __name__ == "__main__":
    sys.exit(main() or 0)
