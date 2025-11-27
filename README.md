# 3D Print Cost Evaluator (Streamlit)

A small Streamlit webapp to estimate the true cost of 3D-printed models.

## Features

- Input model data (filament grams, print time, plate count, sale price)
- Configure environment & preferences (filament cost, power, labour rate, automation)
- Get a full breakdown of:
  - Material cost
  - Energy cost
  - Labour cost (prep, cleanup, plate changes, remote checks)
  - Total cost, profit, and profit margin
  - Remote-friendliness flag (can the job run mostly unattended?)

## Installation

```bash
pip install -r requirements.txt
```

## Running the app

```bash
streamlit run app.py
```

Then open the URL shown in your terminal (usually http://localhost:8501).

## File overview

- `app.py`         — Streamlit UI and wiring
- `cost_model.py`  — Pure cost calculation logic
- `requirements.txt` — Python dependencies
- `README.md`      — This file
