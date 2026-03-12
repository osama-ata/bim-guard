# API Contracts: Unified Compliance Engine

**Branch**: `003-unified-compliance-engine` | **Date**: 2026-03-11

## Endpoints

### 1. `POST /api/v1/ingest`
Ingegests a PDF and returns AI-extracted rule candidates.

**Request**: Multipart File (PDF)  
**Response**: `200 OK`
```json
{
  "document_id": "uuid",
  "rules": [
    {
      "temp_id": "r-1",
      "category": "IfcWall",
      "type": "NOMENCLATURE",
      "logic": { "pattern": "W-[0-9]+" },
      "confidence": 0.92,
      "source_text": "All walls must follow W-### format."
    }
  ]
}
```

### 2. `POST /api/v1/compliance/check`
Triggers full metadata and spatial validation.

**Request**:
```json
{
  "model_id": "uuid",
  "rule_ids": ["uuid-1", "uuid-2"]
}
```
**Response**: `202 Accepted` (Task ID for async processing)

### 3. `GET /api/v1/compliance/results/{model_id}`
Returns all detected issues.

**Response**: `200 OK`
```json
{
  "summary": { "critical": 5, "warnings": 12, "passed": 140 },
  "issues": [
    {
      "id": "ISSUE-001",
      "type": "CLEARANCE_VIOLATION",
      "element_id": "3lKj89...2k",
      "description": "Halo (0.5m) intersects with Wall-X",
      "viewpoint": { "position": [1,2,3], "target": [0,0,0] }
    }
  ]
}
```

### 4. `GET /api/v1/compliance/export/bcf/{model_id}`
Generates and downloads the BCF report.

**Response**: `200 OK` (binary/zip stream)
