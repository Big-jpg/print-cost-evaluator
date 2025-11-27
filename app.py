# app.py - 3D Print Cost Evaluator (Refined UI/UX)

import streamlit as st
import pandas as pd

from cost_model import (
    EnvironmentSettings,
    ModelInput,
    calculate_costs,
)


st.set_page_config(
    page_title="3D Print Cost Evaluator",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_session_defaults():
    """Initialize session state with sensible defaults."""
    defaults = {
        "filament_price_per_kg": 25.0,
        "electricity_price_per_kwh": 0.30,
        "printer_power_watts": 250.0,
        "labour_rate_per_hour": 30.0,
        "prep_time_minutes": 10.0,
        "cleanup_time_minutes": 10.0,
        "plate_change_time_minutes": 5.0,
        "remote_check_minutes_per_hour": 2.0,
        "has_automation": False,
        "automated_plate_capacity": 4,
        "healthy_margin_floor_percent": 20.0,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def sidebar_env_settings() -> EnvironmentSettings:
    """Render sidebar with environment settings and preferences."""
    
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Material & Energy Section
        with st.expander("💰 Material & Energy Costs", expanded=True):
            filament_price_per_kg = st.number_input(
                "Filament price ($/kg)",
                min_value=0.0,
                value=float(st.session_state["filament_price_per_kg"]),
                step=0.5,
                help="Cost per kilogram of filament material",
            )
            electricity_price_per_kwh = st.number_input(
                "Electricity rate ($/kWh)",
                min_value=0.0,
                value=float(st.session_state["electricity_price_per_kwh"]),
                step=0.05,
                help="Your local electricity cost per kilowatt-hour",
            )
            printer_power_watts = st.number_input(
                "Printer power (W)",
                min_value=0.0,
                value=float(st.session_state["printer_power_watts"]),
                step=10.0,
                help="Average power consumption of your 3D printer",
            )

        # Labour & Time Section
        with st.expander("👤 Labour & Time", expanded=True):
            labour_rate_per_hour = st.number_input(
                "Labour rate ($/hour)",
                min_value=0.0,
                value=float(st.session_state["labour_rate_per_hour"]),
                step=1.0,
                help="Your hourly rate for hands-on work",
            )
            
            st.markdown("**Time per job:**")
            prep_time_minutes = st.number_input(
                "Prep time (min)",
                min_value=0.0,
                value=float(st.session_state["prep_time_minutes"]),
                step=1.0,
                help="Time to prepare printer and start the job",
            )
            cleanup_time_minutes = st.number_input(
                "Cleanup time (min)",
                min_value=0.0,
                value=float(st.session_state["cleanup_time_minutes"]),
                step=1.0,
                help="Time to remove print and clean up",
            )
            plate_change_time_minutes = st.number_input(
                "Plate change time (min)",
                min_value=0.0,
                value=float(st.session_state["plate_change_time_minutes"]),
                step=1.0,
                help="Time needed to swap build plates",
            )
            remote_check_minutes_per_hour = st.number_input(
                "Remote monitoring (min/hour)",
                min_value=0.0,
                value=float(st.session_state["remote_check_minutes_per_hour"]),
                step=0.5,
                help="Time spent checking on prints remotely per hour of print time",
            )

        # Automation Section
        with st.expander("🤖 Automation", expanded=True):
            has_automation = st.checkbox(
                "I have plate automation (AMS/sled system)",
                value=bool(st.session_state["has_automation"]),
                help="Enable if you have automated plate changing capability",
            )
            if has_automation:
                automated_plate_capacity = st.number_input(
                    "Automation capacity (plates)",
                    min_value=1,
                    value=int(st.session_state["automated_plate_capacity"]),
                    step=1,
                    help="Maximum plates your system can handle unattended",
                )
            else:
                automated_plate_capacity = 1

        # Pricing Guidance Section
        with st.expander("📊 Pricing Guidance", expanded=True):
            healthy_margin_floor_percent = st.number_input(
                "Target healthy margin (%)",
                min_value=0.0,
                max_value=95.0,
                value=float(st.session_state["healthy_margin_floor_percent"]),
                step=5.0,
                help="Minimum profit margin you consider 'healthy' for your business",
            )
            
            st.caption("This helps classify models as losing money, low margin, or healthy.")

    # Persist to session state
    st.session_state.update({
        "filament_price_per_kg": filament_price_per_kg,
        "electricity_price_per_kwh": electricity_price_per_kwh,
        "printer_power_watts": printer_power_watts,
        "labour_rate_per_hour": labour_rate_per_hour,
        "prep_time_minutes": prep_time_minutes,
        "cleanup_time_minutes": cleanup_time_minutes,
        "plate_change_time_minutes": plate_change_time_minutes,
        "remote_check_minutes_per_hour": remote_check_minutes_per_hour,
        "has_automation": has_automation,
        "automated_plate_capacity": automated_plate_capacity,
        "healthy_margin_floor_percent": healthy_margin_floor_percent,
    })

    return EnvironmentSettings(
        filament_price_per_kg=filament_price_per_kg,
        electricity_price_per_kwh=electricity_price_per_kwh,
        printer_power_watts=printer_power_watts,
        labour_rate_per_hour=labour_rate_per_hour,
        prep_time_minutes=prep_time_minutes,
        cleanup_time_minutes=cleanup_time_minutes,
        plate_change_time_minutes=plate_change_time_minutes,
        remote_check_minutes_per_hour=remote_check_minutes_per_hour,
        has_automation=has_automation,
        automated_plate_capacity=automated_plate_capacity,
    )


def calculate_break_even_and_health(
    total_cost: float, healthy_margin_floor_percent: float
) -> tuple[float, float | None]:
    """Calculate break-even price and healthy margin price."""
    break_even_price = total_cost
    if 0 < healthy_margin_floor_percent < 100:
        m = healthy_margin_floor_percent / 100.0
        healthy_price = total_cost / (1.0 - m)
    else:
        healthy_price = None
    return break_even_price, healthy_price


def classify_model(
    sale_price: float, total_cost: float, healthy_price: float | None
) -> str:
    """Categorize a model's profitability."""
    if sale_price < total_cost:
        return "Losing money"
    if healthy_price is None:
        return "Profitable"
    if sale_price < healthy_price:
        return "Low margin"
    return "Healthy"


def get_status_color(status: str) -> str:
    """Return color for status indicators."""
    colors = {
        "Losing money": "#ff4b4b",
        "Low margin": "#ffa500",
        "Healthy": "#00cc00",
        "Profitable": "#00cc00",
    }
    return colors.get(status, "#808080")


def render_cost_breakdown_chart(breakdown):
    """Render a simple visual breakdown of costs."""
    cost_data = pd.DataFrame({
        "Category": ["Material", "Energy", "Labour"],
        "Cost ($)": [
            breakdown.material_cost,
            breakdown.energy_cost,
            breakdown.labour_cost,
        ],
    })
    
    st.bar_chart(cost_data.set_index("Category"), height=200)


# ---------------------------------------------------------------------
# Single model tab
# ---------------------------------------------------------------------
def render_single_model_tab(env_settings: EnvironmentSettings):
    """Render the single model analysis interface."""
    
    st.markdown("### 📋 Model Details")
    
    with st.expander("ℹ️ How to use", expanded=False):
        st.markdown("""
        **Quick Start:**
        1. Enter your model's specifications below
        2. Adjust settings in the sidebar if needed
        3. Click **Calculate Costs** to see the full breakdown
        
        **What you'll get:**
        - Complete cost breakdown (material, energy, labour)
        - Profit analysis at your sale price
        - Break-even and recommended pricing
        - Remote-friendly assessment
        - Downloadable cost report
        """)

    # Model identification
    col1, col2 = st.columns([2, 1])
    with col1:
        model_name = st.text_input(
            "Model name",
            value="",
            placeholder="e.g., MH-6 Little Bird Helicopter",
            help="Give this model a memorable name",
        )
    with col2:
        reference_url = st.text_input(
            "Reference URL (optional)",
            value="",
            placeholder="https://makerworld.com/...",
            help="Link to the model source",
        )

    st.markdown("---")
    st.markdown("### 🔢 Print Specifications")
    
    # Print specs in a cleaner layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filament_grams = st.number_input(
            "Filament (g)",
            min_value=0.0,
            value=83.0,
            step=1.0,
            help="Total filament weight from slicer",
        )
    
    with col2:
        print_time_hours = st.number_input(
            "Print time (h)",
            min_value=0.0,
            value=5.4,
            step=0.1,
            help="Total print duration from slicer",
        )
    
    with col3:
        plate_count = st.number_input(
            "Plates",
            min_value=1,
            value=1,
            step=1,
            help="Number of build plates needed",
        )
    
    with col4:
        sale_price = st.number_input(
            "Sale price ($)",
            min_value=0.0,
            value=40.0,
            step=1.0,
            help="Your intended selling price",
        )

    st.markdown("---")
    
    # Prominent calculate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        calculate = st.button("🧮 Calculate Costs", type="primary", use_container_width=True)

    if not calculate:
        st.info("👆 Enter your model details above and click **Calculate Costs** to see the analysis.")
        return

    # Perform calculation
    model_input = ModelInput(
        model_name=model_name or None,
        reference_url=reference_url or None,
        filament_grams=filament_grams,
        print_time_hours=print_time_hours,
        plate_count=int(plate_count),
        sale_price=sale_price,
        target_margin_percent=None,
    )

    breakdown = calculate_costs(env_settings, model_input)

    margin_text = (
        f"{breakdown.profit_margin_percent:,.1f}%"
        if breakdown.profit_margin_percent is not None
        else "N/A"
    )

    healthy_floor = float(st.session_state["healthy_margin_floor_percent"])
    break_even_price, healthy_price = calculate_break_even_and_health(
        breakdown.total_cost, healthy_floor
    )
    verdict = classify_model(sale_price, breakdown.total_cost, healthy_price)
    status_color = get_status_color(verdict)

    # Results section with visual hierarchy
    st.markdown("---")
    st.markdown("## 📊 Cost Analysis Results")
    
    # Status banner
    st.markdown(f"""
    <div style="padding: 1rem; border-radius: 0.5rem; background-color: {status_color}20; border-left: 4px solid {status_color};">
        <h3 style="margin: 0; color: {status_color};">Status: {verdict}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")  # spacing

    # Key metrics in a prominent display
    st.markdown("### 💵 Financial Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cost", f"${breakdown.total_cost:,.2f}", help="Sum of all costs")
    col2.metric("Sale Price", f"${sale_price:,.2f}", help="Your asking price")
    
    profit_delta = f"${abs(breakdown.profit):,.2f}" if breakdown.profit >= 0 else f"-${abs(breakdown.profit):,.2f}"
    col3.metric(
        "Profit", 
        f"${breakdown.profit:,.2f}",
        delta=profit_delta if breakdown.profit >= 0 else None,
        delta_color="normal" if breakdown.profit >= 0 else "inverse",
        help="Sale price minus total cost"
    )
    col4.metric("Margin", margin_text, help="Profit as % of sale price")

    st.markdown("---")
    
    # Cost breakdown
    st.markdown("### 📦 Cost Breakdown")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Visual chart
        render_cost_breakdown_chart(breakdown)
    
    with col2:
        # Detailed breakdown
        st.markdown(f"""
        **Material Cost:** ${breakdown.material_cost:,.2f}  
        ↳ {breakdown.filament_kg*1000:.1f}g @ ${env_settings.filament_price_per_kg}/kg
        
        **Energy Cost:** ${breakdown.energy_cost:,.2f}  
        ↳ {print_time_hours:.1f}h × {breakdown.printer_power_kw:.2f}kW @ ${env_settings.electricity_price_per_kwh}/kWh
        
        **Labour Cost:** ${breakdown.labour_cost:,.2f}  
        ↳ {breakdown.total_human_hours:.2f}h @ ${env_settings.labour_rate_per_hour}/h
        """)

    st.markdown("---")
    
    # Pricing guidance
    st.markdown("### 💡 Pricing Guidance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Break-even Price",
            f"${break_even_price:,.2f}",
            help="Minimum price to cover costs (0% margin)"
        )
        if sale_price < break_even_price:
            st.error("⚠️ Current price is below break-even!")
    
    with col2:
        if healthy_price is not None:
            st.metric(
                f"Healthy Price ({healthy_floor:.0f}% margin)",
                f"${healthy_price:,.2f}",
                help=f"Recommended price for {healthy_floor:.0f}% profit margin"
            )
            if sale_price < healthy_price:
                st.warning(f"💭 Consider pricing at ${healthy_price:.2f}+ for better margins")
        else:
            st.info("Set a target margin in sidebar for pricing recommendations")
    
    with col3:
        remote_status = "✅ Yes" if breakdown.remote_friendly else "❌ No"
        st.metric("Remote-friendly", remote_status)
        
        if breakdown.remote_friendly:
            st.success("Can run unattended")
        else:
            st.warning("Requires manual intervention")

    # Labour time breakdown
    with st.expander("⏱️ Time Breakdown Details"):
        st.markdown(f"""
        **Prep & Cleanup:** {breakdown.base_human_minutes:.1f} min  
        **Plate Changes:** {breakdown.plate_change_minutes:.1f} min  
        **Remote Monitoring:** {breakdown.remote_check_minutes:.1f} min  
        **Total Human Time:** {breakdown.total_human_minutes:.1f} min ({breakdown.total_human_hours:.2f} hours)
        """)

    # Narrative summary
    st.markdown("---")
    st.markdown("### 📝 Summary")
    
    model_label = model_input.model_name or "This model"
    
    summary_parts = []
    
    # Basic info
    summary_parts.append(
        f"{model_label} requires **{breakdown.filament_kg*1000:.0f}g** of filament "
        f"and **{model_input.print_time_hours:.1f} hours** of print time across "
        f"**{model_input.plate_count} plate(s)**."
    )
    
    # Cost and profit
    summary_parts.append(
        f"At a sale price of **${sale_price:,.2f}**, your total cost is **${breakdown.total_cost:,.2f}**, "
        f"resulting in a profit of **${breakdown.profit:,.2f}** (**{margin_text}** margin)."
    )
    
    # Pricing guidance
    if breakdown.profit < 0:
        summary_parts.append(
            f"⚠️ **You're losing ${abs(breakdown.profit):,.2f}** on this print. "
            f"Minimum price should be **${break_even_price:,.2f}** to break even."
        )
    elif healthy_price and sale_price < healthy_price:
        summary_parts.append(
            f"💭 To achieve your target **{healthy_floor:.0f}%** margin, "
            f"consider pricing at **${healthy_price:,.2f}** or higher."
        )
    else:
        summary_parts.append(
            f"✅ This pricing meets your profitability goals."
        )
    
    # Remote-friendly status
    if breakdown.remote_friendly:
        summary_parts.append("✅ This job can run **remotely** with your current automation setup.")
    else:
        summary_parts.append("⚠️ This job requires **manual plate changes** and cannot run fully unattended.")
    
    for part in summary_parts:
        st.markdown(part)

    # Export section
    st.markdown("---")
    st.markdown("### 💾 Export")
    
    # Create detailed report
    bom_data = {
        "Model name": [model_input.model_name or "Unnamed model"],
        "Model URL": [model_input.reference_url or ""],
        "Filament (g)": [breakdown.filament_kg * 1000],
        "Print time (h)": [model_input.print_time_hours],
        "Plates": [model_input.plate_count],
        "Material cost ($)": [breakdown.material_cost],
        "Energy cost ($)": [breakdown.energy_cost],
        "Labour cost ($)": [breakdown.labour_cost],
        "Total cost ($)": [breakdown.total_cost],
        "Sale price ($)": [sale_price],
        "Profit ($)": [breakdown.profit],
        "Margin (%)": [breakdown.profit_margin_percent],
        "Break-even price ($)": [break_even_price],
        "Healthy price ($)": [healthy_price],
        "Status": [verdict],
        "Remote-friendly": [breakdown.remote_friendly],
    }
    bom_df = pd.DataFrame(bom_data)

    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(bom_df.T, use_container_width=True)
    
    with col2:
        csv_bytes = bom_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Cost Report (CSV)",
            data=csv_bytes,
            file_name=f"cost_report_{model_input.model_name or 'model'}.csv".replace(" ", "_"),
            mime="text/csv",
            use_container_width=True,
        )


# ---------------------------------------------------------------------
# Portfolio tab
# ---------------------------------------------------------------------
def render_portfolio_tab(env_settings: EnvironmentSettings):
    """Render the portfolio analysis interface."""
    
    st.markdown("### 📊 Portfolio Analysis")
    
    with st.expander("ℹ️ How to use Portfolio Mode", expanded=False):
        st.markdown("""
        **Analyze multiple models at once:**
        
        1. **Download the CSV template** below
        2. **Fill in your models** with their specifications
        3. **Upload the completed CSV**
        4. **Review the analysis** with cost, profit, and status for each model
        5. **Download the full report** for further analysis
        
        **Required columns:**
        - `model_name` - Name of the model
        - `filament_grams` - Filament weight
        - `print_time_hours` - Print duration
        - `plate_count` - Number of plates
        - `sale_price` - Your selling price
        - `reference_url` - (optional) Link to model source
        """)

    # Template download
    st.markdown("#### 📄 Step 1: Get Template")
    
    example_df = pd.DataFrame({
        "model_name": ["Example Model A", "Example Model B", "Example Model C"],
        "reference_url": [
            "https://makerworld.com/model-a",
            "https://makerworld.com/model-b",
            "",
        ],
        "filament_grams": [83.0, 376.0, 150.0],
        "print_time_hours": [5.4, 16.9, 8.2],
        "plate_count": [1, 1, 2],
        "sale_price": [40.0, 60.0, 45.0],
    })
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(example_df, use_container_width=True)
    with col2:
        template_csv = example_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Template",
            data=template_csv,
            file_name="portfolio_template.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown("#### 📤 Step 2: Upload Your Portfolio")
    
    uploaded = st.file_uploader(
        "Upload your portfolio CSV",
        type=["csv"],
        help="Upload a CSV file matching the template format",
    )

    if uploaded is None:
        st.info("👆 Upload a CSV file to analyze your portfolio")
        return

    # Process uploaded file
    try:
        df = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"❌ Could not read CSV: {exc}")
        return

    # Validate required columns
    required_cols = {
        "model_name",
        "filament_grams",
        "print_time_hours",
        "plate_count",
        "sale_price",
    }
    missing = required_cols - set(df.columns)
    if missing:
        st.error(f"❌ Missing required columns: {', '.join(sorted(missing))}")
        return

    # Calculate costs for all models
    healthy_floor = float(st.session_state["healthy_margin_floor_percent"])
    
    with st.spinner("Analyzing portfolio..."):
        results = []
        for _, row in df.iterrows():
            model = ModelInput(
                model_name=str(row.get("model_name", "")) or None,
                reference_url=str(row.get("reference_url", "")) or None,
                filament_grams=float(row["filament_grams"]),
                print_time_hours=float(row["print_time_hours"]),
                plate_count=int(row["plate_count"]),
                sale_price=float(row["sale_price"]),
                target_margin_percent=None,
            )
            breakdown = calculate_costs(env_settings, model)
            break_even_price, healthy_price = calculate_break_even_and_health(
                breakdown.total_cost, healthy_floor
            )
            verdict = classify_model(model.sale_price, breakdown.total_cost, healthy_price)
            profit_per_hour = (
                breakdown.profit / model.print_time_hours
                if model.print_time_hours > 0
                else 0.0
            )

            results.append({
                "Model": model.model_name,
                "URL": model.reference_url or "",
                "Filament (g)": model.filament_grams,
                "Time (h)": model.print_time_hours,
                "Plates": model.plate_count,
                "Sale ($)": model.sale_price,
                "Cost ($)": breakdown.total_cost,
                "Profit ($)": breakdown.profit,
                "Margin (%)": breakdown.profit_margin_percent,
                "$/hour": profit_per_hour,
                "Remote": "✅" if breakdown.remote_friendly else "❌",
                "Status": verdict,
            })

    results_df = pd.DataFrame(results)

    st.markdown("---")
    st.markdown("#### 📈 Step 3: Review Results")

    # Portfolio summary metrics
    st.markdown("##### Portfolio Overview")
    
    total_models = len(results_df)
    losing = (results_df["Status"] == "Losing money").sum()
    low_margin = (results_df["Status"] == "Low margin").sum()
    healthy = (results_df["Status"] == "Healthy").sum()
    avg_margin = results_df["Margin (%)"].mean()
    total_profit = results_df["Profit ($)"].sum()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Models", total_models)
    col2.metric("Healthy", healthy, delta=f"{healthy/total_models*100:.0f}%")
    col3.metric("Low Margin", low_margin, delta=f"{low_margin/total_models*100:.0f}%")
    col4.metric("Losing Money", losing, delta=f"{losing/total_models*100:.0f}%", delta_color="inverse")
    col5.metric("Avg Margin", f"{avg_margin:.1f}%" if not pd.isna(avg_margin) else "N/A")
    
    st.metric("Total Portfolio Profit", f"${total_profit:,.2f}")

    # Status distribution
    if total_models > 0:
        st.markdown("##### Status Distribution")
        status_counts = results_df["Status"].value_counts()
        st.bar_chart(status_counts, height=200)

    st.markdown("---")
    st.markdown("##### Detailed Results")
    
    # Color-code the dataframe
    def highlight_status(row):
        color = get_status_color(row["Status"])
        return [f'background-color: {color}20' if col == "Status" else '' for col in row.index]
    
    styled_df = results_df.style.apply(highlight_status, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)

    # Insights
    with st.expander("💡 Portfolio Insights"):
        insights = []
        
        if losing > 0:
            losing_models = results_df[results_df["Status"] == "Losing money"]["Model"].tolist()
            insights.append(f"⚠️ **{losing} model(s) losing money:** {', '.join(losing_models)}")
        
        if low_margin > 0:
            insights.append(f"💭 **{low_margin} model(s) have low margins** - consider repricing")
        
        best_margin = results_df.loc[results_df["Margin (%)"].idxmax()]
        insights.append(f"🏆 **Best margin:** {best_margin['Model']} at {best_margin['Margin (%)']:.1f}%")
        
        best_hourly = results_df.loc[results_df["$/hour"].idxmax()]
        insights.append(f"⚡ **Best $/hour:** {best_hourly['Model']} at ${best_hourly['$/hour']:.2f}/hour")
        
        remote_count = (results_df["Remote"] == "✅").sum()
        insights.append(f"🤖 **{remote_count}/{total_models} models** can run remotely")
        
        for insight in insights:
            st.markdown(insight)

    # Export
    st.markdown("---")
    st.markdown("#### 💾 Step 4: Export Report")
    
    # Prepare detailed export
    export_df = pd.DataFrame(results)
    csv_bytes = export_df.to_csv(index=False).encode("utf-8")
    
    col1, col2 = st.columns([2, 1])
    with col2:
        st.download_button(
            "📥 Download Full Report (CSV)",
            data=csv_bytes,
            file_name="portfolio_cost_report.csv",
            mime="text/csv",
            use_container_width=True,
        )


def main():
    """Main application entry point."""
    init_session_defaults()
    env_settings = sidebar_env_settings()

    # Header
    st.title("🖨️ 3D Print Cost Evaluator")
    st.markdown("""
    **Make informed pricing decisions** for your 3D printing business. 
    Calculate true costs including material, energy, and labour to ensure profitable pricing.
    """)
    
    st.markdown("---")

    # Tabs
    tab_single, tab_portfolio = st.tabs(["📋 Single Model", "📊 Portfolio Analysis"])

    with tab_single:
        render_single_model_tab(env_settings)

    with tab_portfolio:
        render_portfolio_tab(env_settings)
    
    # Footer
    st.markdown("---")
    st.caption("💡 Tip: Adjust settings in the sidebar to match your specific costs and workflow.")


if __name__ == "__main__":
    main()
