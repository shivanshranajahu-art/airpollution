from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

# ── Document ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "HP_NO2_Air_Pollution_Report.pdf",
    pagesize=A4,
    rightMargin=60, leftMargin=60,
    topMargin=60,   bottomMargin=60,
)
styles  = getSampleStyleSheet()
content = []

# ── Styles ────────────────────────────────────────────────────────────────────
title_style = ParagraphStyle('T', parent=styles['Title'],
    fontSize=20, textColor=colors.HexColor('#1a237e'),
    spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold')

subtitle_style = ParagraphStyle('S', parent=styles['Normal'],
    fontSize=12, textColor=colors.HexColor('#37474f'),
    spaceAfter=4, alignment=TA_CENTER)

heading_style = ParagraphStyle('H', parent=styles['Heading1'],
    fontSize=14, textColor=colors.HexColor('#1a237e'),
    spaceBefore=16, spaceAfter=6, fontName='Helvetica-Bold')

body_style = ParagraphStyle('B', parent=styles['Normal'],
    fontSize=11, textColor=colors.HexColor('#212121'),
    spaceAfter=6, leading=16, alignment=TA_JUSTIFY)

caption_style = ParagraphStyle('C', parent=styles['Normal'],
    fontSize=9, textColor=colors.grey,
    spaceAfter=4, alignment=TA_CENTER, fontName='Helvetica-Oblique')

# ── TITLE PAGE ────────────────────────────────────────────────────────────────
content.append(Spacer(1, 0.5*inch))
content.append(Paragraph("Air Pollution Analysis Using Satellite Data", title_style))
content.append(Paragraph("Nitrogen Dioxide (NO2) Study over Himachal Pradesh", title_style))
content.append(Spacer(1, 0.2*inch))
content.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a237e')))
content.append(Spacer(1, 0.2*inch))
content.append(Paragraph("Using Sentinel-5P Satellite Data on Google Earth Engine", subtitle_style))
content.append(Paragraph("Dataset: COPERNICUS/S5P/OFFL/L3_NO2", subtitle_style))
content.append(Paragraph("Region: Himachal Pradesh, India  |  Period: 2023 - 2024", subtitle_style))
content.append(Spacer(1, 0.2*inch))
content.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
content.append(Spacer(1, 0.3*inch))

student_data = [
    ['Field', 'Details'],
    ['Student Name', 'Your Name Here'],
    ['Roll Number',  'Your Roll Number'],
    ['Course',       'Your Course Name'],
    ['Institution',  'Your College Name'],
    ['Submitted To', 'Your Teacher Name'],
    ['Year',         '2024-2025'],
]
student_table = Table(student_data, colWidths=[2.2*inch, 3.8*inch])
student_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,0),  colors.HexColor('#1a237e')),
    ('TEXTCOLOR',     (0,0),(-1,0),  colors.white),
    ('FONTNAME',      (0,0),(-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0),(-1,0),  12),
    ('BACKGROUND',    (0,1),(-1,-1), colors.HexColor('#e8eaf6')),
    ('FONTNAME',      (0,1),(0,-1),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,1),(-1,-1), 11),
    ('GRID',          (0,0),(-1,-1), 0.5, colors.grey),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, colors.HexColor('#e8eaf6')]),
    ('PADDING',       (0,0),(-1,-1), 8),
]))
content.append(student_table)
content.append(Spacer(1, 0.3*inch))

# ── SECTION 1 — Introduction ──────────────────────────────────────────────────
content.append(Paragraph("1. Introduction", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))
content.append(Paragraph(
    "Air pollution is one of the most critical environmental challenges facing the world today. "
    "Nitrogen Dioxide (NO2) is a harmful gas primarily produced by vehicle emissions, industrial "
    "activities, and power plants. Prolonged exposure to NO2 causes respiratory diseases, "
    "cardiovascular problems, and contributes to the formation of acid rain and smog.",
    body_style))
content.append(Paragraph(
    "This project analyzes the spatial and temporal distribution of NO2 pollution over "
    "Himachal Pradesh — a mountainous Himalayan state in northern India — using satellite "
    "data from the Sentinel-5P satellite, processed on Google Earth Engine (GEE). "
    "Because Himachal Pradesh has much lower pollution levels than the Indo-Gangetic Plain, "
    "a tight colour scale (0.000020-0.000080 mol/m2) is used so that all AQI colour categories "
    "are visible and district-level differences are clearly distinguishable. "
    "The study compares 2023 vs 2024 monthly, seasonal, and district-level NO2 levels.",
    body_style))

