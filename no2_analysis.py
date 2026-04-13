import ee
import folium
import webbrowser
import os

# Initialize
ee.Initialize(project='lateral-booking-484916-r8')

# 1. Define India boundary
india = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017") \
          .filter(ee.Filter.eq('country_na', 'India'))

# 2. Load Sentinel-5P NO2 data
no2 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
        .select('tropospheric_NO2_column_number_density') \
        .filterDate('2023-01-01', '2023-12-31') \
        .filterBounds(india) \
        .mean() \
        .clip(india)

# 3. Visualization parameters
viz = {
    'min': 0,
    'max': 0.0002,
    'palette': ['blue', 'green', 'yellow', 'orange', 'red']
}

# 4. Get tile URL from GEE
map_id = no2.getMapId(viz)
tile_url = map_id['tile_fetcher'].url_format

# 5. Create folium map
m = folium.Map(location=[22, 80], zoom_start=5)

# 6. Add NO2 layer
folium.TileLayer(
    tiles=tile_url,
    attr='Google Earth Engine',
    name='NO2 Pollution India 2023',
    overlay=True,
    control=True
).add_to(m)

# 7. Add layer control
folium.LayerControl().add_to(m)

# 8. Save and open
m.save('india_no2_map.html')
os.startfile('india_no2_map.html')

print("Map opened successfully!")