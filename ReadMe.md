
Frankfurt map:
create a geographical information systems wich shows you the value of an area based on the number of schools, trees and transport stations in a radius of 500m.
A Grid of coordinationpoints was created only. 
This programm calculates a value for each coordinationpoints wich are spread over Frankfurt. For each of these points a scores gets calculated. To calculated the score all trees, schools and transport stations inside the radius (≈700m) of a point where counted. Based on these numbers a scores gets calculated for a point. The score gets later plotted with a color (red-green). 


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
   - https://github.com/codeforamerica/click_that_hood/blob/master/public/data/frankfurt-main.geojson

