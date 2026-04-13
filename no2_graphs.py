import ee
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Initialize ────────────────────────────────────────────────────────────────
ee.Initialize(project='lateral-booking-484916-r8')

# ── Himachal Pradesh bounding box ─────────────────────────────────────────────
hp = ee.Geometry.Rectangle([75.5, 30.4, 79.0, 33.3])

# ── AQI colour helpers ────────────────────────────────────────────────────────
def aqi_color(v):
    if   v < 0.000030: return '#00e400'
    elif v < 0.000045: return '#92d050'
    elif v < 0.000060: return '#ffff00'
    elif v < 0.000075: return '#ff7e00'
    elif v < 0.000090: return '#ff0000'
    else:              return '#7e0023'

def aqi_label(v):
    if   v < 0.000030: return 'Good'
    elif v < 0.000045: return 'Satisfactory'
    elif v < 0.000060: return 'Moderate'
    elif v < 0.000075: return 'Poor'
    elif v < 0.000090: return 'Very Poor'
    else:              return 'Severe'

AQI_LEGEND = [
    mpatches.Patch(color='#00e400', label='Good'),
    mpatches.Patch(color='#92d050', label='Satisfactory'),
    mpatches.Patch(color='#ffff00', label='Moderate'),
    mpatches.Patch(color='#ff7e00', label='Poor'),
    mpatches.Patch(color='#ff0000', label='Very Poor'),
    mpatches.Patch(color='#7e0023', label='Severe'),
]

months      = list(range(1, 13))
month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
DARK = '#0d1117'
CARD = '#161b22'

# ── Fetch monthly NO2 (2023 & 2024) ──────────────────────────────────────────
no2_2023, no2_2024 = [], []
print("Fetching Himachal Pradesh monthly NO2... (~3 min)")

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
    print(f"  Month {month:02d} done")

print("\nGenerating graphs...")

# ── GRAPH 1 — Line Chart ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 6))
fig.patch.set_facecolor(DARK); ax.set_facecolor(CARD)

ax.plot(month_names, no2_2023, marker='o', color='#00b4d8',
        linewidth=2.5, markersize=7, label='2023', zorder=3)
ax.plot(month_names, no2_2024, marker='s', color='#f72585',
        linewidth=2.5, markersize=7, label='2024', zorder=3)
ax.fill_between(month_names, no2_2023, no2_2024, alpha=0.12, color='#9d4edd')

for x, y in zip(month_names, no2_2023):
    ax.plot(x, y, 'o', color=aqi_color(y), markersize=11, zorder=5)
for x, y in zip(month_names, no2_2024):
    ax.plot(x, y, 's', color=aqi_color(y), markersize=11, zorder=5)

ax.set_title('Monthly Average NO2 over Himachal Pradesh (2023 vs 2024)',
             fontsize=15, fontweight='bold', color='white', pad=14)
ax.set_xlabel('Month', fontsize=12, color='white')
ax.set_ylabel('NO2 Column Density (mol/m2)', fontsize=12, color='white')
ax.tick_params(colors='white')
ax.grid(True, alpha=0.15, color='white', linestyle='--')
for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

line_leg = [plt.Line2D([0],[0],color='#00b4d8',marker='o',linewidth=2,label='2023'),
            plt.Line2D([0],[0],color='#f72585',marker='s',linewidth=2,label='2024')]
l1 = ax.legend(handles=line_leg, loc='upper left',
               facecolor='#1a1a2e', edgecolor='#30363d', labelcolor='white',
               fontsize=10, title='Year', title_fontsize=10)
ax.add_artist(l1)
ax.legend(handles=AQI_LEGEND, loc='upper right',
          facecolor='#1a1a2e', edgecolor='#30363d', labelcolor='white',
          fontsize=9, title='AQI Category', title_fontsize=9)

plt.tight_layout()
plt.savefig('no2_line_chart.png', dpi=150, facecolor=DARK)
plt.show()
print("Graph 1 saved: no2_line_chart.png")

# ── GRAPH 2 — Bar Chart ───────────────────────────────────────────────────────
x = np.arange(len(month_names)); w = 0.35

fig, ax = plt.subplots(figsize=(13, 6))
fig.patch.set_facecolor(DARK); ax.set_facecolor(CARD)

b1 = ax.bar(x-w/2, no2_2023, w, color=[aqi_color(v) for v in no2_2023],
            edgecolor=DARK, linewidth=0.7, label='2023')
