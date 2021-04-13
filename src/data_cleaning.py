
import pandas as pd
import geopandas as gp
import numpy as np
import re
import os
import googlemaps
from dotenv import load_dotenv
from pyproj import CRS, Transformer
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, String, MetaData

#
# functions
#

def create_dataframe(latitude, longitude, category, detail):
    ''' df template '''
    df = pd.DataFrame({"latitude":latitude,
                       "longitude":longitude,
                       "category": category,
                       "detail": detail})
    return df

def get_single_points(list_of_coord):
    ''' get single points out of a polygon '''
    list_of_points = []
    for i in range(len(list_of_coord)):
        for coordinate in range(len(list_of_coord[0])):
            list_of_points.append(list_of_coord[i][coordinate])
    return list_of_points

def empty_table_for(table_name):
    ''' define an empty table of the object '''
    table = Table(table_name, metadata,
    Column('index', Integer),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('category', String),
    Column('detail', String)
    )
    return table

#
# read in data
#

trees = pd.read_csv("../data/raw_data/baumauswahl_veroffentlichung_8-berbeitetrkr.csv", delimiter=";")
rmv = pd.read_csv("../data/raw_data/RMV_Haltestellen.csv", delimiter=";")
schools = pd.read_excel("../data/raw_data/Liste der Schulen_1.xlsx")
grid = gp.read_file('../data/raw_data/grid.json')

#
# trees
#

# initialize transformer

crs_wgs84 = CRS.from_epsg(4326)       # epsg code for WGS84
crs_etrs89 = CRS.from_epsg(25832)     # epsg code for ETRS89
transformer = Transformer.from_crs(crs_etrs89, crs_wgs84, always_xy=True)

# prepare coordinates

heights = trees['HOCHWERT']
heights = [element.replace(",",".") for element in heights]

rights = trees['RECHTSWERT']
rights = [element.replace(",",".") for element in rights]

# etrs89 into wgs84

tree_long_lat = [transformer.transform(rights[i], heights[i]) for i in range(len(trees))]
tree_long = [long for long, lat in tree_long_lat]
tree_lat = [lat for long, lat in tree_long_lat]

print("tree preperation succesfull")

#
# transport Station
#

rmv_frankfurt = rmv[rmv['LANDKREIS']== "Stadt Frankfurt a.M"]
station_lat = [element.replace(",",".") for element in rmv_frankfurt['Y_WGS84']]
station_long = [element.replace(",",".") for element in rmv_frankfurt['X_WGS84']]

print("transport preperation succesfull")

#
# schools
#
 
schools = schools[schools['Stand 01.02.2021'].apply(lambda x: str(x).isdigit())]

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv('api_key'))

adresses = [f'{schools.iloc[i,3]} {schools.iloc[i,4]} {schools.iloc[i,5]}' for i in range(len(schools))]
geojson_schools = [gmaps.geocode(adress) for adress in adresses]  

regex_longitude = re.compile("'lng': (\d+.\d+)")
regex_latitude = re.compile("'lat': (\d+.\d+)")

school_long = [regex_longitude.findall(str(entry))[0] for entry in geojson_schools]
school_lat = [regex_latitude.findall(str(entry))[0] for entry in geojson_schools]

print("school preperation succesfull")

#
# grid
#

long_ar = []
lat_ar = []

for i in range(len(grid)):    
    x, y = grid['geometry'][i].exterior.coords.xy
    long_ar.append(x)
    lat_ar.append(y)

longitude = get_single_points(long_ar)
latitude = get_single_points(lat_ar)

print("grid preperation succesfull")

#
# create dataframes for upload
#

final_tree = create_dataframe( tree_lat
                              ,tree_long
                              ,'Tree'
                              ,trees['GEBIET'])

final_transport = create_dataframe( station_lat
                                   ,station_long
                                   ,"Transport Station"
                                   ,rmv_frankfurt['HST_NAME'])

final_school = create_dataframe( school_lat
                                ,school_long
                                ,"School"
                                ,schools["Unnamed: 2"])

grid_points = pd.DataFrame({"latitude":latitude,
                            "longitude":longitude})

print("dataframes are created")

#
# upload
#

uri = 'postgres://localhost/frankfurt'
engine = create_engine(uri, echo=False)
metadata = MetaData()

tree = empty_table_for('tree')
transport = empty_table_for('transport')
school = empty_table_for('school')
grid_point = Table('grid_points', metadata,
    Column('index', Integer),
    Column('latitude', Float),
    Column('longitude', Float)
    )

metadata.create_all(engine)

final_tree.to_sql('tree', engine, if_exists='append')
final_transport.to_sql('transport', engine, if_exists='append')
final_school.to_sql('school', engine, if_exists='append')
grid_points.to_sql('grid_points', engine, if_exists='append')

print("data are uploaded to sql db <frankfurt>")