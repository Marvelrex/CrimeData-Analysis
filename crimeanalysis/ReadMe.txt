This program import math,time,statistics, numpy,matplotlib and shapefile.

Read the shape file, I choose the relative path, so it might be reading problem, just change the path, if it is still not work you can contact marvelrex0725@gmail.com :) !


For the first input, you can choose the grid size, not limit to 0.003 or 0.002 and all points will be purple.. It will give differen size of grids. Then you can choose the threshold value, not limit to 50%, 75% or 90%.
And blocks will be covered by yellow. 

I create lots of data structure, so memory space wasted a lot. As the exchange, I made my program more effective. In the count of points part, if I used the 
brute force, there will be run 8 millions times which is n^3. Lots of points have the same coordinates, so I made a dictionary named dictcrime to store coordinates 
and counts. Then I dont have to count same points several times. To read all points, it only took less than 20000 times. I used three for loops with flag switch. Flag means
if this point is read correctly, if not it will run the loop again else next points will be in loops.