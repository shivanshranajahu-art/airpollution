from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# ----------------------------------------
# Document Setup
# ----------------------------------------
doc = SimpleDocTemplate(
    "NO2_Air_Pollution_Report.pdf",
    pagesize=A4,
    rightMargin=60,
    leftMargin=60,
    topMargin=60,
    bottomMargin=60
)

styles = getSampleStyleSheet()
content = []

# ----------------------------------------
# Custom Styles
# ----------------------------------------
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=20,
    textColor=colors.HexColor('#1a237e'),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor('#37474f'),
    spaceAfter=4,
    alignment=TA_CENTER
)

heading_style = ParagraphStyle(
    'Heading',
    parent=styles['Heading1'],
    fontSize=14,
    textColor=colors.HexColor('#1a237e'),
    spaceBefore=16,
    spaceAfter=6,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=11,
    textColor=colors.HexColor('#212121'),
    spaceAfter=6,
    leading=16,
    alignment=TA_JUSTIFY
)

# ----------------------------------------
# TITLE PAGE
# ----------------------------------------
content.append(Spacer(1, 0.5*inch))
content.append(Paragraph("Air Pollution Analysis Using Satellite Data", title_style))
content.append(Paragraph("Nitrogen Dioxide (NO₂) Study over India", title_style))
content.append(Spacer(1, 0.2*inch))
content.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a237e')))
content.append(Spacer(1, 0.2*inch))

content.append(Paragraph("Using Sentinel-5P Satellite Data on Google Earth Engine", subtitle_style))
content.append(Paragraph("Dataset: COPERNICUS/S5P/OFFL/L3_NO2", subtitle_style))
content.append(Paragraph("Region: India | Period: 2023 - 2024", subtitle_style))
content.append(Spacer(1, 0.2*inch))
content.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
content.append(Spacer(1, 0.3*inch))

# Student Info Table
student_data = [
    ['Field', 'Details'],
    ['Student Name', 'Your Name Here'],
    ['Roll Number', 'Your Roll Number'],
    ['Course', 'Your Course Name'],
    ['Institution', 'Your College Name'],
    ['Submitted To', 'Your Teacher Name'],
    ['Year', '2024-2025'],
]

student_table = Table(student_data, colWidths=[2.2*inch, 3.8*inch])
student_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8eaf6')),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 1), (-1, -1), 11),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1),
     [colors.white, colors.HexColor('#e8eaf6')]),
    ('PADDING', (0, 0), (-1, -1), 8),
]))
content.append(student_table)
content.append(Spacer(1, 0.3*inch))

# ----------------------------------------
# SECTION 1 - Introduction
# ----------------------------------------
content.append(Paragraph("1. Introduction", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))
content.append(Paragraph(
    "Air pollution is one of the most critical environmental challenges facing the world today. "
    "Nitrogen Dioxide (NO₂) is a harmful gas primarily produced by vehicle emissions, industrial "
    "activities, and power plants. Prolonged exposure to NO₂ causes respiratory diseases, "
    "cardiovascular problems, and contributes to the formation of acid rain and smog.",
    body_style))
content.append(Paragraph(
    "This project analyzes the spatial and temporal distribution of NO₂ pollution over India "
    "using satellite data from the Sentinel-5P satellite, processed on Google Earth Engine (GEE). "
    "The study compares NO₂ levels for the years 2023 and 2024 to identify pollution trends "
    "across different seasons and regions of India.",
    body_style))

# ----------------------------------------
# SECTION 2 - Objectives
# ----------------------------------------
content.append(Paragraph("2. Objectives", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))

objectives = [
    "To analyze the spatial distribution of NO₂ pollution over India using satellite data.",
    "To perform temporal comparison of NO₂ levels between 2023 and 2024.",
    "To identify high pollution hotspots across different regions of India.",
    "To study seasonal variations in NO₂ concentration.",
    "To visualize pollution data using interactive maps and statistical graphs.",
]
for i, obj in enumerate(objectives, 1):
    content.append(Paragraph(f"  {i}. {obj}", body_style))

# ----------------------------------------
# SECTION 3 - Tools and Dataset
# ----------------------------------------
content.append(Paragraph("3. Tools and Dataset Used", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))

tools_data = [
    ['Tool / Dataset', 'Purpose'],
    ['Google Earth Engine (GEE)', 'Cloud-based satellite data processing'],
    ['Sentinel-5P (TROPOMI)', 'NO₂ satellite data source'],
    ['COPERNICUS/S5P/OFFL/L3_NO2', 'Exact GEE dataset used'],
    ['Python 3.x', 'Programming language'],
    ['earthengine-api', 'Python API for GEE'],
    ['Folium', 'Interactive map visualization'],
    ['Matplotlib', 'Graph and chart generation'],
    ['ReportLab', 'PDF report generation'],
    ['PyCharm IDE', 'Development environment'],
]

