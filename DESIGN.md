
## System Overview

Store Intelligence Platform is an AI-powered retail analytics system that processes CCTV footage to generate actionable business insights. The solution combines computer vision, object tracking, event generation, analytics, and visualization into a unified platform.

## Architecture

### Computer Vision Layer

* YOLOv8 for person detection
* ByteTrack for multi-object tracking
* OpenCV for video processing

### Event Processing Layer

* Zone detection
* Zone entry/exit events
* Dwell time calculation
* Event logging in JSONL format

### Analytics Layer

* Visitor analytics
* Conversion analytics
* Funnel analytics
* Brand and product analytics
* Heatmap generation

### API Layer

* FastAPI REST endpoints
* Swagger/OpenAPI documentation

### Dashboard Layer

* Streamlit dashboard
* Plotly visualizations
* Exportable reports

## AI-Assisted Decisions

### YOLOv8 Selection

YOLOv8 was selected due to its strong balance of accuracy and inference speed for real-time retail analytics.

### ByteTrack Selection

ByteTrack was chosen because it maintains stable identities even during partial occlusions and crowded scenes, improving visitor tracking consistency.

### Heatmap Generation

OpenCV-based heatmap generation was selected for lightweight processing and easy visualization of customer movement patterns.

### FastAPI Selection

FastAPI was chosen for its high performance, automatic OpenAPI generation, and ease of deployment.

### Streamlit Selection

Streamlit enabled rapid development of an interactive analytics dashboard suitable for business stakeholders.
