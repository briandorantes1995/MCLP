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

maximumdistance = input("Enter the maximum distance in meters for the node to be covered(meters)")
facilities = input("Enter the facilities to be placed in the available locations")
# Compute distances 

dist2 = euclidean_distances(posiblelocations, costumerscoords)

# Convert back to dataframe.

df2 = pd.DataFrame( dist2, columns=costumers.index, index=posiblelocations.index)

given_set = {maximumdistance}
df2['coverednodes'] = df2.isin(given_set).sum(1)
print(df2.head())