import ee
import numpy as np

# ── Initialize ────────────────────────────────────────────────────────────────
ee.Initialize(project='lateral-booking-484916-r8')

# ── Himachal Pradesh bounding box ─────────────────────────────────────────────
hp = ee.Geometry.Rectangle([75.5, 30.4, 79.0, 33.3])

months      = list(range(1, 13))
month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']

districts = {
    'Shimla':      ee.Geometry.Point([77.17, 31.10]),
    'Manali':      ee.Geometry.Point([77.18, 32.23]),
    'Dharamshala': ee.Geometry.Point([76.32, 32.21]),
    'Kullu':       ee.Geometry.Point([77.10, 31.95]),
    'Mandi':       ee.Geometry.Point([76.93, 31.70]),
    'Solan':       ee.Geometry.Point([77.09, 30.90]),
    'Bilaspur':    ee.Geometry.Point([76.76, 31.33]),
    'Hamirpur':    ee.Geometry.Point([76.52, 31.68]),
    'Una':         ee.Geometry.Point([76.26, 31.46]),
    'Kangra':      ee.Geometry.Point([76.26, 32.09]),
    'Chamba':      ee.Geometry.Point([76.12, 32.55]),
    'Sirmaur':     ee.Geometry.Point([77.66, 30.55]),
}

def aqi_label(v):
    if   v < 0.000030: return 'Good'
    elif v < 0.000045: return 'Satisfactory'
    elif v < 0.000060: return 'Moderate'
    elif v < 0.000075: return 'Poor'
    elif v < 0.000090: return 'Very Poor'
    else:              return 'Severe'

# ── PART 1 — Monthly HP-wide stats ────────────────────────────────────────────
print("=" * 62)
print("  HIMACHAL PRADESH — NO2 Monthly Analysis (2023 vs 2024)")
print("=" * 62)

no2_2023, no2_2024 = [], []

for month in months:
    for year, store in [(2023, no2_2023), (2024, no2_2024)]:
        img = (ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
               .select('tropospheric_NO2_column_number_density')
               .filterDate(f'{year}-{month:02d}-01', f'{year}-{month:02d}-28')
               .filterBounds(hp).mean().clip(hp))
        val = img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=hp, scale=10000, maxPixels=1e9
        ).get('tropospheric_NO2_column_number_density').getInfo()
        store.append(round(val, 8) if val else 0)

print(f"\n{'Month':<8} {'2023 (mol/m2)':<18} {'Category':<16} {'2024 (mol/m2)':<18} {'Category'}")
print("-" * 72)
for i, m in enumerate(month_names):
    print(f"{m:<8} {no2_2023[i]:<18.6f} {aqi_label(no2_2023[i]):<16} "
          f"{no2_2024[i]:<18.6f} {aqi_label(no2_2024[i])}")

avg23 = round(np.mean(no2_2023), 8)
avg24 = round(np.mean(no2_2024), 8)
chg   = round(((avg24-avg23)/avg23)*100, 2) if avg23 else 0
arrow = "UP (more pollution)" if chg > 0 else "DOWN (cleaner)"

print(f"\n  Annual Average 2023 : {avg23:.6f} mol/m2  ->  {aqi_label(avg23)}")
print(f"  Annual Average 2024 : {avg24:.6f} mol/m2  ->  {aqi_label(avg24)}")
print(f"  Year-on-Year Change : {arrow} {abs(chg)}%")

# ── PART 2 — Seasonal ─────────────────────────────────────────────────────────
print("\n" + "=" * 62)
print("  SEASONAL ANALYSIS — HIMACHAL PRADESH")
print("=" * 62)

seasons = {
    'Winter  (Jan-Feb)':  [0, 1],
    'Spring  (Mar-May)':  [2, 3, 4],
    'Monsoon (Jun-Sep)':  [5, 6, 7, 8],
    'Autumn  (Oct-Nov)':  [9, 10],
    'Pre-Win (Dec)':      [11],
}

print(f"\n{'Season':<22} {'2023 avg':<18} {'2024 avg':<18} {'Change'}")
print("-" * 65)
for season, idx in seasons.items():
    s23 = round(np.mean([no2_2023[i] for i in idx]), 8)
    s24 = round(np.mean([no2_2024[i] for i in idx]), 8)
    ch  = round(((s24-s23)/s23)*100, 1) if s23 else 0
    arr = "UP" if ch > 0 else "DOWN"
    print(f"{season:<22} {s23:.6f} ({aqi_label(s23):<14}) "
          f"{s24:.6f} ({aqi_label(s24):<14}) {arr} {abs(ch)}%")

# ── PART 3 — District ranking ─────────────────────────────────────────────────
print("\n" + "=" * 62)
print("  DISTRICT-WISE NO2 ANALYSIS — HP 2024")
print("=" * 62)

img24 = (ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
         .select('tropospheric_NO2_column_number_density')
         .filterDate('2024-01-01', '2024-12-31')
         .filterBounds(hp).mean().clip(hp))

dresults = {}
for name, point in districts.items():
    try:
        v = img24.sample(point, 5000).first() \
              .get('tropospheric_NO2_column_number_density').getInfo()
        dresults[name] = round(v, 8) if v else 0
    except:
        dresults[name] = 0

sorted_d = sorted(dresults.items(), key=lambda x: x[1], reverse=True)

print(f"\n  {'Rank':<6} {'District':<14} {'NO2 (mol/m2)':<18} {'Category'}")
print("  " + "-" * 52)
for rank, (name, val) in enumerate(sorted_d, 1):
    print(f"  {rank:<6} {name:<14} {val:<18.6f} {aqi_label(val)}")

print(f"\n  Most Polluted : {sorted_d[0][0]}  ({sorted_d[0][1]:.6f} mol/m2 -> {aqi_label(sorted_d[0][1])})")
print(f"  Cleanest      : {sorted_d[-1][0]}  ({sorted_d[-1][1]:.6f} mol/m2 -> {aqi_label(sorted_d[-1][1])})")

# ── PART 4 — HP vs India ──────────────────────────────────────────────────────
print("\n" + "=" * 62)
print("  HIMACHAL PRADESH vs INDIA — 2024")
print("=" * 62)

india = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(
    ee.Filter.eq('country_na', 'India'))

india_img = (ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
             .select('tropospheric_NO2_column_number_density')
             .filterDate('2024-01-01', '2024-12-31')
             .filterBounds(india).mean().clip(india))

india_avg = india_img.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=india.geometry(), scale=25000, maxPixels=1e9
).get('tropospheric_NO2_column_number_density').getInfo()

india_avg = round(india_avg, 8) if india_avg else 0
hp_avg    = avg24
diff_pct  = round(((hp_avg - india_avg) / india_avg) * 100, 1) if india_avg else 0

print(f"\n  India Average 2024 : {india_avg:.6f} mol/m2  ->  {aqi_label(india_avg)}")
print(f"  HP Average 2024    : {hp_avg:.6f} mol/m2  ->  {aqi_label(hp_avg)}")
if diff_pct < 0:
    print(f"\n  Himachal Pradesh is {abs(diff_pct)}% CLEANER than national average!")
else:
    print(f"\n  Himachal Pradesh is {diff_pct}% above national average.")

print("\nAnalysis complete!")