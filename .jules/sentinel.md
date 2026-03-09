## 2024-05-18 - Information Leakage via Error Messages
**Vulnerability:** HTTPException detail strings exposed raw exception details `str(e)` in error responses.
**Learning:** This occurred due to directly passing caught exception details to the client instead of generic error messages, leading to potential exposure of internal systems, paths, or logic (stack traces/errors).
**Prevention:** Always log the detailed error internally (`logger.error()`) and return generic error messages to the client when raising HTTPExceptions.
