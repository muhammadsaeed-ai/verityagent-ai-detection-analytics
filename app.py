from __future__ import annotations

import argparse

from analytics import build_event_log, export_csv, export_summary, load_detections, summary
from config import DEFAULT_CSV, DEFAULT_INPUT, DEFAULT_JSON


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Turn object-detector output into an event log, CSV report, and summary."
    )
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to detector JSON output.")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Path for the CSV event report.")
    parser.add_argument("--json", default=str(DEFAULT_JSON), help="Path for the JSON summary.")
    parser.add_argument("--confidence", type=float, default=0.0, help="Minimum confidence from 0 to 1.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    detections = load_detections(args.input)
    events = build_event_log(detections, args.confidence)
    report = summary(events)
    export_csv(events, args.csv)
    export_summary(report, args.json)

    print(f"[INFO] Loaded detections: {len(detections)}")
    print(f"[INFO] Events after filtering: {len(events)}")
    print(f"[INFO] CSV report: {args.csv}")
    print(f"[INFO] JSON summary: {args.json}")
    print("[INFO] Object counts:")
    for label, count in report["object_counts"].items():
        print(f"  - {label}: {count}")


if __name__ == "__main__":
    main()
