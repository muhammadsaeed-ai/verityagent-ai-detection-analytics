from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_COLUMNS = {"timestamp", "frame", "label", "confidence"}


def load_detections(path: str | Path) -> pd.DataFrame:
    """Load detector output from a JSON array or JSON-lines file."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Detection file not found: {source}")

    text = source.read_text(encoding="utf-8").strip()
    if not text:
        return pd.DataFrame(columns=sorted(REQUIRED_COLUMNS))

    try:
        data: Any = json.loads(text)
    except json.JSONDecodeError:
        data = [json.loads(line) for line in text.splitlines() if line.strip()]

    if isinstance(data, dict):
        data = data.get("detections", [])
    if not isinstance(data, list):
        raise ValueError("Detection input must be a JSON array or an object containing 'detections'.")

    frame = pd.DataFrame(data)
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required detection fields: {', '.join(sorted(missing))}")

    frame["confidence"] = pd.to_numeric(frame["confidence"], errors="coerce")
    frame["frame"] = pd.to_numeric(frame["frame"], errors="coerce").fillna(0).astype(int)
    frame["label"] = frame["label"].astype(str).str.strip()
    frame["timestamp"] = frame["timestamp"].astype(str)
    return frame


def build_event_log(detections: pd.DataFrame, confidence_threshold: float = 0.0) -> pd.DataFrame:
    """Normalize detector output into an analytics-ready event log."""
    if not 0.0 <= confidence_threshold <= 1.0:
        raise ValueError("confidence_threshold must be between 0 and 1.")

    events = detections.copy()
    events = events[events["confidence"].fillna(0) >= confidence_threshold]
    events = events.reset_index(drop=True)
    events["event_id"] = range(1, len(events) + 1)
    return events


def object_counts(events: pd.DataFrame) -> pd.Series:
    """Return detection counts grouped by object label."""
    if "label" not in events.columns:
        raise ValueError("Event log must contain a 'label' column.")
    return events["label"].value_counts().sort_index()


def summary(events: pd.DataFrame) -> dict[str, Any]:
    """Build a JSON-serializable summary of the event log."""
    counts = object_counts(events)
    return {
        "total_events": int(len(events)),
        "unique_objects": int(events["object_id"].nunique()) if "object_id" in events else 0,
        "object_counts": {str(k): int(v) for k, v in counts.items()},
        "average_confidence": round(float(events["confidence"].mean()), 4) if len(events) else 0.0,
    }


def export_csv(events: pd.DataFrame, path: str | Path) -> None:
    """Export the event log as CSV."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(destination, index=False)


def export_summary(data: dict[str, Any], path: str | Path) -> None:
    """Export analytics summary as formatted JSON."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(data, indent=2), encoding="utf-8")
