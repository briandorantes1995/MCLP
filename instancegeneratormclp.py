# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 14:16:03 2022

@author: brian
"""

from numpy.random import seed
import time
import pandas as pd
import numpy as np


locations = int(input("How many locations will you have?"))
posiblelocations = int(round(0.10*locations))
minx = int(input("Enter min x:"))
maxx = int(input("Enter max x:"))
miny = int(input("Enter min y:"))
maxy = int(input("Enter max y:"))
minpopulation = int(input("Enter min population:"))
maxpopulation = int(input("Enter max population:"))
instances = int(input("How many instances will you generate?"))

time_start = time.perf_counter()
# Loop for generating n instances
for i in range(0, instances):
    np.random.seed(int(i))
    xposible = np.random.randint(minx, maxx, posiblelocations)
    xposible = np.insert(xposible, 0, locations)
    yposible = np.random.randint(miny, maxy, posiblelocations)
    yposible = np.insert(yposible, 0,posiblelocations )
    xposibles= pd.DataFrame(data=xposible)
    yposibles= pd.DataFrame(data=yposible)
    posiblelocationcoords = pd.concat([xposibles, yposibles], axis=1, sort=False)
    name = "inp" + str(locations) + "-" + str(i+1) + ".csv"
    posiblelocationcoords.to_csv(name, index=False, header=False)
    x = np.random.randint(minx, maxx, locations)
    y = np.random.randint(miny, maxy, locations)
    z = np.random.randint(minpopulation, maxpopulation, locations)
    xs = pd.DataFrame(data=x)
    ys = pd.DataFrame(data=y)
    zs = pd.DataFrame(data=z)
    df = pd.concat([xs, ys, zs], axis=1, sort=False)
    name2 = "inc" + str(locations) + "-" + str(i+1) + ".csv"
    df.to_csv(name2,index=False, header=False)


time_elapsed = (time.perf_counter() - time_start)
print(f"Runtime of the program is {time_elapsed}")
