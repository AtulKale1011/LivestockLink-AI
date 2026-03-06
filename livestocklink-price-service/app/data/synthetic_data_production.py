import pandas as pd
import numpy as np

np.random.seed(42)

start_date = "2022-01-01"
end_date = "2025-12-31"
dates = pd.date_range(start=start_date, end=end_date, freq="W")

districts = [
    "ahmednagar","akola","amravati","aurangabad","beed",
    "bhandara","buldhana","chandrapur","dhule","gadchiroli",
    "gondia","hingoli","jalgaon","jalna","kolhapur",
    "latur","mumbai_city","mumbai_suburban","nagpur","nanded",
    "nandurbar","nashik","osmanabad","palghar","parbhani",
    "pune","raigad","ratnagiri","sangli","satara",
    "sindhudurg","solapur","thane","wardha","washim","yavatmal"
]

coastal_districts = [
    "mumbai_city","mumbai_suburban","raigad",
    "ratnagiri","sindhudurg","thane","palghar"
]

livestock_config = {
    "cow_milk_A1": {"base": 34, "category": "milk", "unit": "liter"},
    "cow_milk_A2": {"base": 55, "category": "milk", "unit": "liter"},
    "buffalo_milk": {"base": 45, "category": "milk", "unit": "liter"},
    "broiler_chicken": {"base": 100, "category": "meat", "unit": "kg"},
    "desi_chicken": {"base": 180, "category": "meat", "unit": "kg"},
    "layer_egg": {"base": 5, "category": "egg", "unit": "piece"},
    "goat_meat": {"base": 420, "category": "meat", "unit": "kg"},
    "sheep_meat": {"base": 380, "category": "meat", "unit": "kg"},
    "pig_meat": {"base": 200, "category": "meat", "unit": "kg"},
    "fish_rohu": {"base": 150, "category": "fish", "unit": "kg"},
    "fish_katla": {"base": 140, "category": "fish", "unit": "kg"},
    "fish_tilapia": {"base": 130, "category": "fish", "unit": "kg"},
    "fish_surmai": {"base": 450, "category": "fish", "unit": "kg"},
    "fish_pomfret": {"base": 500, "category": "fish", "unit": "kg"},
}

data = []

for livestock, config in livestock_config.items():
    for district in districts:

        district_variation = np.random.uniform(-15, 15)

        for date in dates:

            years_passed = date.year - 2022
            inflation = config["base"] * 0.05 * years_passed

            seasonal = config["base"] * 0.1 * np.sin(
                2 * np.pi * date.isocalendar().week / 52
            )

            festival_flag = 1 if date.month in [6, 7] else 0
            festival_spike = (
                config["base"] * 0.2
                if festival_flag and config["category"] == "meat"
                else 0
            )

            feed_cost_index = 1 + 0.3 * np.sin(2 * np.pi * date.month / 12)
            water_availability_index = 1 + 0.4 * np.sin(2 * np.pi * (date.month-3) / 12)

            disease_risk_index = round(np.random.uniform(0.05, 0.25), 2)
            climate_risk_index = round(np.random.uniform(0.05, 0.3), 2)

            export_demand_index = (
                1.2 if district in coastal_districts and config["category"] == "fish" else 1
            )

            noise = np.random.normal(0, config["base"] * 0.05)

            price = (
                config["base"]
                + district_variation
                + inflation
                + seasonal
                + festival_spike
                + noise
            ) * export_demand_index

            production_cost_estimate = price * (0.6 + 0.1 * feed_cost_index)

            profit_margin_estimate = round(
                (price - production_cost_estimate) / price, 2
            )

            data.append([
                date.strftime("%Y-%m-%d"),
                district,
                livestock,
                config["category"],
                config["unit"],
                round(price, 2),
                round(feed_cost_index, 2),
                round(water_availability_index, 2),
                disease_risk_index,
                climate_risk_index,
                festival_flag,
                export_demand_index,
                round(production_cost_estimate, 2),
                profit_margin_estimate
            ])

df = pd.DataFrame(data, columns=[
    "date",
    "district",
    "animal_type",
    "category",
    "unit",
    "price",
    "feed_cost_index",
    "water_availability_index",
    "disease_risk_index",
    "climate_risk_index",
    "festival_flag",
    "export_demand_index",
    "production_cost_estimate",
    "profit_margin_estimate"
])

df.to_csv("app/data/maharashtra_livestock_economic_weekly.csv", index=False)

print("Economic livestock dataset generated successfully.")
print("Total rows:", len(df))