# notify-flow

A bridge between the people who **sell** a garment and the people who **make** it.

Orders land from a Shoper shop, get translated into a model the workshop actually
thinks in — off-the-shelf or sewn to measure, which measurements, which fabric,
how much of it went — and are served over an authenticated API.

## The problem it solves

A shop's order export answers *"what was bought"*. A workshop needs *"what do we
cut, from what, and by when"*. Those are different questions, and until now the
gap was closed by someone reading one format and retyping it into another.

This service does that translation once, in one place. The seller keeps working in
Shoper; the workshop gets clean, queryable orders.

## Layers

| Layer | Owns | Knows nothing about |
|---|---|---|
| `Api/` | HTTP: routes, status codes, auth | business rules |
| `Services/` | domain rules + Shoper-specific parsing | HTTP, SQL |
| `Database/` | tables and queries | HTTP, Shoper |
| `models/` | shared vocabulary: schemas and enums | everything else |

Shop-specific knowledge (shipping ids, status codes) lives in `config/*.json`, not
in code, so it changes without a deploy. See `config/*.example.json`.

## The domain model, briefly

Two fields carry the distinction the workshop cares about, and they are
deliberately separate:

- **`product_type`** — *what was bought*. `STANDARD` (a fixed size off the shelf)
  or `MADE_TO_ORDER` (sewn to the customer's measurements). Derived once, from the
  order's size attribute, and never changes.
- **`fulfillment_path`** — *how it is being made*. `WAREHOUSE` or `PRODUCTION`.
  Mutable: a standard item drops to production when stock runs out.

Collapsing them into one field would lose the fact that an item was catalogue
stock once it moves to production — and with it, any way to see how often stock
runs short.

Material consumption is recorded after the fact, by the person who cut the fabric,
because faulty material makes the actual metrage differ from any norm.

## API

| Method | Path | Auth |
|---|---|---|
| `POST` | `/auth/register` | public — new accounts start with no permissions |
| `POST` | `/auth/login` | public — returns a bearer token |
| `GET` | `/orders` | bearer token |
| `PUT` | `/orders/{order_id}/status` | bearer token |
| `POST` | `/webhooks/shoper/orders` | `X-Webhook-Secret` header |

Passwords are hashed with Argon2id. Access tokens are JWTs, valid 15 minutes.
A new account gets the `PENDING` role and is refused everywhere until an admin
promotes it.

## Running it

```bash
cp .env.example .env          # then fill in the values
pip install -r requirements.txt
docker compose up -d db       # Postgres on :5433
uvicorn main:app --reload
```

Logs go to `logs/app.log` and, for failures only, `logs/errors.log`.

## Status

Working: order ingestion via webhook, order parsing, persistence, registration,
login, token-protected endpoints, structured logging.

Not built yet: refresh tokens (so logout cannot truly revoke a session), per-role
endpoint permissions, device limits, material stock deduction. Known security gaps
are listed in [SECURITY.md](SECURITY.md).
