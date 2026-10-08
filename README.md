# REST API Client (Python)

Portfolio sample: a small, production-minded REST client built on httpx.
Covers the patterns I standardize on when services talk to third-party APIs:

- Bearer-token auth with automatic refresh on 401
- Exponential-backoff retries for 429/5xx (with `Retry-After` support)
- Transparent cursor pagination (`iter_pages`)
- Typed errors so callers can branch on failure mode
- Request timeouts on every call — no hanging forever

`example_server.py` is a tiny FastAPI app (paginated `/items` endpoint with
rate limiting) so you can exercise the client locally.

## Run the demo

```bash
pip install -r requirements.txt
uvicorn example_server:app --port 8000 &
python demo.py
```

## Layout

- `client.py` — the reusable client
- `example_server.py` — FastAPI demo API
- `demo.py` — end-to-end usage example
- `tests/test_client.py` — unit tests with a mocked transport
