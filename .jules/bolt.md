## 2026-03-07 - Python Backend Disk I/O Bottleneck on IFC Processing
**Learning:** `ifcopenshell.open()` works directly on files, which means processing an uploaded file stream requires temporarily writing the byte content to disk before reading it back in. This extra disk I/O step introduces a significant and unnecessary performance penalty.
**Action:** When accepting an IFC file over a network stream, decode it (handling common `utf-8` and legacy `latin-1` encodings) and use `ifcopenshell.file.from_string(content_str)` to parse directly from memory.