b2 = ax.bar(x+w/2, no2_2024, w, color=[aqi_color(v) for v in no2_2024],
            edgecolor=DARK, linewidth=0.7, alpha=0.80, hatch='///', label='2024')

ax.set_title('NO2 Monthly Comparison - Himachal Pradesh 2023 vs 2024',
             fontsize=15, fontweight='bold', color='white', pad=14)
ax.set_xlabel('Month', fontsize=12, color='white')
ax.set_ylabel('NO2 Column Density (mol/m2)', fontsize=12, color='white')
ax.set_xticks(x); ax.set_xticklabels(month_names, color='white')
ax.tick_params(colors='white')
ax.grid(True, alpha=0.15, color='white', axis='y', linestyle='--')
for sp in ax.spines.values(): sp.set_edgecolor('#30363d')
ax.legend(handles=AQI_LEGEND, facecolor='#1a1a2e', edgecolor='#30363d',
          labelcolor='white', fontsize=9, title='AQI Category', title_fontsize=9)

plt.tight_layout()
plt.savefig('no2_bar_chart.png', dpi=150, facecolor=DARK)
plt.show()
print("Graph 2 saved: no2_bar_chart.png")

# ── GRAPH 3 — Seasonal ────────────────────────────────────────────────────────
seasons = {
    'Winter\n(Jan-Feb)':  [0, 1],
    'Spring\n(Mar-May)':  [2, 3, 4],
    'Monsoon\n(Jun-Sep)': [5, 6, 7, 8],
    'Autumn\n(Oct-Nov)':  [9, 10],
    'Pre-Win\n(Dec)':     [11],
}
s23 = [np.mean([no2_2023[i] for i in idx]) for idx in seasons.values()]
s24 = [np.mean([no2_2024[i] for i in idx]) for idx in seasons.values()]
x2  = np.arange(len(seasons))

fig, ax = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor(DARK); ax.set_facecolor(CARD)

bars23 = ax.bar(x2-w/2, s23, w, color=[aqi_color(v) for v in s23],
                edgecolor=DARK, linewidth=0.7)
bars24 = ax.bar(x2+w/2, s24, w, color=[aqi_color(v) for v in s24],
                edgecolor=DARK, linewidth=0.7, alpha=0.80, hatch='///')

for bar, v in zip(list(bars23)+list(bars24), s23+s24):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+max(s23+s24)*0.012,
            f'{v:.2e}', ha='center', va='bottom', fontsize=8.5, color='white', rotation=30)

ax.set_title('Seasonal NO2 Average over Himachal Pradesh (2023 vs 2024)',
             fontsize=15, fontweight='bold', color='white', pad=14)
ax.set_xlabel('Season', fontsize=12, color='white')
ax.set_ylabel('NO2 Column Density (mol/m2)', fontsize=12, color='white')
ax.set_xticks(x2); ax.set_xticklabels(list(seasons.keys()), color='white', fontsize=9)
ax.tick_params(colors='white')
ax.grid(True, alpha=0.15, color='white', axis='y', linestyle='--')
for sp in ax.spines.values(): sp.set_edgecolor('#30363d')
ax.legend(handles=AQI_LEGEND, facecolor='#1a1a2e', edgecolor='#30363d',
          labelcolor='white', fontsize=9, title='AQI Category', title_fontsize=9)

plt.tight_layout()
plt.savefig('no2_seasonal_chart.png', dpi=150, facecolor=DARK)
plt.show()
print("Graph 3 saved: no2_seasonal_chart.png")

# ── GRAPH 4 — Annual Average ──────────────────────────────────────────────────
avg23 = round(np.mean(no2_2023), 8)
avg24 = round(np.mean(no2_2024), 8)
chg   = round(((avg24-avg23)/avg23)*100, 2) if avg23 else 0

fig, ax = plt.subplots(figsize=(7, 6))
fig.patch.set_facecolor(DARK); ax.set_facecolor(CARD)

bars = ax.bar(['2023', '2024'], [avg23, avg24],
              color=[aqi_color(avg23), aqi_color(avg24)],
              edgecolor='white', linewidth=1, width=0.4)
for bar, val in zip(bars, [avg23, avg24]):
    ax.text(bar.get_x()+bar.get_width()/2,
            bar.get_height()+max(avg23,avg24)*0.02,
            f'{val:.2e}\n({aqi_label(val)})',
            ha='center', va='bottom', fontsize=11, color='white', fontweight='bold')

