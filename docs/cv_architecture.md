# Workload Vision Agent Architecture (Computer Vision Monitor)

## Innovation Thesis
Traditional APM monitoring relies purely on time-series telemetry (e.g. Prometheus metrics or ELK logs). The APEX platform pioneers **Visual Anomaly Detection**, taking periodic "screenshots" of human-readable Application Insights or Grafana dashboards.

> This guarantees that APEX catches exactly what an operator would catch visually, bridging the semantic gap between pure metrics and human-understandable visual UI patterns.

## Architecture

### 1. The Metric Analyzer (`agents/workload_vision/metric_analyzer.py`)
- Employs **OpenCV (opencv-python)** to ingest and preprocess dashboard JPEGs/PNGs.
- Extracts spatial sub-domains (e.g. identifying bounding boxes for line charts vs gauges).
- Applies **Tesseract OCR (pytesseract)** to extract numerical values precisely from the GUI.

### 2. Autoencoder Anomaly Detection (`agents/workload_vision/vision_models.py`)
- Utilizes deep Convolutional Autoencoders written in **PyTorch**.
- **The Catch**: The model is trained exclusively on "Normal" dashboard operations. When fed an image of an exploding query pipeline graph, the model fails to reconstruct the wild spike. The resulting **Mean Squared Error (MSE) loss** spikes above our statistical threshold, instantly flagging an anomaly.

### 3. Agent Integration (`agents/workload_vision/agent.py`)
- Fuses the OCR numbers and the PyTorch localized graph error into a unified JSON verdict.
- Emits Alerts via the MCP `Alerts Server` the millisecond an anomaly triggers visual divergence.
