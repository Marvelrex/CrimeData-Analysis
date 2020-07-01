# -------------------------------------------------------
# Assignment 1
# Written by Jialin Yang ID:40069006
# For COMP 472 Section AB – Summer 2020
# --------------------------------------------------------
import math
import time
import statistics
import numpy as np
import matplotlib.pyplot as plt
import shapefile as shp
from matplotlib import patches
from matplotlib.ticker import MultipleLocator

# Read shapes and records from shape file
sf = shp.Reader("shape\crime_dt.shp", encoding='ISO-8859-1')
ShapeRecords = sf.shapeRecords()
Records = sf.records()
Shapes = sf.shapes()
Fields = sf.fields

# use list to store all points
crimelist = []
for x in range(len(Shapes)):
    crimelist.append(Shapes[x].points[0])
# Noticed there are lots of points are duplicate, so I made a dictionary to count all points in format {points: counts}
crimelist.sort()


def convert(list):
    return tuple(list)


dictcrime = {}
i = 0
while i < len(crimelist):
    nsame = crimelist.count(crimelist[i])
    dictcrime[convert(crimelist[i])] = nsame
    i += nsame
sumcrime = len(Records)
# User determine the grid size
print("Please enter the size of grid:(Recommend:0.003 or 0.002) ")
size = input()
size = float(size)
xNumb = 0.04 / size
yNumb = 0.04 / size
xNumb = math.ceil(xNumb)
yNumb = math.ceil(yNumb)
total = xNumb * yNumb
crimes = np.zeros([xNumb, yNumb])
# All info of this grid graph
print("The size of grid is " + str(size) + " with width = " + str(xNumb) + " and height = " + str(yNumb)
      + "total grids = " + str(total))
# Create grid graphs and set background color purple
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_title('CrimeData', fontsize=18)
ax.set_xlabel('xlabel', fontsize=10)
ax.set_ylabel('ylabel', fontsize=10)

ax.set_aspect('equal')
ax.minorticks_on()
ax.set_xlim(-73.59, -73.55)
ax.set_ylim(45.49, 45.53)
ax.xaxis.set_major_locator(MultipleLocator(size))
ax.yaxis.set_major_locator(MultipleLocator(size))
ax.xaxis.grid(True, which='major')
ax.yaxis.grid(True, which='major')
plt.grid(True, color='w', linestyle='-', linewidth=2)
plt.gca().patch.set_facecolor('#5d0573')
y1 = 45.490
x1 = -73.590
x2 = -73.590
y2 = 45.490

flag = False
# To read all points and count them to store to a 2-d list which are correspond to graph coordinates
for z in dictcrime:
    xcoor = z[0]
    ycoor = z[1]
    for x in range(1, int(xNumb) + 2):
        if flag:
            flag = False
            break
        xrange = round(x1 + x * size, 4)
        for y in range(1, int(yNumb) + 2):
            if xcoor > xrange:
                flag = False
                break
            yrange = round(y1 + y * size, 4)
            if (yrange - size) <= ycoor < yrange:
                crimes[x - 1][y - 1] += dictcrime[z]
                flag = True
                break
print(crimes)
# Show the info of each grid including coordinates and number of crime.
for row in range(xNumb):
    x2 += size
    y2 += size
    for col in range(yNumb):
        print("In the grid " + str(round(x2 - float(size), 4)) + "~" + str(round(x2, 4)) + "  " + str(
            round(y2 - float(size), 4)) + "~" + str(round(y2, 4)),
              ", Crimes are: " + str(crimes[row][col]))
# Make 2-d lists to single list and sorting them to a descending order.
crimedata = []
for t in range(0, xNumb):
    for r in crimes[t]:
        crimedata.append(r)
crimedata.sort()
crimedata.reverse()
print(crimedata)
# Give the statistics data of crime data including standard deviation,median and average
print("Standard Deviation of sample is % s " % (statistics.stdev(crimedata)))
print("Median of data-set is : % s " % (statistics.median(crimedata)))
print("Average of crime is : % s" % (statistics.mean(crimedata)))
# Allow user to input the threshold and change it.
print("Please input the threshold value: (Recommend 50 75 90) ")
threshold = input()
threshold = float(threshold) / 100
floor = math.floor(total * (1 - threshold))
print(str(floor) + " Blocks :" + str(crimedata[0:floor]) + "Are considered as blocks")


def get_key(val, dict):
    for key, value in dict.items():
        if val == value:
            return key
    return "Didn't exist"


def find(list1, crimerates):
    for row1 in range(xNumb):
        for col1 in range(yNumb):
            if list1[row1][col1] == crimerates:
                return [row1, col1]
    return "No results"


