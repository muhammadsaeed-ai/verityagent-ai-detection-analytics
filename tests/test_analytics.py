import pandas as pd
import pytest

from analytics import build_event_log, object_counts, summary


def sample_frame():
    return pd.DataFrame([
        {"timestamp": "00:00:01", "frame": 1, "object_id": 1, "label": "car", "confidence": 0.9},
        {"timestamp": "00:00:02", "frame": 2, "object_id": 2, "label": "person", "confidence": 0.8},
        {"timestamp": "00:00:03", "frame": 3, "object_id": 1, "label": "car", "confidence": 0.95},
    ])


def test_confidence_filter():
    events = build_event_log(sample_frame(), 0.9)
    assert len(events) == 2


def test_object_counts():
    events = build_event_log(sample_frame())
    counts = object_counts(events)
    assert counts["car"] == 2
    assert counts["person"] == 1


def test_summary():
    events = build_event_log(sample_frame())
    report = summary(events)
    assert report["total_events"] == 3
    assert report["unique_objects"] == 2


def test_invalid_threshold():
    with pytest.raises(ValueError):
        build_event_log(sample_frame(), 1.5)
