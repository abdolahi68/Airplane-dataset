# Flight Data Caching (OpenSky)

A tiny, reliable pipeline that **fetches live aircraft positions** from the OpenSky Network and **caches them into timestamped JSON files** for later analysis, visualization, or teaching demos.

This repository contains two Python modules:

- `flight_caching.py` — the periodic cacher (writes timestamped JSON snapshots)  
- `airplane_data_fetcher.py` — the API client (fetches/parses OpenSky data)

---

## ✨ Features

- Pulls live flight states from OpenSky’s public endpoint (`/api/states/all`).
- Converts each record into a simple object (`id`, `latitude`, `longitude`).
- Writes timestamped JSON snapshots under a cache directory.
- Runs on a fixed interval (default: every 60s) until you press `Ctrl+C`.

---

## 🗂️ Repository Structure

```
.
├── airplane_data_fetcher.py   # Fetches live flight data from OpenSky
├── flight_caching.py          # Runs the periodic fetch → JSON cache
└── flight_data_cache/         # (Created at runtime) JSON snapshots live here
```

---

## 🚀 Quick Start

### 1) Requirements
- Python 3.9+ (Linux/Mac/Windows)
- `pip` for installing dependencies

### 2) (Recommended) Create a virtual environment
```bash
python -m venv .venv
# On Linux/Mac:
source .venv/bin/activate
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```
If you don’t have a `requirements.txt` yet, create one with at least:
```
requests>=2.31.0
```

### 4) Run the cacher
```bash
python flight_caching.py
```
You should see logs about successful fetches and saved JSON files. Press **Ctrl+C** to stop.

---

## ⚙️ Configuration

Open `flight_caching.py` and adjust the constants near the top:

- `FETCH_INTERVAL` — seconds between fetches (default: `60`)
- `CACHE_DIRECTORY` — where to store JSON files (default: `flight_data_cache`)

The script will create `CACHE_DIRECTORY` if it doesn’t exist.

---

## 📦 Including Your Existing Dataset (>100 samples)

If you already have 100+ JSON snapshots, place them under `flight_data_cache/` so the structure stays consistent.

**Option A: Commit a small sample and ignore the rest**
```gitignore
# Python venv & cache
.venv/
__pycache__/
*.pyc

# Local data (untracked)
flight_data_cache/
.env
```

**Option B: Track all snapshots with Git LFS**
```bash
git lfs install
echo "flight_data_cache/*.json filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
git add .gitattributes flight_data_cache/
git commit -m "Track dataset with Git LFS"
```

---

## 🧾 Data Format

Each snapshot is a JSON array of objects like:
```json
[
  { "id": "airplane_0", "latitude": 48.4284, "longitude": -123.3656 },
  { "id": "airplane_1", "latitude": 47.6218, "longitude": -122.3516 }
]
```

Notes:
- Entries are included only when both `latitude` and `longitude` exist.
- `id` is assigned sequentially per fetch (e.g., `airplane_0`, `airplane_1`, …).

---
