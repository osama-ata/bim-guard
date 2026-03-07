## 2026-03-03 - [Prevent Information Leakage in API Responses]
**Vulnerability:** Internal error details (stack traces, paths) were leaked via `detail=str(e)` in HTTP 500 error responses in the FastAPI backend endpoints `analyze.py` and `rules.py`.
**Learning:** Returning unhandled exception strings directly to the client can expose sensitive infrastructure details or implementation logic, violating the "Fail securely" principle.
**Prevention:** Always catch exceptions and map them to generic, user-friendly error messages (e.g., `"An error occurred while processing the request."`) in public-facing API responses. Log the actual detailed error internally using a logger.
