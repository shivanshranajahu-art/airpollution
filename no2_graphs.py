import ee
import matplotlib.pyplot as plt
import numpy as np

# Initialize
ee.Initialize(project='lateral-booking-484916-r8')

# 1. Define India boundary
india = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017") \
          .filter(ee.Filter.eq('country_na', 'India'))

# 2. Fetch monthly NO2 values
months = list(range(1, 13))
no2_2023 = []
no2_2024 = []

print("Fetching data... please wait 3-5 minutes...")

for month in months:
    # 2023
    img_2023 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
                 .select('tropospheric_NO2_column_number_density') \
                 .filterDate(f'2023-{month:02d}-01', f'2023-{month:02d}-28') \
                 .filterBounds(india) \
                 .mean() \
                 .clip(india)

    val_2023 = img_2023.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=india.geometry(),
        scale=10000,
        maxPixels=1e9
    ).get('tropospheric_NO2_column_number_density').getInfo()

    # 2024
    img_2024 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
                 .select('tropospheric_NO2_column_number_density') \
                 .filterDate(f'2024-{month:02d}-01', f'2024-{month:02d}-28') \
                 .filterBounds(india) \
                 .mean() \
                 .clip(india)

    val_2024 = img_2024.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=india.geometry(),
        scale=10000,
        maxPixels=1e9
    ).get('tropospheric_NO2_column_number_density').getInfo()

    no2_2023.append(round(val_2023, 8) if val_2023 else 0)
    no2_2024.append(round(val_2024, 8) if val_2024 else 0)
    print(f"  Month {month:02d} done ✓")

# 3. Month labels
month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']

print("\nAll data fetched! Generating graphs...")

# ----------------------------------------
# GRAPH 1 - Line Chart (2023 vs 2024)
# ----------------------------------------
plt.figure(figsize=(13, 6))
plt.plot(month_names, no2_2023, marker='o', color='royalblue',
         linewidth=2.5, markersize=7, label='2023')
plt.plot(month_names, no2_2024, marker='s', color='crimson',
         linewidth=2.5, markersize=7, label='2024')
plt.fill_between(month_names, no2_2023, no2_2024, alpha=0.1, color='purple')
plt.title('Monthly Average NO₂ over India (2023 vs 2024)', fontsize=15, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('NO₂ Column Density (mol/m²)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('no2_line_chart.png', dpi=150)
plt.show()
print("Graph 1 saved: no2_line_chart.png")

# ----------------------------------------
# GRAPH 2 - Bar Chart (2023 vs 2024)
# ----------------------------------------
x = np.arange(len(month_names))
width = 0.35
plt.figure(figsize=(13, 6))
plt.bar(x - width/2, no2_2023, width, label='2023',
        color='steelblue', edgecolor='black', linewidth=0.5)
plt.bar(x + width/2, no2_2024, width, label='2024',
        color='tomato', edgecolor='black', linewidth=0.5)
plt.title('NO₂ Monthly Comparison - India 2023 vs 2024', fontsize=15, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('NO₂ Column Density (mol/m²)', fontsize=12)
plt.xticks(x, month_names)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('no2_bar_chart.png', dpi=150)
plt.show()
print("Graph 2 saved: no2_bar_chart.png")

# ----------------------------------------
# GRAPH 3 - Seasonal Analysis
# ----------------------------------------
seasons = {
    'Winter (Jan-Feb)': [0, 1],
    'Spring (Mar-May)': [2, 3, 4],
    'Summer (Jun-Aug)': [5, 6, 7],
    'Autumn (Sep-Dec)': [8, 9, 10, 11]
}

seasonal_2023 = [round(np.mean([no2_2023[i] for i in idx]), 8)
                 for idx in seasons.values()]
seasonal_2024 = [round(np.mean([no2_2024[i] for i in idx]), 8)
                 for idx in seasons.values()]

x2 = np.arange(len(seasons))
plt.figure(figsize=(10, 6))
plt.bar(x2 - width/2, seasonal_2023, width, label='2023',
        color='steelblue', edgecolor='black', linewidth=0.5)
plt.bar(x2 + width/2, seasonal_2024, width, label='2024',
        color='tomato', edgecolor='black', linewidth=0.5)
plt.title('Seasonal NO₂ Average over India (2023 vs 2024)', fontsize=15, fontweight='bold')
plt.xlabel('Season', fontsize=12)
plt.ylabel('NO₂ Column Density (mol/m²)', fontsize=12)
plt.xticks(x2, seasons.keys(), fontsize=10)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('no2_seasonal_chart.png', dpi=150)
plt.show()
print("Graph 3 saved: no2_seasonal_chart.png")

# ----------------------------------------
# GRAPH 4 - Annual Average Comparison
# ----------------------------------------
avg_2023 = round(np.mean(no2_2023), 8)
avg_2024 = round(np.mean(no2_2024), 8)
change = round(((avg_2024 - avg_2023) / avg_2023) * 100, 2)

plt.figure(figsize=(7, 6))
bars = plt.bar(['2023', '2024'], [avg_2023, avg_2024],
               color=['steelblue', 'tomato'],
               edgecolor='black', linewidth=0.5, width=0.4)
plt.title('Annual Average NO₂ over India', fontsize=15, fontweight='bold')
plt.ylabel('NO₂ Column Density (mol/m²)', fontsize=12)
for bar, val in zip(bars, [avg_2023, avg_2024]):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
             f'{val:.2e}', ha='center', va='bottom', fontsize=11)
plt.figtext(0.5, 0.01, f'Change from 2023 to 2024: {change}%',
            ha='center', fontsize=11, color='darkgreen')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('no2_annual_chart.png', dpi=150)
plt.show()
print("Graph 4 saved: no2_annual_chart.png")

print("\n✓ All 4 graphs saved successfully in your project folder!")
print(f"\n📊 Annual Average 2023: {avg_2023:.6f} mol/m²")
print(f"📊 Annual Average 2024: {avg_2024:.6f} mol/m²")
print(f"📈 Change: {change}%")