# Mooneazy Signals Function

A serverless **Appwrite Function** responsible for automated market analysis, trading signal generation, database persistence, and push notification dispatching for the **Mooneazy** trading platform.

---

## 📌 Overview

This function executes on a schedule (or via HTTP trigger) to scan supported trading pairs across multiple timeframes. It identifies high-probability trading setups using quantitative rules and chart pattern strategies, records newly discovered signals in an Appwrite database, and broadcasts push notifications to subscribed users.

### Key Capabilities
- **Multi-Strategy Signal Generation:** Integrates Pullback, Breakout, Head & Shoulders, and Higher Timeframe (HTF) trend-following setups.
- **Active Signal Filtering:** Filters raw triggers to return only active, actionable signals within their valid execution window.
- **Appwrite TablesDB Persistence:** Stores signal details including entry price, stop-loss (SL), take-profit levels (TP1, TP2), direction (buy/sell), and status (`pending`/`closed`).
- **Push Notification Broadcasts:** Automatically dispatches alerts to subscribers via Appwrite Messaging.
- **Resilient Execution:** Structured exception handling with detailed error logging in the function context response.

---

## 🏗 Architecture & Flow

```
┌────────────────────────────────────────────────────────┐
│               Trigger (Cron / HTTP Request)            │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
               ┌────────────────────────┐
               │      src/main.py       │
               └────────────┬───────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Market Scan  │     │   Database   │     │ Push Alerts  │
│  (mooneazy)  │ ──► │ (TablesDB)   │ ──► │  (Messaging) │
│              │     │              │     │              │
│• Pullback    │     │• Store new   │     │• Send push   │
│• Breakout    │     │  signals     │     │  to topic    │
│• HTF Trends  │     │• Status & TPs│     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │ JSON Response & Logs     │
              └──────────────────────────┘
```

---

## 📁 Project Structure

```
.
├── src/
│   ├── main.py                     # Appwrite function entrypoint
│   ├── appwrite_api/               # Appwrite SDK integrations
│   │   ├── client.py               # Client setup and authentication
│   │   ├── db.py / signals_table.py# Signals database operations
│   │   ├── messages.py             # Push notification dispatching
│   │   ├── models.py               # Pydantic models for signal data
│   │   └── alert_models.py         # Models for push alert payloads
│   └── mooneazy/                   # Core trading engine package
│       └── mooneazy/
│           ├── scripts/            # Orchestration (scalper, analysis, config)
│           ├── candles_api/        # Market candle data fetching
│           ├── pullback_strategy/  # Pullback & Head & Shoulders logic
│           ├── breakout_strategy/  # Volume & price breakout logic
│           ├── ultimate_setups/    # HTF trend & pivot strategies
│           └── trading/            # Risk management & TP calculations
├── pyproject.toml                  # Project metadata & workspace configuration
├── requirements.txt                # Python package dependencies
└── README.md                       # Documentation
```

---

## ⚙️ Configuration & Environment Variables

Configure these environment variables in your Appwrite Function console or `.env` file:

| Variable | Description | Example / Default |
|---|---|---|
| `APPWRITE_FUNCTION_API_ENDPOINT` | Appwrite REST endpoint URL | `https://cloud.appwrite.io/v1` |
| `APPWRITE_FUNCTION_PROJECT_ID` | Appwrite project ID | `65a...` |
| `APPWRITE_FUNCTION_API_KEY` | Appwrite API key with Database & Tables permissions | `standard_api_key` |
| `PUSH_NOTIFICATIONS_API_KEYS` | Appwrite API key with Messaging write permissions | `messaging_api_key` |
| `SIGNALS_DB_ID` | Database ID containing the signals table | `trading_db` |
| `SIGNALS_TABLE_ID` | Table ID for storing signal entries | `signals` |
| `FUNCTION_ENVIRONEMENT` | Environment mode (`dev` enables testing push payloads) | `dev` / `production` |
| `ENVIRONMENT` | Execution context (e.g. `testing` plays audio alert) | `testing` / `production` |

---

## 📊 Supported Assets & Default Parameters

Defined in `src/mooneazy/mooneazy/scripts/config.py`:

- **Assets:** `BTCUSDT`, `ETHUSDT`, `XAUUSDT`
- **Execution Timeframes:** `15m`, `30m`
- **Higher Timeframe Trends (HTF):** `4h`, `1d`
- **Indicators:**
  - EMA Cross Periods: `8` (fast), `20` (slow)
  - Hull Moving Average: `55`
  - Risk/Reward Targets: `1:2` (TP1), `1:5` (TP2)

---

## 📡 API Usage & Response

When invoked inside Appwrite Function runtime:

### Request
- **Method:** `POST` or `GET`
- **Path:** `/`

### Sample Response (`200 OK`)
```json
{
  "signals": [
    {
      "time": 1727712000,
      "utc_time": "2026-09-30 16:00:00",
      "entry_price": 63450.0,
      "symbol": "BTCUSDT",
      "sl": 63100.0,
      "tp1": 64150.0,
      "tp2": 65200.0,
      "direction": "buy",
      "interval": "15m",
      "signal_type": "pullback",
      "tp1_status": "pending",
      "tp2_status": "pending",
      "status": "pending"
    }
  ],
  "errors": null
}
```

---

## 🛠 Local Setup & Development

### Prerequisites
- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or `pip`

### Installation

Using `uv`:
```bash
# Sync dependencies and workspace
uv sync
```

Using standard `pip`:
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies and local mooneazy package
pip install -r requirements.txt
```

### Running Tests
```bash
pytest
```

---

## 🚀 Deployment

This function is designed to be deployed directly to an **Appwrite** instance:

1. **Runtime:** Python 3.11
2. **Entrypoint:** `src/main.py`
3. **Build Command:** `pip install -r requirements.txt`
4. **Schedule:** `*/15 * * * *` (recommended to run on candle close every 15 minutes)
