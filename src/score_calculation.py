import pandas as pd
import geopandas as gp
import numpy as np
from shapely import geometry
from shapely.geometry import shape
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, MetaData

#
# functions
#

def make_shapely_points(df):
    ''' takes long and lat values from a def and returns 
        a list a of shapely geometry points'''
    shapely_points = [geometry.Point(df['latitude'][i], df['longitude'][i]) 
                      for i in range(len(df['latitude']))]
    return shapely_points

def number_of(object_location, points):
    ''' takes shapely geometry points and counts how often 
        the object is inside the radius of each point '''
    number_per_point = []
    for i in range(len(points)):
        l=[]
        for location in object_location:
            if points[i].distance(location) < 0.007:
                l.append(location)  
        number_per_point.append(len(l))
    return number_per_point

#
# read in data
#

uri = 'postgres://localhost/frankfurt'
engine = create_engine(uri, echo=False)

schools = pd.read_sql("SELECT latitude, longitude FROM school;", engine)
transport = pd.read_sql("SELECT latitude, longitude FROM transport;", engine)
trees = pd.read_sql("SELECT latitude, longitude FROM tree;", engine)
grid_points = pd.read_sql("SELECT latitude, longitude FROM grid_points;", engine)

print("data was read in")

#
# make shaply points out of long and lat
#

points = make_shapely_points(grid_points)
school_points = make_shapely_points(schools)
tree_points = make_shapely_points(trees)
transport_points = make_shapely_points(transport)

print("made shapelypoints")

#
# make the score
#

number_school = number_of(school_points, points)
number_tree = number_of(tree_points, points)
number_transport = number_of(transport_points, points)

list_score = [(number_school[i]*70)+(number_transport[i]*100)+(number_tree[i]*30) 
              for i in range(len(number_school))]

scale = np.frompyfunc(lambda x, min, max: (x - min) / (max - min), 3, 1)
scores = [scale(score, 0, 6) for score in list_score]
grid_points['score'] = scores

print("score is calculated")

#
# upload
#

metadata = MetaData()

points_score = Table('points_score', metadata,
    Column('index', Integer),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('score', Float),
)
metadata.create_all(engine)
grid_points.to_sql('points_score', engine, if_exists='append')

print("and uploaded to <frankfurt>")