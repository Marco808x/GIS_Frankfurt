GIS Frankfurt is a map of Frankfurt that shows the value of an area in a color between red and green based on the number of schools, trees, and transportation stations nearby.
First, the required data was collected from the sources. Then the data were cleaned up (including converting one coordination system to another, collect latitude and longitude for addresses, and more) and uploaded to a local SQL database.
The next step was to create a grid of geographical points over Frankfurt.
For each of these points a value was calculated based on the number of trees, schools and transport stations within a radius of 700 m:
Point value = number of trees inside the radius * (w)weight + number of schools inside the radius * (w) + number of transport stations inside the radius * (w)
After the calculation, the values ​​were scaled and uploaded to the SQL database.
In the last step, the values ​​were displayed together with the Frankfurt borders on a counter-map.

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


screenshot of interactive html_map:
![Bildschirmfoto 2021-04-15 um 17 56 06](https://user-images.githubusercontent.com/76050281/114900159-e5172a80-9e13-11eb-922e-96428ea02759.png)