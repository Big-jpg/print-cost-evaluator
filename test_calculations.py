#!/usr/bin/env python3
"""Test the cost model with the provided test case."""

from cost_model import EnvironmentSettings, ModelInput, calculate_costs


def test_example_case():
    """Test case from requirements document."""
    
    # Test inputs
    env = EnvironmentSettings(
        filament_price_per_kg=25.0,
        electricity_price_per_kwh=0.30,
        printer_power_watts=250.0,
        labour_rate_per_hour=30.0,
        prep_time_minutes=10.0,
        cleanup_time_minutes=10.0,
        plate_change_time_minutes=5.0,
        remote_check_minutes_per_hour=2.0,
        has_automation=False,
        automated_plate_capacity=4,
    )
    
    model = ModelInput(
        model_name="MH-6 Little Bird Helicopter",
        reference_url=None,
        filament_grams=83.0,
        print_time_hours=5.4,
        plate_count=1,
        sale_price=40.0,
        target_margin_percent=None,
    )
    
    # Calculate
    breakdown = calculate_costs(env, model)
    
    # Display results
    print("=" * 60)
    print("3D PRINT COST EVALUATOR - TEST CASE")
    print("=" * 60)
    print(f"\nModel: {model.model_name}")
    print(f"Filament: {model.filament_grams} g")
    print(f"Print time: {model.print_time_hours} h")
    print(f"Plates: {model.plate_count}")
    print(f"Sale price: ${model.sale_price:.2f}")
    
    print("\n" + "-" * 60)
    print("COST BREAKDOWN")
    print("-" * 60)
    print(f"Material cost:    ${breakdown.material_cost:>8.2f}")
    print(f"Energy cost:      ${breakdown.energy_cost:>8.2f}")
    print(f"Labour cost:      ${breakdown.labour_cost:>8.2f}")
    print(f"{'─' * 30}")
    print(f"Total cost:       ${breakdown.total_cost:>8.2f}")
    
    print("\n" + "-" * 60)
    print("PROFIT ANALYSIS")
    print("-" * 60)
    print(f"Sale price:       ${model.sale_price:>8.2f}")
    print(f"Total cost:       ${breakdown.total_cost:>8.2f}")
    print(f"Profit:           ${breakdown.profit:>8.2f}")
    if breakdown.profit_margin_percent is not None:
        print(f"Profit margin:    {breakdown.profit_margin_percent:>7.1f}%")
    
    print("\n" + "-" * 60)
    print("HUMAN TIME BREAKDOWN")
    print("-" * 60)
    print(f"Base time (prep + cleanup): {breakdown.base_human_minutes:.1f} min")
    print(f"Plate change time:          {breakdown.plate_change_minutes:.1f} min")
    print(f"Remote check time:          {breakdown.remote_check_minutes:.1f} min")
    print(f"Total human time:           {breakdown.total_human_minutes:.1f} min ({breakdown.total_human_hours:.2f} h)")
    
    print("\n" + "-" * 60)
    print("OTHER DETAILS")
    print("-" * 60)
    print(f"Remote-friendly: {'✅ Yes' if breakdown.remote_friendly else '❌ No'}")
    print(f"Filament used: {breakdown.filament_kg:.3f} kg")
    print(f"Printer power: {breakdown.printer_power_kw:.2f} kW")
    
    print("\n" + "=" * 60)
    print("EXPECTED VALUES (from requirements)")
    print("=" * 60)
    print("Material cost ≈ $2.08")
    print("Energy cost ≈ $0.41")
    print("Human minutes ≈ 30.8 min → 0.513 h")
    print("Labour cost ≈ $15.4")
    print("Total cost ≈ $17.9")
    print("Profit ≈ $22.1")
    print("Margin ≈ 55.3%")
    print("Remote-friendly ✅ (single plate)")
    
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    
    # Verify calculations
    assert abs(breakdown.material_cost - 2.075) < 0.01, f"Material cost mismatch: {breakdown.material_cost}"
    assert abs(breakdown.energy_cost - 0.405) < 0.01, f"Energy cost mismatch: {breakdown.energy_cost}"
    assert abs(breakdown.total_human_minutes - 30.8) < 0.1, f"Human time mismatch: {breakdown.total_human_minutes}"
    assert abs(breakdown.labour_cost - 15.4) < 0.1, f"Labour cost mismatch: {breakdown.labour_cost}"
    assert abs(breakdown.total_cost - 17.88) < 0.1, f"Total cost mismatch: {breakdown.total_cost}"
    assert abs(breakdown.profit - 22.12) < 0.1, f"Profit mismatch: {breakdown.profit}"
    assert abs(breakdown.profit_margin_percent - 55.3) < 0.5, f"Margin mismatch: {breakdown.profit_margin_percent}"
    assert breakdown.remote_friendly == True, "Should be remote-friendly"
    
    print("✅ All calculations verified successfully!")
    print("=" * 60)


if __name__ == "__main__":
    test_example_case()
