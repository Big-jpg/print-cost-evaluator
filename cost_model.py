from dataclasses import dataclass


@dataclass
class EnvironmentSettings:
    filament_price_per_kg: float
    electricity_price_per_kwh: float
    printer_power_watts: float
    labour_rate_per_hour: float
    prep_time_minutes: float
    cleanup_time_minutes: float
    plate_change_time_minutes: float
    remote_check_minutes_per_hour: float
    has_automation: bool
    automated_plate_capacity: int


@dataclass
class ModelInput:
    model_name: str | None
    reference_url: str | None
    filament_grams: float
    print_time_hours: float
    plate_count: int
    sale_price: float
    target_margin_percent: float | None = None


@dataclass
class CostBreakdown:
    filament_kg: float
    material_cost: float
    printer_power_kw: float
    energy_cost: float
    base_human_minutes: float
    plate_change_minutes: float
    remote_check_minutes: float
    total_human_minutes: float
    total_human_hours: float
    labour_cost: float
    total_cost: float
    profit: float
    profit_margin_percent: float | None
    remote_friendly: bool
    recommended_sale_price_for_target_margin: float | None


def clamp_non_negative(value: float) -> float:
    return max(value, 0.0)


def calculate_costs(env: EnvironmentSettings, model: ModelInput) -> CostBreakdown:
    # Normalise obvious non-negatives
    filament_grams = clamp_non_negative(model.filament_grams)
    print_time_hours = clamp_non_negative(model.print_time_hours)
    plate_count = max(int(model.plate_count), 0)
    sale_price = model.sale_price

    # Material
    filament_kg = filament_grams / 1000.0
    material_cost = filament_kg * env.filament_price_per_kg

    # Energy
    printer_power_kw = env.printer_power_watts / 1000.0
    energy_cost = print_time_hours * printer_power_kw * env.electricity_price_per_kwh

    # Human time
    base_human_minutes = env.prep_time_minutes + env.cleanup_time_minutes

    if not env.has_automation:
        extra_plate_changes = max(plate_count - 1, 0)
    else:
        if plate_count <= env.automated_plate_capacity:
            extra_plate_changes = 0
        else:
            extra_plate_changes = max(plate_count - env.automated_plate_capacity, 0)

    plate_change_minutes = extra_plate_changes * env.plate_change_time_minutes

    remote_check_minutes = env.remote_check_minutes_per_hour * print_time_hours

    total_human_minutes = base_human_minutes + plate_change_minutes + remote_check_minutes
    total_human_hours = total_human_minutes / 60.0
    labour_cost = total_human_hours * env.labour_rate_per_hour

    total_cost = material_cost + energy_cost + labour_cost
    profit = sale_price - total_cost

    if sale_price > 0:
        profit_margin_percent = (profit / sale_price) * 100.0
    else:
        profit_margin_percent = None

    # Remote-friendly flag
    remote_friendly = (plate_count == 1) or (
        env.has_automation and plate_count <= env.automated_plate_capacity
    )

    # Optional recommended sale price
    recommended_price = None
    if model.target_margin_percent is not None:
        target_margin = model.target_margin_percent / 100.0
        if 0 <= target_margin < 1:
            recommended_price = total_cost / (1.0 - target_margin)

    return CostBreakdown(
        filament_kg=filament_kg,
        material_cost=material_cost,
        printer_power_kw=printer_power_kw,
        energy_cost=energy_cost,
        base_human_minutes=base_human_minutes,
        plate_change_minutes=plate_change_minutes,
        remote_check_minutes=remote_check_minutes,
        total_human_minutes=total_human_minutes,
        total_human_hours=total_human_hours,
        labour_cost=labour_cost,
        total_cost=total_cost,
        profit=profit,
        profit_margin_percent=profit_margin_percent,
        remote_friendly=remote_friendly,
        recommended_sale_price_for_target_margin=recommended_price,
    )
