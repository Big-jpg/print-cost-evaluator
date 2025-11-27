import streamlit as st

from cost_model import (
    EnvironmentSettings,
    ModelInput,
    calculate_costs,
)


st.set_page_config(
    page_title="3D Print Cost Evaluator",
    page_icon="🖨️",
    layout="wide",
)


def init_session_defaults():
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
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def sidebar_env_settings() -> EnvironmentSettings:
    st.sidebar.header("Environment & Preferences")

    filament_price_per_kg = st.sidebar.number_input(
        "Filament price per kg",
        min_value=0.0,
        value=float(st.session_state["filament_price_per_kg"]),
        step=0.5,
    )
    electricity_price_per_kwh = st.sidebar.number_input(
        "Electricity price per kWh",
        min_value=0.0,
        value=float(st.session_state["electricity_price_per_kwh"]),
        step=0.05,
    )
    printer_power_watts = st.sidebar.number_input(
        "Printer power (W)",
        min_value=0.0,
        value=float(st.session_state["printer_power_watts"]),
        step=10.0,
    )

    st.sidebar.markdown("---")
    labour_rate_per_hour = st.sidebar.number_input(
        "Labour rate per hour",
        min_value=0.0,
        value=float(st.session_state["labour_rate_per_hour"]),
        step=1.0,
    )
    prep_time_minutes = st.sidebar.number_input(
        "Prep time (minutes)",
        min_value=0.0,
        value=float(st.session_state["prep_time_minutes"]),
        step=1.0,
    )
    cleanup_time_minutes = st.sidebar.number_input(
        "Cleanup time (minutes)",
        min_value=0.0,
        value=float(st.session_state["cleanup_time_minutes"]),
        step=1.0,
    )
    plate_change_time_minutes = st.sidebar.number_input(
        "Plate change time per plate (minutes)",
        min_value=0.0,
        value=float(st.session_state["plate_change_time_minutes"]),
        step=1.0,
    )
    remote_check_minutes_per_hour = st.sidebar.number_input(
        "Remote check minutes per print hour",
        min_value=0.0,
        value=float(st.session_state["remote_check_minutes_per_hour"]),
        step=0.5,
    )

    st.sidebar.markdown("---")
    has_automation = st.sidebar.checkbox(
        "I have plate automation / sled system",
        value=bool(st.session_state["has_automation"]),
    )
    automated_plate_capacity = st.sidebar.number_input(
        "Automated plate capacity (plates per unattended run)",
        min_value=1,
        value=int(st.session_state["automated_plate_capacity"]),
        step=1,
    )

    # Persist updated values back to session_state
    st.session_state["filament_price_per_kg"] = filament_price_per_kg
    st.session_state["electricity_price_per_kwh"] = electricity_price_per_kwh
    st.session_state["printer_power_watts"] = printer_power_watts
    st.session_state["labour_rate_per_hour"] = labour_rate_per_hour
    st.session_state["prep_time_minutes"] = prep_time_minutes
    st.session_state["cleanup_time_minutes"] = cleanup_time_minutes
    st.session_state["plate_change_time_minutes"] = plate_change_time_minutes
    st.session_state["remote_check_minutes_per_hour"] = remote_check_minutes_per_hour
    st.session_state["has_automation"] = has_automation
    st.session_state["automated_plate_capacity"] = automated_plate_capacity

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


