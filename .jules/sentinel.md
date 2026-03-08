## 2024-05-15 - Information Leakage in Error Responses
**Vulnerability:** The API endpoints were directly passing exception details (`str(e)`) to the client inside HTTP 500 error responses (e.g., in `analyze.py` and `rules.py`).
**Learning:** Returning unhandled exception strings directly to the client can leak internal system details, library versions, database connection info, or stack traces, which could be used by attackers to understand the internal workings of the backend system.
**Prevention:** Catch exceptions and log the detailed error internally (`logger.error()`), but return generic, safe error messages to the client (e.g., "An internal error occurred").
