# Quickstart: Unified Compliance Engine

## Overview
Automated rule extraction and BIM validation pipeline.

## API Endpoints (cURL samples)

### 1. Ingest PDF Document
```bash
curl -X POST http://localhost:8000/api/v1/compliance/ingest \
  -F "file=@bep.pdf"
```

### 2. Run Compliance Check
```bash
curl -X POST http://localhost:8000/api/v1/compliance/check \
  -F "file=@model.ifc" \
  -F "rule_set_ids=[\"obc_part9\"]"
```

### 3. Export BCF
```bash
curl http://localhost:8000/api/v1/compliance/checks/{id}/bcf
```

## Frontend Integration
The feature resides in `apps/web/features/compliance/`. Use the `IngestionView` and `RuleSetSelector` components to interact with the engine.
State is managed via `useBIMStore` with specific compliance fields.
