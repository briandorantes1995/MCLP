import pandas as pd
import sys
import time
from sklearn.metrics.pairwise import euclidean_distances



instance = "inc50-1.csv"
instance2 = "inp50-1.csv"


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


# Compute distances 

dist2 = euclidean_distances(posiblelocations, costumerscoords)

# Convert back to dataframe.

df2 = pd.DataFrame( dist2, columns=costumers.index, index=posiblelocations.index)
print(df2.head())