# Fill the blocks with yellow color
blocks = []
for plots in range(floor):
    x3, y3 = find(crimes, crimedata[plots])
    x3 = round(-73.59 + x3 * size, 4)
    y3 = round(45.49 + y3 * size, 4)
    x4 = round(x3 - size, 4)
    y4 = round(y3 - size, 4)
    blocks.append((x4, y4))  # Store Dangerous blocks to the list
    r1 = patches.Rectangle((x4, y4), size, size, color="#fcff30")
    ax.add_patch(r1)

# Allow user to input start point and goal point.
print("Please choose the area you would like to user! \nX coordinate:")
userx = input()
userx = float(userx)
print("Y coordinate: ")
usery = input()
usery = float(usery)
start = [userx, usery]
print("Please also choose your destination coordinates \nX coordinate:")
goalx = input()
goalx = float(goalx)
print("Y coordinate: ")
goaly = input()
goaly = float(goaly)
destination = [goalx, goaly]


# Heurostic Function= Current area's vertical distance + horizontal distance Each area has 5 directions if all area
# around it is safe but with different actual cost. Trying to make a better one, I will try to improve it before demo.
def search(start, destination):
    user = start
    goal = destination

    step = 0
    user[0] = float(user[0])
    user[1] = float(user[1])
    goal[0] = float(goal[0])
    goal[1] = float(goal[1])
    path = [user]
    fndict = {}
    fnlist = []

    while user[0] != goal[0] and user[1] != goal[1]:
        left = (round(user[0] - size, 4), round(user[1], 4))
        right = (round(user[0], 4), round(user[1], 4))

        if left in blocks and right in blocks:

            if len(fnlist) == 0:
                print("Due to blocks, no path is found.Please change the map and try again")
                quit(0)


        elif left in blocks and right not in blocks:
            gntop = 1.3
            hntop = ((goal[0] - user[0]) + (goal[1] - (user[1] + size))) / size

            fn = gntop + hntop
            nextarea = [user[0], user[1] + size]
            path.append(nextarea)
            user = nextarea
        elif right in blocks and left not in blocks:
            gntop = 1.3
            hntop = ((goal[0] - user[0]) + (goal[1] - (user[1] + size))) / size
            fn = gntop + hntop
            nextarea = [user[0], user[1] + size]
            path.append(nextarea)
            user = nextarea
        elif right not in blocks and left not in blocks:
            gnleft = 1
            hnleft = ((goal[0] - (user[0] - size)) + (goal[1] - (user[1]))) / size
            left = (round(user[0] - size, 4), user[1])
            fnleft = gnleft + hnleft - step

            gnright = 1
            hnright = ((goal[0] - (user[0] + size)) + (goal[1] - (user[1]))) / size
            right = (round(user[0] + size, 4), user[1])
            fnright = gnright + hnright - step

            gnlefttop = 1.5
            hnlefttop = ((goal[0] - (user[0] - size)) + (goal[1] - (user[1] + size))) / size
            lefttop = (round(user[0] - size, 4), round(user[1] + size, 4))
            fnlefttop = gnlefttop + hnlefttop - step

            gnrighttop = 1.5
            hnrighttop = ((goal[0] - (user[0] + size)) + (goal[1] - (user[1] + size))) / size
            righttop = (round(user[0] + size, 4), round(user[1] + size, 4))
            fnrighttop = gnrighttop + hnrighttop - step

            gntop = 1
            hntop = (((goal[0] - user[0]) + (goal[1] - (user[1] + size))) / size)
            top = (user[0], round(user[1] + size, 4))
            fntop = gntop + hntop - step

            leftli = (left, step)
            rightli = (right, step)
            topli = (top, step)
            righttopli = (righttop, step)
            lefttopli = (lefttop, step)

            fndict[leftli] = fnleft
            fndict[rightli] = fnright
            fndict[topli] = fntop
            fndict[righttopli] = fnrighttop
            fndict[lefttopli] = fnlefttop
            fnlist.extend([fnleft, fnright, fnlefttop, fnrighttop, fntop])
            fnlist.sort()

            lefttopleft = (round(lefttop[0] - size, 4), lefttop[1])

            if lefttop in blocks and top in blocks:
                fnlist.remove(fntop)
                fndict.pop(topli)
            if lefttop in blocks and lefttopleft in blocks:
                fnlist.remove(fnlefttop)
                fndict.pop(lefttopli)
            if righttop in blocks and top in blocks:
                fnlist.remove(fnrighttop)
                fndict.pop(righttopli)

            nextpoint = get_key(fnlist[0], fndict)
            path.append(nextpoint[0])
            user = nextpoint[0]
            fndict.pop(nextpoint)
            del fnlist[0]
            step += 1

    path.append(goal)
    return path


t0 = time.time()
paths = search(start, destination)
if time.time() - t0 > 10:
    print("Time Over. The optimal path is not found.")
else:
    print("Your search time is ", time.time() - t0, " seconds")
xs = []
ys = []
for pts in paths:
    xs.append(pts[0])
    print(pts[0])
    ys.append(pts[1])
plt.plot(xs, ys, '-')

plt.show()
