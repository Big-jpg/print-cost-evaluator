# UI Features Guide - 3D Print Cost Evaluator

## Quick Reference: What's New and Where to Find It

This guide highlights the key UI/UX improvements and how to use them effectively.

---

## 🎨 Visual Design Improvements

### Color-Coded Status System

The app now uses intuitive color coding to help you quickly assess profitability:

- **🟢 Green (Healthy)** - Model meets or exceeds your target margin
- **🟠 Orange (Low Margin)** - Model is profitable but below target margin
- **🔴 Red (Losing Money)** - Model is priced below cost

**Where you'll see it:**
- Status banners at the top of results
- Portfolio table row backgrounds
- Alert messages and warnings

---

## 📱 Sidebar Organization

### New Collapsible Sections

The sidebar is now organized into logical groups that you can expand/collapse:

#### 💰 Material & Energy Costs
- Filament price per kg
- Electricity rate
- Printer power consumption

#### 👤 Labour & Time
- Your hourly labour rate
- Prep time per job
- Cleanup time per job
- Plate change time
- Remote monitoring time

#### 🤖 Automation
- Enable/disable automation checkbox
- Automation capacity (if enabled)

#### 📊 Pricing Guidance
- Target healthy margin percentage
- Used to classify models and suggest pricing

**Pro Tip:** Hover over the ℹ️ icons for helpful explanations of each setting.

---

## 📋 Single Model Analysis

### Step-by-Step Workflow

#### 1. Model Details Section
Enter basic information about your model:
- **Model name** - Give it a memorable name (optional)
- **Reference URL** - Link to MakerWorld/Thingiverse (optional)

#### 2. Print Specifications
Enter the data from your slicer:
- **Filament (g)** - Total filament weight
- **Print time (h)** - Total print duration
- **Plates** - Number of build plates needed
- **Sale price ($)** - Your intended selling price

#### 3. Calculate
Click the big **🧮 Calculate Costs** button to see results.

### Results Display

#### Status Banner
A prominent colored banner shows your profitability status at a glance.

#### Financial Summary (4 Metrics)
- **Total Cost** - Sum of all costs
- **Sale Price** - Your asking price
- **Profit** - How much you'll make (or lose)
- **Margin** - Profit as a percentage

#### Cost Breakdown
- **Visual chart** - Bar chart showing material, energy, and labour costs
- **Detailed breakdown** - Formulas showing how each cost was calculated

#### Pricing Guidance (3 Columns)
- **Break-even Price** - Minimum price to cover costs (0% margin)
- **Healthy Price** - Recommended price for your target margin
- **Remote-friendly** - Whether the job can run unattended

#### Summary
A plain-language explanation of the analysis with actionable recommendations.

#### Export
Download a complete cost report as CSV for your records.

---

## 📊 Portfolio Analysis

### 4-Step Process

#### Step 1: Get Template
- View the example CSV format in the table
- Click **📥 Download Template** to get a starter file

#### Step 2: Upload Your Portfolio
- Fill in the template with your models
- Upload the completed CSV file

**Required columns:**
- `model_name` - Name of the model
- `filament_grams` - Filament weight
- `print_time_hours` - Print duration
- `plate_count` - Number of plates
- `sale_price` - Your selling price
- `reference_url` - (optional) Link to model

#### Step 3: Review Results

**Portfolio Overview (5 Metrics):**
- Total Models
- Healthy count (with percentage)
- Low Margin count (with percentage)
- Losing Money count (with percentage)
- Average Margin across portfolio

**Status Distribution Chart:**
Visual bar chart showing the health of your portfolio.

**Detailed Results Table:**
Color-coded table with all models and their calculations.

**Portfolio Insights (Expandable):**
Automated analysis highlighting:
- Which models are losing money (by name)
- How many have low margins
- Best margin model
- Best profit-per-hour model
- How many can run remotely

#### Step 4: Export Report
Download the full portfolio analysis as CSV.

---

## 💡 Key Features Explained

### Progressive Disclosure

Information is revealed progressively to avoid overwhelming you:

1. **Before calculation** - Only input fields are shown
2. **After calculation** - Full results appear
3. **Expanders** - Detailed info hidden until you need it

### Contextual Help

Every input has help available:
- **Tooltips** - Hover over ℹ️ icons
- **Placeholders** - Example values in input fields
- **Help text** - Explanations under complex settings

### Smart Defaults

The app comes pre-configured with reasonable defaults:
- Filament: $25/kg
- Electricity: $0.30/kWh
- Printer power: 250W
- Labour rate: $30/hour
- Target margin: 20%

Adjust these in the sidebar to match your situation.

### Empty States

Helpful prompts guide you when sections are empty:
- "👆 Enter your model details above and click Calculate Costs"
- "👆 Upload a CSV file to analyze your portfolio"

### Actionable Warnings

The app provides specific guidance, not just alerts:

**Instead of:** "Low margin"  
**You get:** "💭 Consider pricing at $45.00+ for better margins"

**Instead of:** "Losing money"  
**You get:** "⚠️ You're losing $5.23 on this print. Minimum price should be $22.65 to break even."

---

## 🎯 Common Use Cases

### Use Case 1: Quick Price Check
**Goal:** Check if a model is profitable at a given price

1. Enter model specs from slicer
2. Enter your intended sale price
3. Click Calculate
4. Look at the status banner (green = good, red = bad)

**Time:** < 1 minute

---

### Use Case 2: Find Optimal Price
**Goal:** Determine what price to charge for a healthy margin

