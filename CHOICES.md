
YOLOv8n was selected because it provides fast inference while maintaining sufficient accuracy for person detection in retail environments.

### Tracking Model

ByteTrack was selected due to its ability to maintain consistent customer identities across frames and handle occlusions effectively.

## Schema Design

The event schema follows a JSONL format where each line represents a single retail event.

Key fields:

* event_id
* store_id
* camera_id
* visitor_id
* event_type
* timestamp
* zone_id
* dwell_ms
* confidence

This schema supports:

* Zone analytics
* Customer journeys
* Dwell analysis
* Funnel analytics

## API Architecture

The API follows a REST-based architecture.

Endpoints:

* /metrics
* /conversion
* /brands
* /funnel

Benefits:

* Simple integration
* Easy dashboard consumption
* OpenAPI documentation support
* Scalable analytics layer

## Analytics Design

Analytics are computed from event logs and transaction data.

Generated insights:

* Visitor counts
* Zone popularity
* Dwell time
* Conversion rates
* Revenue metrics
* Brand performance
* Product performance
* Heatmaps