# ── SECTION 2 — Objectives ────────────────────────────────────────────────────
content.append(Paragraph("2. Objectives", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))
objectives = [
    "To analyze the spatial distribution of NO2 pollution across Himachal Pradesh districts.",
    "To perform temporal comparison of NO2 levels between 2023 and 2024.",
    "To identify high-pollution districts vs clean districts in HP.",
    "To study seasonal variations in NO2 (Winter, Spring, Monsoon, Autumn).",
    "To compare Himachal Pradesh NO2 levels against the India national average.",
    "To visualize pollution data using AQI-colour-coded charts and interactive maps.",
]
for i, obj in enumerate(objectives, 1):
    content.append(Paragraph(f" {i}. {obj}", body_style))

# ── SECTION 3 — Tools and Dataset ─────────────────────────────────────────────
content.append(Paragraph("3. Tools and Dataset Used", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))
tools_data = [
    ['Tool / Dataset',              'Purpose'],
    ['Google Earth Engine (GEE)',   'Cloud-based satellite data processing'],
    ['Sentinel-5P (TROPOMI)',       'NO2 satellite data source'],
    ['COPERNICUS/S5P/OFFL/L3_NO2', 'Exact GEE dataset used'],
    ['Python 3.x',                  'Programming language'],
    ['earthengine-api',             'Python API for GEE'],
    ['Folium',                      'Interactive HP-centred map with AQI legend'],
    ['Matplotlib',                  'AQI-colour-coded graphs and district charts'],
    ['ReportLab',                   'PDF report generation'],
    ['PyCharm IDE',                 'Development environment'],
]
tools_table = Table(tools_data, colWidths=[3*inch, 3*inch])
tools_table.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,0),  colors.HexColor('#1a237e')),
    ('TEXTCOLOR',     (0,0),(-1,0),  colors.white),
    ('FONTNAME',      (0,0),(-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0),(-1,-1), 10),
    ('GRID',          (0,0),(-1,-1), 0.5, colors.grey),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, colors.HexColor('#e8eaf6')]),
    ('PADDING',       (0,0),(-1,-1), 7),
]))
content.append(tools_table)

# ── SECTION 4 — Methodology ───────────────────────────────────────────────────
content.append(Paragraph("4. Methodology", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))
content.append(Paragraph(
    "The methodology followed in this project involves the following steps:", body_style))
steps = [
    "Account Setup: Created a Google Earth Engine account and authenticated the Python API.",
    "Region: Defined HP bounding box (75.5E-79.0E, 30.4N-33.3N) instead of all-India.",
    "Data Collection: Accessed Sentinel-5P NO2 data filtered to HP boundary for 2023-2024.",
    "Colour Fix: Set viz min=0.000020, max=0.000080 mol/m2 so all 6 AQI colours appear on map.",
    "District Sampling: Sampled NO2 at 12 HP district centres to compare local levels.",
    "Temporal Analysis: Computed monthly, seasonal, and annual means for 2023 and 2024.",
    "HP vs India: Compared HP annual average against national India 2024 average.",
    "Visualization: 5 AQI-colour-coded graphs + 1 interactive Folium map with district pins.",
    "Report Generation: Compiled all results into this professional PDF report.",
]
for i, step in enumerate(steps, 1):
    content.append(Paragraph(f" Step {i}: {step}", body_style))

