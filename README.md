# AI Detection Analytics

**VerityAgent Python AI Mini Projects — Project #08**

Turn object-detector output into structured event logs, object counts, CSV reports, JSON summaries, and an interactive Streamlit dashboard.

## Features

- JSON/JSONL detector-output ingestion
- Confidence filtering
- Event-log generation
- Object counts by class
- Unique-object statistics when tracking IDs are supplied
- CSV export
- JSON summary export
- Interactive Streamlit dashboard
- Downloadable reports
- Automated unit tests

## Pipeline

```text
Object Detector Output
        ↓
   Input Validation
        ↓
 Confidence Filtering
        ↓
    Event Log (Pandas)
        ↓
 ┌──────┴─────────┐
 ↓                ↓
CSV Report    Analytics Summary
                  ↓
           Streamlit Dashboard
```

## Installation

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## CLI Usage

Process the included sample detector output:

```bash
python app.py
```

Use your own detector output:

```bash
python app.py --input path/to/detections.json
```

Apply a confidence threshold:

```bash
python app.py --input path/to/detections.json --confidence 0.5
```

Specify report locations:

```bash
python app.py --input path/to/detections.json --csv outputs/events.csv --json outputs/summary.json
```

## Dashboard

Start Streamlit:

```bash
streamlit run streamlit_app.py
```

The dashboard provides total detections, unique tracked objects when IDs are available, average confidence, object-count charts, an event timeline, an event table, and CSV download.

## Detector Output Format

The input must be a JSON array or an object containing a `detections` array. Each detection requires `timestamp`, `frame`, `label`, and `confidence`. An optional `object_id` can be supplied when the upstream detector/tracker provides persistent IDs.

Example:

```json
[
  {
    "timestamp": "00:00:01",
    "frame": 1,
    "object_id": 101,
    "label": "car",
    "confidence": 0.92
  }
]
```

## Architecture Note

This project analyzes **object-detector output**. It does not itself run an object-detection model. The analytics layer can therefore consume outputs from YOLO, Faster R-CNN, or another detector that produces the documented fields.

## Limitations

Analytics quality depends on the upstream detector and tracker. Duplicate detections, missed detections, incorrect classes, or unstable tracking IDs affect the resulting reports. The included sample data is illustrative and is not benchmark data.

## Testing

```bash
pytest -q
```

## Future Improvements

- Direct YOLO integration
- Real-time video analytics
- SQLite/PostgreSQL event storage
- Advanced time-window analytics
- Multi-camera dashboards
- Alert rules
- Excel export

## Branding

**VerityAgent** — AI Engineering & Python Projects
