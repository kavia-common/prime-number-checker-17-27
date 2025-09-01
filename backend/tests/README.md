# Backend Tests

This directory contains pytest test cases for the FastAPI backend.

What is covered:
- Health check endpoint: GET /
- Prime check endpoint (expected): POST /check-prime
  - Valid primes (2, 3, 5, 13, 97, 101)
  - Valid non-primes (0, 1, 4, 8, 9, 15, 100)
  - Invalid inputs (string, float, null, missing field, list, object)

Expected API for /check-prime:
- Request: JSON body {"number": <int>}
- Response: 200 OK with {"number": <int>, "is_prime": <bool>}
- Validation: Non-integer payloads should return 422 Unprocessable Entity.

Running tests:
- Ensure the backend virtualenv has the dependencies installed as per requirements.txt
- Run: `pytest -q`

Note:
- The prime-check endpoint is not currently implemented in `src/api/main.py`. 
- Tests for /check-prime will fail until that endpoint and corresponding validation are implemented.
