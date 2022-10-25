import pandas as pd
import sys
import time
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

if not sys.argv:
    instance = "inc50-1.csv"
    instance2 = "inp50-1.csv"
else:
    print("\nYou choose this instance:" + sys.argv[1])
    instance = str(sys.argv[1])
    instance2 = str(sys.argv[2])


time_start = time.perf_counter()
posiblelocations = pd.read_csv(instance2)
info = list(posiblelocations.columns)
n = int(info[0])
m = int(info[1])
posiblelocations.rename(columns={info[0]: 'X', info[1]: 'Y'}, inplace=True)
posiblelocations.index += 1


costumers = pd.read_csv(instance,header=None)
costumers.rename(columns={0: 'X', 1: 'Y', 2: 'Demand'}, inplace=True)
costumers.index += 1
costumerscoords = costumers[['X','Y']]

# Ask for constraints
maximumdistance = int(input("Enter the maximum distance in meters for the node to be covered(meters)"))
facilities = int(input("Enter the facilities to be placed in the available locations"))

# Compute distances 

dist2 = euclidean_distances(posiblelocations, costumerscoords)

# Convert back to dataframe.

df = pd.DataFrame( dist2, columns=costumers.index, index=posiblelocations.index)

# Start the heuristic
df['coverednodes'] = df[df >= maximumdistance].count(1)

# This does the sorting, by covered nodes(it maximizes the covered nodes)
df.sort_values(by=['coverednodes'], ascending=False, inplace=True)

dfheuristic = df.iloc[:facilities]


# Selected locations
 
selectedlocations = list(dfheuristic.index.values)

  
# Binary Path
for i in range(facilities):
    for j in range(n):
        g = np.where(dfheuristic.iloc[i, j] >= maximumdistance, True, False)
        if g:
            dfheuristic.iloc[i, j] = 1
        else:
            dfheuristic.iloc[i, j] = 0
 
dfheuristic.loc['Total',:]= dfheuristic.sum(axis=0)
               
print(dfheuristic)