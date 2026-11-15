---
paths:
  - "app/routers/**/*.py"
---
# Router Layer Rules (`app/routers/`)

1. **Thin Orchestration Only**: Routers parse HTTP/multipart/base64 inputs, call functions in `app/services/`, and return frozen Pydantic models from `app/models/schemas.py`.
2. **No Direct SDK Imports**: Never import `google.genai`, `google.generativeai`, or `pymongo` in router modules.
3. **Boundary Validation**:
   - Validate base64 payloads with `base64.b64decode(..., validate=True)` and raise `HTTPException(status_code=400, ...)` on malformed input or empty bytes.
   - Always declare `response_model=...` on every route decorator.
4. **Error Safety**: Never leak raw upstream SDK stack traces or credentials (`GEMINI_API_KEY`, `MONGODB_URI`) in HTTP error details.
