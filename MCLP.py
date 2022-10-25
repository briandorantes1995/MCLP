import pandas as pd
import sys
import time
from sklearn.metrics.pairwise import euclidean_distances

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

maximumdistance = int(input("Enter the maximum distance in meters for the node to be covered(meters)"))
facilities = int(input("Enter the facilities to be placed in the available locations"))
# Compute distances 

dist2 = euclidean_distances(posiblelocations, costumerscoords)

# Convert back to dataframe.

df2 = pd.DataFrame( dist2, columns=costumers.index, index=posiblelocations.index)

# Start the heuristic
df2['coverednodes'] = df2[df2 >= maximumdistance].count(1)

# This does the sorting, by covered nodes(it maximizes the covered nodes)
df2.sort_values(by=['coverednodes'], ascending=False, inplace=True)

df2.to_csv("prueba.csv",index=False, header=False)
print(df2.head())