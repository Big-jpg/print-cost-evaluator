# 3D Print Cost Evaluator - Project Summary

## Overview

The **3D Print Cost Evaluator** is a Streamlit web application designed to help creators selling third-party 3D prints estimate the **true cost** of printing a model, including material, energy, and human effort costs.

## GitHub Repository

**Repository URL:** [https://github.com/Big-jpg/print-cost-evaluator](https://github.com/Big-jpg/print-cost-evaluator)

## Features Implemented

### Core Functionality

1. **Model Input**
   - Model name (optional)
   - Reference URL (optional, for MakerWorld/Thingiverse links)
   - Filament used (grams)
   - Print time (hours)
   - Number of plates
   - Sale price

2. **Environment & Preferences (Sidebar)**
   - Filament price per kg
   - Electricity price per kWh
   - Printer power consumption (W)
   - Labour rate per hour
   - Prep time (minutes)
   - Cleanup time (minutes)
   - Plate change time per plate (minutes)
   - Remote check time per hour (minutes)
   - Automation setup (checkbox)
   - Automated plate capacity

3. **Cost Breakdown**
   - **Material cost**: Based on filament weight and price per kg
   - **Energy cost**: Based on print time, printer power, and electricity price
   - **Labour cost**: Includes prep, cleanup, plate changes, and remote monitoring
   - **Total cost**: Sum of all costs
   - **Profit**: Sale price minus total cost
   - **Profit margin**: Percentage profit relative to sale price

4. **Remote-Friendly Indicator**
   - Shows whether the job can run unattended based on:
     - Single plate jobs (always remote-friendly)
     - Multi-plate jobs with automation (remote-friendly if within automation capacity)

5. **Target Margin Calculator (Optional)**
   - Input a target profit margin percentage
   - Get a recommended sale price to achieve that margin

## Technical Implementation

### File Structure

```
print-cost-evaluator/
├── app.py                  # Main Streamlit application
├── cost_model.py          # Pure cost calculation functions
├── requirements.txt       # Python dependencies
├── test_calculations.py   # Test script to verify calculations
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
└── PROJECT_SUMMARY.md    # This file
```

### Cost Model Formulas

#### Material Cost
```
filament_kg = filament_grams / 1000
material_cost = filament_kg × filament_price_per_kg
```

#### Energy Cost
```
printer_power_kw = printer_power_watts / 1000
energy_cost = print_time_hours × printer_power_kw × electricity_price_per_kwh
```

#### Labour Cost
```
base_human_minutes = prep_time_minutes + cleanup_time_minutes

# Plate change calculation
if has_automation:
    if plate_count <= automated_plate_capacity:
        plate_change_minutes = 0
    else:
        extra_plate_changes = plate_count - automated_plate_capacity
        plate_change_minutes = extra_plate_changes × plate_change_time_minutes
else:
    extra_plate_changes = max(plate_count - 1, 0)
    plate_change_minutes = extra_plate_changes × plate_change_time_minutes

remote_check_minutes = remote_check_minutes_per_hour × print_time_hours
total_human_minutes = base_human_minutes + plate_change_minutes + remote_check_minutes
total_human_hours = total_human_minutes / 60
labour_cost = total_human_hours × labour_rate_per_hour
```

#### Total Cost and Profit
```
total_cost = material_cost + energy_cost + labour_cost
profit = sale_price - total_cost
profit_margin_percent = (profit / sale_price) × 100
```

#### Remote-Friendly Flag
```
remote_friendly = (plate_count == 1) OR 
                  (has_automation AND plate_count <= automated_plate_capacity)
```

#### Recommended Price for Target Margin
```
target_margin = target_margin_percent / 100
recommended_sale_price = total_cost / (1 - target_margin)
```

## Test Results

The application was tested with the example case from the requirements:

**Test Inputs:**
- Filament: 83 g
- Print time: 5.4 h
- Plates: 1
- Sale price: $40.00
- Filament price: $25.00/kg
- Electricity: $0.30/kWh
- Printer power: 250 W
- Labour rate: $30/h
- Prep: 10 min
- Cleanup: 10 min
- Plate change: 5 min
- Remote check: 2 min/hour
- No automation

**Test Results:**
- Material cost: **$2.08** ✅
- Energy cost: **$0.41** ✅
- Labour cost: **$15.40** ✅
- Total cost: **$17.88** ✅
- Profit: **$22.12** ✅
- Profit margin: **55.3%** ✅
- Remote-friendly: **✅ Yes** (single plate)

All calculations match the expected values from the requirements document.

## Running the Application

### Installation

```bash
pip install -r requirements.txt
```

### Running Locally

```bash
streamlit run app.py
```

Then open the URL shown in your terminal (usually http://localhost:8501).

### Running Tests

```bash
python3 test_calculations.py
```

## Technology Stack

- **Python 3.11+**
- **Streamlit 1.36+** - Web framework
- **Dataclasses** - For structured data models

## Future Enhancements (Not in v1)

The requirements document identified several stretch goals for future iterations:

1. **3MF metadata import** - Upload Bambu Studio `.3mf` files and extract metadata
2. **Scenario comparison** - Clone configurations and compare side-by-side
3. **Batch mode** - Evaluate multiple models and sort by margin/return
4. **Shareable links** - Encode configuration in URL query parameters

## Deployment Options

The application can be deployed to:

1. **Streamlit Cloud** (recommended for easy sharing)
2. **Docker container**
3. **Any Python hosting service** (Heroku, Railway, etc.)

## License

This project is provided as-is for personal and commercial use.

## Repository Information

- **Owner:** Big-jpg
- **Repository:** print-cost-evaluator
- **URL:** https://github.com/Big-jpg/print-cost-evaluator
- **Visibility:** Public
- **Default Branch:** master
