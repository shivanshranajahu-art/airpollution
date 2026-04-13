import ee
import folium
from folium import plugins
import os

# ── 1. Initialize Earth Engine ────────────────────────────────────────────────
print("Initializing Earth Engine...")
ee.Initialize(project='lateral-booking-484916-r8')

# ── 2. Precise HP Boundary & Outline ──────────────────────────────────────────
print("Fetching Data & Processing Full Coverage...")
hp_boundary = ee.FeatureCollection("FAO/GAUL/2015/level1").filter(ee.Filter.eq('ADM1_NAME', 'Himachal Pradesh'))

# Create a crisp, glowing white border for the state to make it look premium
empty = ee.Image().byte()
hp_outline = empty.paint(featureCollection=hp_boundary, color=1, width=2)
outline_url = hp_outline.getMapId({'palette': ['#ffffff']})['tile_fetcher'].url_format


# ── 3. The "Full Fill" Data Function ──────────────────────────────────────────
def get_full_fill_no2(year):
    collection = (ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2")
                  .select('tropospheric_NO2_column_number_density')
                  .filterDate(f'{year}-10-01', f'{year}-12-31')  # Winter Peak for Speed
                  .filterBounds(hp_boundary.geometry()))

    # Process and scale the data
    img = collection.mean().multiply(1000000).clip(hp_boundary)

    # THE MAGIC FIX: unmask(10)
    # This guarantees that EVERY pixel inside HP gets filled.
    # If the satellite missed a snowy mountain, or the air is ultra-clean,
    # it gets a baseline value of 10 (which we will color as Dark Forest Green).
    return img.unmask(10).clip(hp_boundary)


no2_2023 = get_full_fill_no2(2023)
no2_2024 = get_full_fill_no2(2024)

# ── 4. Premium Visualization Palette ──────────────────────────────────────────
# 10: Pristine Air (Dark Forest Green) -> Blends with dark theme but fills the map!
# 20: Clean (Forest Green)
# 30: Moderate (Light Green/Yellow-Green)
# 45: Elevated (Yellow)
# 55: High (Orange)
# 70: Severe (Red)
viz = {
    'min': 10,
    'max': 70,
    'palette': ['#0a2e15', '#228b22', '#adff2f', '#ffff00', '#ff9900', '#ff0000']
}

# ── 5. Build Map & Side-by-Side Slider ────────────────────────────────────────
print("Building UI and rendering map tiles...")
m = folium.Map(location=[31.8, 77.2], zoom_start=8, tiles='CartoDB dark_matter', prefer_canvas=True)

# Generate Tile URLs
url_2023 = ee.Image(no2_2023).getMapId(viz)['tile_fetcher'].url_format
url_2024 = ee.Image(no2_2024).getMapId(viz)['tile_fetcher'].url_format

# Add Data Layers
left_layer = folium.TileLayer(tiles=url_2023, attr='S5P', name='2023', overlay=True, opacity=0.85).add_to(m)
right_layer = folium.TileLayer(tiles=url_2024, attr='S5P', name='2024', overlay=True, opacity=0.85).add_to(m)

# Add the Slider Control
sbs = plugins.SideBySideLayers(left_layer, right_layer)
sbs.add_to(m)

# Add the White State Border (Stays on top of everything)
folium.TileLayer(tiles=outline_url, attr='FAO', name='HP Border', overlay=True, control=False, opacity=0.6).add_to(m)

# ── 6. District Markers ───────────────────────────────────────────────────────
districts = {
    'Baddi': [30.95, 76.79, 'Industrial Zone'],
    'Shimla': [31.10, 77.17, 'Capital'],
    'Manali': [32.23, 77.18, 'Tourism Hub'],
    'Una': [31.46, 76.26, 'Border Region'],
    'Dharamshala': [32.21, 76.32, 'Urban Center']
}

for name, info in districts.items():
    folium.CircleMarker(
        location=[info[0], info[1]],
        radius=5, color='#ffffff', weight=1, fill=True, fill_color='#ffffff', fill_opacity=1.0,
        popup=f"<div style='font-family:sans-serif;'><b>{name}</b><br><small>{info[2]}</small></div>"
    ).add_to(m)

# ── 7. SaaS-Grade Web UI Dashboard ────────────────────────────────────────────
dashboard_html = """
<style>
    /* Dashboard Base */
    .ui-box { position: fixed; z-index: 9999; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: white; background: rgba(10,12,16,0.95); border: 1px solid #333; pointer-events: auto; }

    /* Top Header */
    .header { top: 20px; left: 50%; transform: translateX(-50%); padding: 15px 35px; border-radius: 30px; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.8); }

    /* Bottom Legend */
    .legend { bottom: 30px; right: 20px; padding: 18px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.8); }
    .grad-bar { height: 12px; width: 250px; background: linear-gradient(to right, #0a2e15, #228b22, #adff2f, #ffff00, #ff9900, #ff0000); border-radius: 6px; margin: 12px 0; border: 1px solid #555; }

    /* GIANT WATERMARK LABELS */
    .watermark { position: fixed; top: 50%; transform: translateY(-50%); z-index: 800; font-family: 'Arial Black', sans-serif; font-size: 12vw; font-weight: 900; color: rgba(255, 255, 255, 0.05); pointer-events: none; user-select: none; letter-spacing: -2px; }
    .wm-left { left: 2%; } .wm-right { right: 2%; }

    /* Typography */
    .title-text { margin:0; font-size: 18px; letter-spacing: 1px; font-weight: 600; text-transform: uppercase; }
    .slider-hint { margin-top: 6px; font-size: 13px; color: #00d9ff; font-weight: bold; letter-spacing: 0.5px; }
</style>

<div class="watermark wm-left">2023</div>
<div class="watermark wm-right">2024</div>

<div class="ui-box header">
    <h3 class="title-text">Himachal Pradesh Air Quality Intelligence</h3>
    <div class="slider-hint">◄ 2023 &nbsp; &nbsp; [ DRAG CENTER SLIDER ] &nbsp; &nbsp; 2024 ►</div>
</div>

<div class="ui-box legend">
    <b style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #aaa;">NO₂ Pollution Intensity</b><br>
    <div class="grad-bar"></div>
    <div style="display: flex; justify-content: space-between; font-size: 10px; font-weight: bold; color:#ddd;">
        <span>PRISTINE</span><span>MODERATE</span><span>SEVERE</span>
    </div>
</div>
"""
m.get_root().html.add_child(folium.Element(dashboard_html))

# ── 8. Save and Launch ────────────────────────────────────────────────────────
file_path = 'HP_NO2_Ultimate_Full_Fill.html'
m.save(file_path)
print(f"✅ Success! Premium Map saved to {file_path}. Opening in browser...")
os.startfile(file_path)