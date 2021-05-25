GIS Frankfurt is a map of Frankfurt that shows the value of an area in a color between red and green. The more schools, trees, and transport stations nearby, the better the area.
 
 
data_preprocess:
  - pre-process data
  - upload to sql db

score_calculation:
   - counts schools trees and transport stations inside a radius of 700m
   - calculate score, based on the counting

map.py:
  - creates an html map

data source: 
   - government 
   - rmv 


screenshot of interactive html_map:
![Bildschirmfoto 2021-04-15 um 17 56 06](https://user-images.githubusercontent.com/76050281/114900159-e5172a80-9e13-11eb-922e-96428ea02759.png)
