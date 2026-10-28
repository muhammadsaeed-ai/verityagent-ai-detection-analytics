from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "sample_data" / "detections.json"
DEFAULT_CSV = BASE_DIR / "outputs" / "detection_events.csv"
DEFAULT_JSON = BASE_DIR / "outputs" / "detection_summary.json"

SUPPORTED_FIELDS = {
    "timestamp",
    "frame",
    "object_id",
    "label",
    "confidence",
    "x1",
    "y1",
    "x2",
    "y2",
}