def main():
    init_session_defaults()

    env_settings = sidebar_env_settings()

    st.title("🖨️ 3D Print Cost Evaluator")
    st.write(
        "Estimate the real cost of a 3D printed model, including material, "
        "energy, and human effort. Use this to check if a model is worth "
        "selling at a given price."
    )

    with st.expander("How to use", expanded=False):
        st.markdown(
            """
            1. Enter model details below (filament used, print time, plate count, sale price).

            2. Adjust your environment settings in the sidebar (filament price, labour rate, etc.).

            3. Click **Calculate** to see a full cost breakdown and profit estimate.

            4. Optionally set a **target margin** to see a recommended sale price.

            """
        )

    col1, col2 = st.columns(2)
    with col1:
        model_name = st.text_input("Model name (optional)", value="")
        reference_url = st.text_input("Model URL (optional)", value="")

    with col2:
        filament_grams = st.number_input(
            "Filament used (grams)",
            min_value=0.0,
            value=83.0,
            step=1.0,
        )
        print_time_hours = st.number_input(
            "Print time (hours)",
            min_value=0.0,
            value=5.4,
            step=0.1,
        )

    plate_count = st.number_input(
        "Number of plates used",
        min_value=1,
        value=1,
        step=1,
    )

    sale_price = st.number_input(
        "Sale price for this print (your revenue)",
        min_value=0.0,
        value=40.0,
        step=1.0,
    )

    target_margin_percent = st.number_input(
        "Target margin % (optional; 0 to disable)",
        min_value=0.0,
        max_value=95.0,
        value=0.0,
        step=1.0,
    )
    if target_margin_percent <= 0:
        target_margin = None
    else:
        target_margin = target_margin_percent

    calculate = st.button("Calculate", type="primary")

    if calculate:
        model_input = ModelInput(
            model_name=model_name or None,
            reference_url=reference_url or None,
            filament_grams=filament_grams,
            print_time_hours=print_time_hours,
            plate_count=int(plate_count),
            sale_price=sale_price,
            target_margin_percent=target_margin,
        )

        breakdown = calculate_costs(env_settings, model_input)

        st.subheader("Cost breakdown")

        c1, c2, c3 = st.columns(3)
        c1.metric("Material cost", f"${breakdown.material_cost:,.2f}")
        c2.metric("Energy cost", f"${breakdown.energy_cost:,.2f}")
        c3.metric("Labour cost", f"${breakdown.labour_cost:,.2f}")

        c4, c5, c6 = st.columns(3)
        c4.metric("Total cost", f"${breakdown.total_cost:,.2f}")
        c5.metric("Sale price", f"${sale_price:,.2f}")
        c6.metric("Profit", f"${breakdown.profit:,.2f}")

        margin_text = (
            f"{breakdown.profit_margin_percent:,.1f}%"
            if breakdown.profit_margin_percent is not None
            else "N/A"
        )
        c7, c8, c9 = st.columns(3)
        c7.metric("Profit margin", margin_text)
        c8.metric("Human time (hours)", f"{breakdown.total_human_hours:,.2f}")
        c9.metric(
            "Remote-friendly",
            "✅ Yes" if breakdown.remote_friendly else "❌ No",
        )

        st.markdown("---")

        st.markdown("### Details")
        st.markdown(
            f"- **Filament used:** {breakdown.filament_kg*1000:.1f} g "
            f"({breakdown.filament_kg:.3f} kg)\n"
            f"- **Printer power:** {breakdown.printer_power_kw:.2f} kW\n"
            f"- **Base human time:** {breakdown.base_human_minutes:.1f} min\n"
            f"- **Plate change time:** {breakdown.plate_change_minutes:.1f} min\n"
            f"- **Remote checks:** {breakdown.remote_check_minutes:.1f} min\n"
            f"- **Total human time:** {breakdown.total_human_minutes:.1f} min"
        )

        if target_margin is not None and breakdown.recommended_sale_price_for_target_margin:
            st.markdown("---")
            st.subheader("Recommended price for target margin")
            st.write(
                f"To achieve a **{target_margin:.1f}%** margin, "
                f"you should charge approximately "
                f"**${breakdown.recommended_sale_price_for_target_margin:,.2f}**."
            )

        st.markdown("---")
        st.markdown("### Summary")

        model_label = model_input.model_name or "this model"
        summary_lines = [
            f"For **{model_label}**, printing one copy uses "
            f"**{breakdown.filament_kg*1000:.0f} g** of filament and "
            f"**{model_input.print_time_hours:.1f} h** of printer time across "
            f"**{model_input.plate_count} plate(s)**.",
            f"Your estimated total cost is **${breakdown.total_cost:,.2f}**, "
            f"giving a profit of **${breakdown.profit:,.2f}** "
            f"({margin_text} margin) at a sale price of **${sale_price:,.2f}**.",
            "This job is "
            + ("**remote-friendly** ✅ in your current setup."
               if breakdown.remote_friendly
               else "**not remote-friendly** ❌ in your current setup."),
        ]

        for line in summary_lines:
            st.markdown(f"- {line}")


if __name__ == "__main__":
    main()
