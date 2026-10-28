from __future__ import annotations

import pandas as pd
import streamlit as st

from analytics import build_event_log, load_detections, object_counts, summary
from config import DEFAULT_INPUT

st.set_page_config(page_title="AI Detection Analytics", page_icon="📊", layout="wide")

st.title("📊 AI Detection Analytics")
st.caption("VerityAgent Python AI Mini Projects — Project #08")

uploaded = st.file_uploader("Upload detector output (JSON or JSONL)", type=["json", "jsonl"])
threshold = st.sidebar.slider("Minimum confidence", 0.0, 1.0, 0.0, 0.05)

if uploaded is not None:
    raw = uploaded.getvalue().decode("utf-8")
    import tempfile
    from pathlib import Path

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp.write(raw.encode("utf-8"))
        input_path = Path(tmp.name)
else:
    input_path = DEFAULT_INPUT

try:
    detections = load_detections(input_path)
    events = build_event_log(detections, threshold)
except (FileNotFoundError, ValueError) as exc:
    st.info(f"Upload detector output or add sample data to `{DEFAULT_INPUT}`.")
    st.error(str(exc))
    st.stop()

report = summary(events)
counts = object_counts(events)

col1, col2, col3 = st.columns(3)
col1.metric("Total detections", report["total_events"])
col2.metric("Unique objects", report["unique_objects"])
col3.metric("Average confidence", f"{report['average_confidence']:.2%}")

left, right = st.columns(2)
with left:
    st.subheader("Objects by class")
    st.bar_chart(counts)

with right:
    st.subheader("Detection events over time")
    if not events.empty:
        time_series = events.groupby("timestamp").size().rename("events")
        st.line_chart(time_series)
    else:
        st.info("No events match the selected confidence threshold.")

st.subheader("Event log")
st.dataframe(events, use_container_width=True, hide_index=True)

csv_data = events.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV report", csv_data, "detection_events.csv", "text/csv")
