import geopandas as gpd
import pandas as pd
import plotly.express as px
import json


# Load Canada provinces/territories shapefile (cartographic boundary)
provinces = gpd.read_file('images/slide_why_flows/Alternative format/lcsd000a25a_e.shp')


# Load COVID-19 deaths data (CSV)
covid = pd.read_csv('images/slide_why_flows/COVID-19_Epidemiology_Update.csv')

# Sum deaths by province (exclude 'Canada' and 'Repatriated travellers')
df = covid[~covid['prname'].isin(['Canada', 'Repatriated travellers'])]
df = df.groupby('prname', as_index=False)['numdeaths'].sum()
df['prname'] = df['prname'].str.title()



# The shapefile's province name field may differ; inspect columns
name_col = [c for c in provinces.columns if 'name' in c.lower()][0]
provinces[name_col] = provinces[name_col].str.title()
gdf = provinces.merge(df, left_on=name_col, right_on='prname', how='left')

# Compute centroids for circles
gdf['centroid'] = gdf.geometry.centroid
gdf['lon'] = gdf.centroid.x
gdf['lat'] = gdf.centroid.y


# Plot base map (provinces polygons)
import plotly.graph_objects as go
fig = go.Figure()
# Remove non-polygon columns for geojson export
geojson_gdf = gdf.drop(columns=['centroid', 'lat', 'lon'], errors='ignore')
fig.add_trace(go.Choroplethmapbox(
    geojson=json.loads(geojson_gdf.to_json()),
    locations=gdf[name_col],
    z=[0]*len(gdf),
    featureidkey=f'properties.{name_col}',
    showscale=False,
    marker_opacity=0.2,
    marker_line_width=0.5
))
import os
fig.add_trace(go.Scattermapbox(
    lat=gdf['lat'],
    lon=gdf['lon'],
    mode='markers',
    marker=dict(
        size=gdf['numdeaths'].fillna(0).apply(lambda x: 8 + 0.08*x),
        color=gdf['numdeaths'],
        colorscale='Reds',
        showscale=True,
        sizemode='area',
        sizeref=2.*max(gdf['numdeaths'].fillna(0))/100**2,
        sizemin=8,
        opacity=0.8
    ),
    text=gdf[name_col],
    customdata=gdf[name_col],
    hovertemplate='<b>%{text}</b><br>Total deaths: %{marker.color}<br>Click for timeline<extra></extra>'
))

# Generate per-province weekly deaths timeline HTMLs
timeline_dir = 'images/slide_why_flows/province_timelines'
os.makedirs(timeline_dir, exist_ok=True)
covid['date'] = pd.to_datetime(covid['date'])
for pname in df['prname']:
    sub = covid[covid['prname'].str.title() == pname]
    weekly = sub.groupby(pd.Grouper(key='date', freq='W'))['numdeaths'].sum().reset_index()
    tfig = px.line(weekly, x='date', y='numdeaths', title=f'Weekly COVID-19 Deaths: {pname}', markers=True)
    tfig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=300)
    tfig.write_html(f'{timeline_dir}/{pname.replace(" ", "_")}_timeline.html', include_plotlyjs='cdn')
print(f'Per-province timelines written to {timeline_dir}/')
fig.update_layout(
    mapbox_style='carto-positron',
    mapbox_center={'lat': 56.1304, 'lon': -106.3468},
    mapbox_zoom=2.5,
    margin={"r":0,"t":0,"l":0,"b":0}
)
fig.write_html('images/slide_why_flows/COVID-19-Canada-deaths-interactive.html')
print('Done: images/slide_why_flows/COVID-19-Canada-deaths-interactive.html')