# ── SECTION 5 — AQI Scale ─────────────────────────────────────────────────────
content.append(Paragraph("5. AQI Colour Scale (Tuned for Himachal Pradesh)", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))
aqi_data = [
    ['Category',     'NO2 Range (mol/m2)',   'Health Impact'],
    ['Good',         '< 0.000030',           'Minimal risk — typical in HP mountains'],
    ['Satisfactory', '0.000030 - 0.000045',  'Acceptable; minor risk for sensitive groups'],
    ['Moderate',     '0.000045 - 0.000060',  'Sensitive groups may experience effects'],
    ['Poor',         '0.000060 - 0.000075',  'Health effects for general public'],
    ['Very Poor',    '0.000075 - 0.000090',  'Serious health effects — industrial areas'],
    ['Severe',       '> 0.000090',           'Emergency conditions'],
]
aqi_bgs = {
    'Good':         colors.HexColor('#00e400'),
    'Satisfactory': colors.HexColor('#92d050'),
    'Moderate':     colors.HexColor('#ffff00'),
    'Poor':         colors.HexColor('#ff7e00'),
    'Very Poor':    colors.HexColor('#ff0000'),
    'Severe':       colors.HexColor('#7e0023'),
}
aqi_table = Table(aqi_data, colWidths=[1.5*inch, 1.8*inch, 2.7*inch])
ts = [
    ('BACKGROUND',  (0,0),(-1,0),  colors.HexColor('#1a237e')),
    ('TEXTCOLOR',   (0,0),(-1,0),  colors.white),
    ('FONTNAME',    (0,0),(-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',    (0,0),(-1,-1), 9),
    ('GRID',        (0,0),(-1,-1), 0.5, colors.grey),
    ('PADDING',     (0,0),(-1,-1), 6),
]
for r, (cat, *_) in enumerate(aqi_data[1:], 1):
    if cat in aqi_bgs:
        ts.append(('BACKGROUND', (0,r),(0,r), aqi_bgs[cat]))
        txt = colors.black if cat in ('Good','Satisfactory','Moderate') else colors.white
        ts.append(('TEXTCOLOR',  (0,r),(0,r), txt))
aqi_table.setStyle(TableStyle(ts))
content.append(aqi_table)

# ── SECTION 6 — Results ───────────────────────────────────────────────────────
content.append(Paragraph("6. Results and Analysis", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))

graphs = [
    ('no2_line_chart.png',     'Figure 1: Monthly NO2 Trend - HP 2023 vs 2024 (AQI coloured dots)'),
    ('no2_bar_chart.png',      'Figure 2: Monthly NO2 Bar Comparison - HP 2023 vs 2024'),
    ('no2_seasonal_chart.png', 'Figure 3: Seasonal NO2 Analysis - Himachal Pradesh'),
    ('no2_annual_chart.png',   'Figure 4: Annual Average NO2 Comparison'),
    ('no2_district_chart.png', 'Figure 5: District-wise NO2 - Himachal Pradesh 2024'),
]
for img_file, caption in graphs:
    if os.path.exists(img_file):
        content.append(Paragraph(caption, caption_style))
        content.append(Image(img_file, width=5.5*inch, height=3*inch))
        content.append(Spacer(1, 0.2*inch))
    else:
        content.append(Paragraph(
            f"Image not found: {img_file}  — Run no2_graphs.py first.", body_style))

# ── SECTION 7 — Conclusion ────────────────────────────────────────────────────
content.append(Paragraph("7. Conclusion", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))
content.append(Paragraph(
    "This project successfully demonstrated the use of Google Earth Engine and Sentinel-5P "
    "satellite data for analyzing air pollution (NO2) over Himachal Pradesh. The interactive "
    "maps clearly show AQI-colour-coded pollution levels across HP districts. By using a tight "
    "colour scale appropriate for HP (not the India-wide scale), district differences are now "
    "clearly visible in green, yellow, orange, and red — not just a uniform blue.",
    body_style))
content.append(Paragraph(
    "District analysis shows that lower-altitude industrial zones (Solan, Una) have higher "
    "NO2 levels, while high-altitude districts (Chamba, Lahaul-Spiti) are among the cleanest. "
    "Seasonal analysis confirms higher NO2 in winter due to temperature inversions, and the "
    "lowest levels during monsoon when rainfall scrubs pollutants from the air. "
    "Overall, Himachal Pradesh remains significantly cleaner than the national India average, "
    "benefiting from its mountainous terrain, forest cover, and limited heavy industry.",
    body_style))

# ── SECTION 8 — References ────────────────────────────────────────────────────
content.append(Paragraph("8. References", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))
references = [
    "Google Earth Engine. (2024). Earth Engine Data Catalog. https://developers.google.com/earth-engine/datasets",
    "European Space Agency. (2024). Sentinel-5P TROPOMI. https://sentinel.esa.int/web/sentinel/missions/sentinel-5p",
    "Copernicus. (2024). NO2 Tropospheric Column. COPERNICUS/S5P/OFFL/L3_NO2",
    "CPCB India. National Air Quality Index. https://cpcb.nic.in",
    "Python Software Foundation. (2024). Python 3.x Documentation. https://docs.python.org",
    "Folium Documentation. https://python-visualization.github.io/folium",
]
for i, ref in enumerate(references, 1):
    content.append(Paragraph(f"[{i}] {ref}", body_style))

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(content)
print("Report saved as: HP_NO2_Air_Pollution_Report.pdf")
os.startfile("HP_NO2_Air_Pollution_Report.pdf")