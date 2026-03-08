## 2026-03-08 - In-Memory IFC File Parsing
**Learning:** `ifcopenshell` can parse IFC files directly from memory strings using `ifcopenshell.file.from_string()`, avoiding the need for `tempfile` disk write/read operations that bottleneck the API under load. Note that it expects a standard `str` (decoded from bytes), not `bytes` directly.
**Action:** When handling user-uploaded IFC files in API endpoints, decode the bytes to UTF-8 strings and pass directly to `ifcopenshell.file.from_string()` rather than creating temporary files.