tools_table = Table(tools_data, colWidths=[3*inch, 3*inch])
tools_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1),
     [colors.white, colors.HexColor('#e8eaf6')]),
    ('PADDING', (0, 0), (-1, -1), 7),
]))
content.append(tools_table)

# ----------------------------------------
# SECTION 4 - Methodology
# ----------------------------------------
content.append(Paragraph("4. Methodology", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))
content.append(Paragraph(
    "The methodology followed in this project involves the following steps:",
    body_style))

steps = [
    "Account Setup: Created a Google Earth Engine account and authenticated the Python API.",
    "Data Collection: Accessed Sentinel-5P NO₂ data from GEE data catalog.",
    "Data Filtering: Filtered data by date range (2023 and 2024) and geographic boundary (India).",
    "Data Processing: Computed monthly and annual mean NO₂ values using GEE reducers.",
    "Visualization: Generated interactive maps using Folium and statistical charts using Matplotlib.",
    "Analysis: Compared 2023 vs 2024 NO₂ levels across months and seasons.",
    "Report Generation: Compiled all results into this professional PDF report.",
]
for i, step in enumerate(steps, 1):
    content.append(Paragraph(f"  Step {i}: {step}", body_style))

# ----------------------------------------
# SECTION 5 - Results (Graphs)
# ----------------------------------------
content.append(Paragraph("5. Results and Analysis", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))

# Insert graphs if they exist
graphs = [
    ('no2_line_chart.png', 'Figure 1: Monthly NO₂ Trend - 2023 vs 2024'),
    ('no2_bar_chart.png',  'Figure 2: Monthly NO₂ Bar Comparison'),
    ('no2_seasonal_chart.png', 'Figure 3: Seasonal NO₂ Analysis'),
    ('no2_annual_chart.png', 'Figure 4: Annual Average NO₂ Comparison'),
]

for img_file, caption in graphs:
    if os.path.exists(img_file):
        content.append(Paragraph(caption, subtitle_style))
        content.append(Image(img_file, width=5.5*inch, height=3*inch))
        content.append(Spacer(1, 0.2*inch))
    else:
        content.append(Paragraph(
            f"⚠ {caption} - Image not found. Run no2_graphs.py first.",
            body_style))

# ----------------------------------------
# SECTION 6 - Conclusion
# ----------------------------------------
content.append(Paragraph("6. Conclusion", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))
content.append(Paragraph(
    "This project successfully demonstrated the use of Google Earth Engine and Sentinel-5P "
    "satellite data for analyzing air pollution (NO₂) over India. The interactive maps clearly "
    "show pollution hotspots in industrial and urban regions of India, particularly in states "
    "like Uttar Pradesh, Maharashtra, and West Bengal.",
    body_style))
content.append(Paragraph(
    "The temporal analysis revealed seasonal patterns in NO₂ levels, with higher concentrations "
    "observed during winter months due to temperature inversions that trap pollutants near the "
    "surface. The comparison between 2023 and 2024 provides valuable insights into pollution "
    "trends and the effectiveness of environmental policies.",
    body_style))
content.append(Paragraph(
    "Google Earth Engine proved to be an extremely powerful and accessible platform for "
    "large-scale environmental analysis, enabling processing of petabytes of satellite data "
    "without requiring local computational resources.",
    body_style))

# ----------------------------------------
# SECTION 7 - References
# ----------------------------------------
content.append(Paragraph("7. References", heading_style))
content.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
content.append(Spacer(1, 0.1*inch))

references = [
    "Google Earth Engine. (2024). Earth Engine Data Catalog. https://developers.google.com/earth-engine/datasets",
    "European Space Agency. (2024). Sentinel-5P TROPOMI. https://sentinel.esa.int/web/sentinel/missions/sentinel-5p",
    "Copernicus. (2024). NO₂ Tropospheric Column. COPERNICUS/S5P/OFFL/L3_NO2",
    "Python Software Foundation. (2024). Python 3.x Documentation. https://docs.python.org",
    "Geemap Documentation. https://geemap.org",
    "Folium Documentation. https://python-visualization.github.io/folium",
]
for i, ref in enumerate(references, 1):
    content.append(Paragraph(f"[{i}] {ref}", body_style))

# ----------------------------------------
# Build PDF
# ----------------------------------------
doc.build(content)
print("✓ Report saved as: NO2_Air_Pollution_Report.pdf")
os.startfile("NO2_Air_Pollution_Report.pdf")