import ee
import folium
import os

# Initialize
ee.Initialize(project='lateral-booking-484916-r8')

# 1. Define India boundary
india = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017") \
          .filter(ee.Filter.eq('country_na', 'India'))

# 2. Full year 2023 - using median instead of mean (faster + better quality)
no2_2023 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
             .select('tropospheric_NO2_column_number_density') \
             .filterDate('2023-01-01', '2023-12-31') \
             .filterBounds(india) \
             .median() \
             .clip(india)

# 3. Full year 2024
no2_2024 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
             .select('tropospheric_NO2_column_number_density') \
             .filterDate('2024-01-01', '2024-12-31') \
             .filterBounds(india) \
             .median() \
             .clip(india)

# 4. Visualization parameters
viz = {
    'min': 0.00005,
    'max': 0.00025,
    'palette': [
        '000080',
        '0000FF',
        '00FF00',
        'FFFF00',
        'FF8000',
        'FF0000'
    ]
}

# 5. Get tile URLs
tile_2023 = no2_2023.getMapId(viz)['tile_fetcher'].url_format
tile_2024 = no2_2024.getMapId(viz)['tile_fetcher'].url_format

# 6. Create folium map with faster tiles
m = folium.Map(
    location=[22, 80],
    zoom_start=5,
    tiles='CartoDB positron',
    prefer_canvas=True,
    zoom_control=True
)

# 7. Add 2023 layer - hidden by default
folium.TileLayer(
    tiles=tile_2023,
    attr='Google Earth Engine',
    name='NO2 - Full Year 2023',
    overlay=True,
    control=True,
    show=False,
    opacity=0.85
).add_to(m)

# 8. Add 2024 layer - visible by default
folium.TileLayer(
    tiles=tile_2024,
    attr='Google Earth Engine',
    name='NO2 - Full Year 2024',
    overlay=True,
    control=True,
    show=True,
    opacity=0.85
).add_to(m)

# 9. Add layer control
folium.LayerControl(collapsed=False).add_to(m)

# 10. Save
m.save('no2_2023_2024.html')

# 11. Inject performance fix into HTML
with open('no2_2023_2024.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add performance CSS and loading message
performance_fix = """
<style>
  .leaflet-tile {
    image-rendering: auto !important;
  }
  .leaflet-tile-container {
    will-change: auto !important;
  }
  #loading-msg {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(26,35,126,0.92);
    color: white;
    padding: 18px 32px;
    border-radius: 12px;
    font-size: 16px;
    font-family: Segoe UI, sans-serif;
    z-index: 9999;
    text-align: center;
  }
</style>
<div id="loading-msg">
  🛰️ Loading NO₂ Satellite Data...<br/>
  <small>Please wait a few seconds</small>
</div>
<script>
  window.addEventListener('load', function() {
    setTimeout(function() {
      var msg = document.getElementById('loading-msg');
      if (msg) msg.style.display = 'none';
    }, 4000);
  });
</script>
"""

html = html.replace('</head>', performance_fix + '</head>')

with open('no2_2023_2024.html', 'w', encoding='utf-8') as f:
    f.write(html)

os.startfile('no2_2023_2024.html')
print("Optimized comparison map opened!")
print("Toggle 2023/2024 using top-right layer control")