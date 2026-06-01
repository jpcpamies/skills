"""Regenerador del unified.md desde los archivos .txt individuales.

Se ejecuta al final de cada harvest (o de cada lote) para mantener el
documento concatenado consistente con el estado real del registry.
"""

from pathlib import Path
from typing import Optional


def build_unified(
    transcripts_dir: Path,
    output_path: Path,
    registry: dict,
) -> int:
    """Regenera el unified.md a partir de los .txt en transcripts_dir.

    Orden cronológico (más antiguo → más nuevo) usando published_at del registry.
    Devuelve el número de vídeos incluidos.
    """
    videos = registry.get("videos", {})
    downloaded = [
        (vid, data)
        for vid, data in videos.items()
        if data.get("status") == "downloaded" and data.get("transcript_filename")
    ]

    def sort_key(item):
        _, data = item
        published = data.get("published_at") or "9999-99-99T00:00:00Z"
        return published

    downloaded.sort(key=sort_key)

    parts = []
    included = 0

    for video_id, data in downloaded:
        filename = data["transcript_filename"]
        txt_path = transcripts_dir / filename
        if not txt_path.exists():
            continue

        title = data.get("title", "").strip() or f"[Sin título] ({video_id})"
        try:
            text = txt_path.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            continue

        if not text:
            continue

        parts.append(f"{title}\n\n\n{text}\n\n")
        included += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(parts), encoding="utf-8")
    return included


def build_status_md(
    registry: dict,
    output_path: Path,
    next_check_iso: Optional[str] = None,
    estimated_completion: Optional[str] = None,
) -> None:
    """Genera el status.md legible."""
    # Asegurar que las stats están actualizadas
    from registry_utils import recompute_stats
    recompute_stats(registry)

    src = registry["source"]
    stats = registry["stats"]
    total = stats.get("total_videos", 0) or 1
    downloaded = stats.get("downloaded", 0)
    pct = (downloaded / total * 100) if total else 0

    is_complete = (
        stats.get("pending", 0) == 0 and stats.get("failed_retriable", 0) == 0
    )

    lines = []
    if is_complete:
        lines.append("# ✅ HARVEST COMPLETO\n")
    else:
        lines.append("# 🔄 Harvest en progreso\n")

    lines.append(f"**Tipo:** {src.get('type', 'desconocido')}")
    lines.append(f"**Nombre:** {src.get('name', 'Desconocido')}")
    lines.append(f"**URL:** {src.get('url', '')}")
    lines.append(f"**Slug:** `{src.get('slug', '')}`\n")

    lines.append("## Estadísticas\n")
    lines.append(f"| Métrica | Valor |")
    lines.append(f"|---|---|")
    lines.append(f"| Total de vídeos detectados | {stats.get('total_videos', 0)} |")
    lines.append(f"| Descargados con éxito | {downloaded} ({pct:.1f}%) |")
    lines.append(f"| Pendientes | {stats.get('pending', 0)} |")
    lines.append(f"| Reintentables (failed_retriable) | {stats.get('failed_retriable', 0)} |")
    lines.append(f"| Sin transcripción disponible | {stats.get('no_transcript_available', 0)} |")
    lines.append(f"| Fallos permanentes | {stats.get('failed_permanent', 0)} |\n")

    lines.append("## Tiempos\n")
    lines.append(f"- **Primera ejecución:** {src.get('first_harvest', 'N/A')}")
    lines.append(f"- **Última ejecución:** {src.get('last_harvest', 'N/A')}")
    lines.append(f"- **Última comprobación incremental:** {src.get('last_incremental_check', 'N/A')}")
    if next_check_iso:
        lines.append(f"- **Próxima comprobación incremental prevista:** {next_check_iso}")
    if estimated_completion and not is_complete:
        lines.append(f"- **Estimación de completitud:** {estimated_completion}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