1. Enter model specs
2. Enter a placeholder sale price (e.g., $0)
3. Click Calculate
4. Look at the "Healthy Price" metric
5. Use that as your minimum price

**Time:** < 2 minutes

---

### Use Case 3: Portfolio Optimization
**Goal:** Identify which models in your catalog need repricing

1. Export your model list to CSV
2. Add specs for each model
3. Upload to Portfolio tab
4. Review the Portfolio Insights
5. Focus on models flagged as "Losing money" or "Low margin"

**Time:** 5-10 minutes for setup, instant analysis

---

### Use Case 4: Automation ROI
**Goal:** See if automation would make more models remote-friendly

1. Analyze a multi-plate model without automation
2. Note the "Remote-friendly: ❌ No" status
3. Enable automation in sidebar
4. Set automation capacity
5. Recalculate
6. See if status changes to "✅ Yes"

**Time:** < 3 minutes

---

## 📐 Understanding the Calculations

### Material Cost
```
Filament (kg) = Filament (g) ÷ 1000
Material Cost = Filament (kg) × Price per kg
```

**Example:** 83g @ $25/kg = 0.083kg × $25 = **$2.08**

---

### Energy Cost
```
Printer Power (kW) = Printer Power (W) ÷ 1000
Energy Cost = Print Time (h) × Power (kW) × Electricity Rate ($/kWh)
```

**Example:** 5.4h × 0.25kW × $0.30/kWh = **$0.41**

---

### Labour Cost
```
Base Time = Prep + Cleanup
Plate Change Time = Extra Plates × Time per Change
Remote Monitoring = Print Hours × Minutes per Hour
Total Human Time = Base + Plate Changes + Monitoring
Labour Cost = Total Hours × Hourly Rate
```

**Example:** 
- Base: 10 + 10 = 20 min
- Plate changes: 0 (single plate)
- Monitoring: 5.4h × 2 min/h = 10.8 min
- Total: 30.8 min = 0.513h
- Cost: 0.513h × $30/h = **$15.40**

---

### Total Cost & Profit
```
Total Cost = Material + Energy + Labour
Profit = Sale Price - Total Cost
Margin (%) = (Profit ÷ Sale Price) × 100
```

**Example:** 
- Total: $2.08 + $0.41 + $15.40 = **$17.89**
- Profit: $40 - $17.89 = **$22.11**
- Margin: ($22.11 ÷ $40) × 100 = **55.3%**

---

## 🚀 Pro Tips

### Tip 1: Save Your Settings
Your sidebar settings persist during your session. Set them once and analyze multiple models without re-entering.

### Tip 2: Use Portfolio for Comparisons
Even if you only have 2-3 models, portfolio mode makes it easy to compare them side-by-side.

### Tip 3: Experiment with Margins
Try different target margins (10%, 20%, 30%) to see how they affect recommended pricing.

### Tip 4: Account for Shipping
If you charge shipping separately, don't include it in the sale price. If shipping is included, add it to the sale price.

### Tip 5: Remote-Friendly Matters
Remote-friendly jobs have lower labour costs (no plate changes). This can significantly impact profitability for multi-plate prints.

### Tip 6: Export Everything
Download cost reports for your records. They're useful for:
- Tax documentation
- Business planning
- Client quotes
- Historical tracking

---

## 🔧 Troubleshooting

### "My profit is negative!"
**Solution:** Look at the "Break-even Price" - that's your minimum. Price at or above the "Healthy Price" for sustainable margins.

### "The CSV upload failed"
**Solution:** Make sure your CSV has all required columns with exact names (case-sensitive). Download the template to see the correct format.

### "Remote-friendly shows No but I have automation"
**Solution:** Check that:
1. Automation checkbox is enabled in sidebar
2. Plate count ≤ Automation capacity
3. You've recalculated after changing settings

### "Labour cost seems too high"
**Solution:** Check your labour rate and time settings in the sidebar. Remote monitoring time can add up on long prints - set it to 0 if you don't monitor.

### "I want to see more decimal places"
**Solution:** Download the CSV export - it contains full precision values.

---

## 📚 Additional Resources

### Files in This Project
- **README.md** - Installation and basic usage
- **UX_IMPROVEMENTS.md** - Detailed design decisions and rationale
- **UI_FEATURES_GUIDE.md** - This file (user-facing guide)
- **app.py** - Main application code
- **cost_model.py** - Calculation logic
- **test_calculations.py** - Automated tests

### Getting Help
- Check the expandable "How to use" sections in each tab
- Hover over ℹ️ icons for field-specific help
- Review the example data in templates
- Examine the narrative summary for plain-language explanations

---

## 🎓 Learning Path

### Beginner (First Time User)
1. Read the "How to use" expander in Single Model tab
2. Try the example values (already filled in)
3. Click Calculate and explore the results
4. Adjust one value and recalculate to see the impact

### Intermediate (Regular User)
1. Customize sidebar settings to match your costs
2. Analyze your actual models from slicer data
3. Use the Healthy Price guidance for pricing decisions
4. Export reports for your records

### Advanced (Power User)
1. Create a portfolio CSV of your entire catalog
2. Use insights to identify repricing opportunities
3. Experiment with automation settings for ROI analysis
4. Track changes over time by comparing exported reports

---

## ✨ Final Notes

This tool is designed to **guide your pricing decisions**, not make them for you. Use it to:

✅ Understand your true costs  
✅ Set sustainable prices  
✅ Identify unprofitable models  
✅ Optimize your product mix  
✅ Make data-driven business decisions  

The UI improvements focus on making this information **clear, actionable, and accessible** so you can focus on growing your 3D printing business.

Happy printing! 🖨️