arrow = 'UP' if chg > 0 else 'DOWN'
chg_col = '#ff4444' if chg > 0 else '#44ff88'
ax.set_title('Annual Average NO2 over Himachal Pradesh',
             fontsize=15, fontweight='bold', color='white', pad=14)
ax.set_ylabel('NO2 Column Density (mol/m2)', fontsize=12, color='white')
ax.tick_params(colors='white')
ax.grid(True, alpha=0.15, color='white', axis='y', linestyle='--')
for sp in ax.spines.values(): sp.set_edgecolor('#30363d')
fig.text(0.5, 0.01, f'Change from 2023 to 2024: {arrow} {abs(chg)}%',
         ha='center', fontsize=13, color=chg_col, fontweight='bold')

plt.tight_layout()
plt.savefig('no2_annual_chart.png', dpi=150, facecolor=DARK)
plt.show()
print("Graph 4 saved: no2_annual_chart.png")

# ── GRAPH 5 — District-wise NO2 (UNIQUE colour per district by AQI) ───────────
print("\nFetching district-level data for 2024...")

district_coords = {
    'Shimla':      [77.17, 31.10],
    'Manali':      [77.18, 32.23],
    'Dharamshala': [76.32, 32.21],
    'Kullu':       [77.10, 31.95],
    'Mandi':       [76.93, 31.70],
    'Solan':       [77.09, 30.90],
    'Bilaspur':    [76.76, 31.33],
    'Hamirpur':    [76.52, 31.68],
    'Una':         [76.26, 31.46],
    'Kangra':      [76.26, 32.09],
    'Chamba':      [76.12, 32.55],
    'Sirmaur':     [77.66, 30.55],
}

img24 = (ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
         .select('tropospheric_NO2_column_number_density')
         .filterDate('2024-01-01', '2024-12-31')
         .filterBounds(hp).median().clip(hp))

dvals = {}
for name, coords in district_coords.items():
    try:
        v = img24.sample(ee.Geometry.Point(coords), 5000).first() \
              .get('tropospheric_NO2_column_number_density').getInfo()
        dvals[name] = round(v, 8) if v else 0
    except:
        dvals[name] = 0
    print(f"  {name} done")

sorted_d = sorted(dvals.items(), key=lambda x: x[1], reverse=True)
dn = [d[0] for d in sorted_d]
dv = [d[1] for d in sorted_d]

fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor(DARK); ax.set_facecolor(CARD)

bars = ax.bar(dn, dv, color=[aqi_color(v) for v in dv],
              edgecolor=DARK, linewidth=0.8, width=0.6)

for bar, val in zip(bars, dv):
    ax.text(bar.get_x()+bar.get_width()/2,
            bar.get_height()+max(dv)*0.008,
            f'{val:.2e}\n{aqi_label(val)}',
            ha='center', va='bottom', fontsize=8.5,
            color='white', fontweight='bold')

ax.set_title('District-wise NO2 Levels - Himachal Pradesh 2024',
             fontsize=14, fontweight='bold', color='white', pad=14)
ax.set_xlabel('District', fontsize=12, color='white')
ax.set_ylabel('NO2 Column Density (mol/m2)', fontsize=12, color='white')
ax.tick_params(axis='x', colors='white', rotation=20, labelsize=10)
ax.tick_params(axis='y', colors='white')
ax.grid(True, alpha=0.15, color='white', axis='y', linestyle='--')
for sp in ax.spines.values(): sp.set_edgecolor('#30363d')
ax.legend(handles=AQI_LEGEND, facecolor='#1a1a2e', edgecolor='#30363d',
          labelcolor='white', fontsize=9, title='AQI Category', title_fontsize=9)

plt.tight_layout()
plt.savefig('no2_district_chart.png', dpi=150, facecolor=DARK)
plt.show()
print("Graph 5 saved: no2_district_chart.png")

print(f"\nAll 5 graphs saved successfully in your project folder!")
print(f"\nHP Annual Average 2023: {avg23:.6f} mol/m2  -> {aqi_label(avg23)}")
print(f"HP Annual Average 2024: {avg24:.6f} mol/m2  -> {aqi_label(avg24)}")
print(f"Change: {chg}%")
print(f"Most polluted district: {sorted_d[0][0]}")
print(f"Cleanest district:      {sorted_d[-1][0]}")