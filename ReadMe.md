
GIS Frankfurt is a map of Frankfurt wich shows the value of an area in a color between red and green, based on the number of schools, trees and transport stations are around. 
First of all, the required data was collected from the sides. Then the data get cleaned (includes converting one coordination system into an other, get the longitude and latitude for dresses and more) und were uploaded to a local sql databank. 
In the next step, a grid of geographic points over Frankfurt was created. 
For each of these points a value was calculated based on the number of trees, schools and transport station wich are inside a radius of 700m:
point value = tree*number inside a circle*wieght + …(schools)… + …(transport stations)…
After the calculation the values were scaled and uploaded into the sql db. 
In the last step the value were plotted in a counter map together with the borders of Frankfurt. 


data_cleaning:
  - read in data
  - cleaning process
  - upload to sql db

score_calculation:
   - calculate the score of each point

map.py:
  - create a html map

data source: 
   - government 
   - rmv 


![Bildschirmfoto 2021-04-15 um 17 56 06](https://user-images.githubusercontent.com/76050281/114900159-e5172a80-9e13-11eb-922e-96428ea02759.png)