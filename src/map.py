import pandas as pd
import geopandas as gp
import numpy as np
import folium 
import branca
from sqlalchemy import create_engine
from scipy.interpolate import griddata
import scipy as sp
import scipy.ndimage
import matplotlib.pyplot as plt
import geojsoncontour
from folium import plugins
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely import geometry
import gmplot
from shapely.geometry import shape

#
# read in data
#

uri = 'postgres://localhost/frankfurt'
engine = create_engine(uri, echo=False)

points_score = pd.read_sql("SELECT latitude, longitude, score FROM points_score;", engine)
districts = gp.read_file(
    "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/frankfurt-main.geojson"
    )
districts = districts.rename(columns={'name': 'District'})

#
# folium map
#

# Setup
value_mean = 3
debug     = False

# Setup style function
style_function = lambda x: {
    'weight': 0.0,
    'fillOpacity': 0.0
}

# Setup colormap
colors = ['#bf250d', '#bf630d', '#bf900d', '#b6bf0d', '#87bf0d', '#4bbf0d']
vmin = value_mean - 3
vmax = value_mean + 3
levels = len(colors)
cm     = branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax).to_step(levels)

# Data Preperation
x_orig = np.asarray(points_score['longitude'])
y_orig = np.asarray(points_score['latitude'])
z_orig = np.asarray(points_score['score'])

# Make a grid
x_arr          = np.linspace(np.min(x_orig), np.max(x_orig), 700)# 500
y_arr          = np.linspace(np.min(y_orig), np.max(y_orig), 700)# 500
x_mesh, y_mesh = np.meshgrid(x_arr, y_arr)

# Grid the values
z_mesh = griddata((x_orig, y_orig), z_orig, (x_mesh, y_mesh), method='linear')

# Gaussian filter the grid to make it smoother
sigma = [5, 5]
z_mesh = sp.ndimage.filters.gaussian_filter(z_mesh, sigma, mode='constant')

# Create the contour
contourf = plt.contourf(x_mesh, 
                        y_mesh, 
                        z_mesh, 
                        levels, 
                        alpha=0.2, 
                        colors=colors, 
                        linestyles='None', 
                        vmin=vmin, 
                        vmax=vmax)

# Convert matplotlib contourf to geojson
geojson = geojsoncontour.contourf_to_geojson(
    contourf=contourf,
    min_angle_deg=3.0,
    ndigits=5,
    stroke_width=1,
    fill_opacity=0.3)

frankfurt = folium.Map(location=[50.11516245279355, 8.68317637662434],    
                zoom_start=12,
                min_zoom = 10,
                width=800, height=500,
                control_scale=True,
                tiles='CartoDB positron')

# Add the contour plot 
folium.GeoJson(
    geojson,
    style_function=lambda x: {
        'color':     x['properties']['stroke'],
        'weight':    x['properties']['stroke-width'],
        'fillColor': x['properties']['fill'],
        'opacity':   0.3,
    }).add_to(frankfurt)

# Add the district borders
folium.features.Choropleth(
    geo_data = districts['geometry'],  
    name='chloropleth',
    data=districts,     
    columns=['District', 'cartodb_id'],  
    fill_color='Reds', 
    fill_opacity=0.0,         
    line_opacity=0.5,         
    
).add_to(frankfurt)

# Add tooltip
folium.GeoJson(
    districts,       
    style_function = style_function,   
    tooltip = folium.GeoJsonTooltip(    
        fields = ['District'],        
        localize = True
    
    )
).add_to(frankfurt)

# Add the colormap to the folium map
cm.caption = 'Area_Value'
frankfurt.add_child(cm)

# Fullscreen mode
plugins.Fullscreen(position='topright', force_separate_button=True).add_to(frankfurt)

# Plot the data
frankfurt.save('../frankfurt_map.html')
