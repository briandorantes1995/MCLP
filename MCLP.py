import pandas as pd
import sys
import time
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import matplotlib.pyplot as plt

# Initialize the plot
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots()

if not sys.argv:
    instance = "inc50-1.csv"
    instance2 = "inp50-1.csv"
else:
    print("\nYou choose this instance:" + sys.argv[1])
    instance = str(sys.argv[1])
    instance2 = str(sys.argv[2])

# Initialize the final results
totalcoverednodes = 0
totalpopulationserved = 0

# initialize time
time_start = time.perf_counter()
posiblelocations = pd.read_csv(instance2)
info = list(posiblelocations.columns)
n = int(info[0])
m = int(info[1])
posiblelocations.rename(columns={info[0]: 'X', info[1]: 'Y'}, inplace=True)
posiblelocations.index += 1


costumers = pd.read_csv(instance, header=None)
costumers.rename(columns={0: 'X', 1: 'Y', 2: 'Demand'}, inplace=True)
costumers.index += 1
costumerscoords = costumers[['X', 'Y']]

# Ask for constraints
maximumdistance = int(input("Enter the maximum distance in meters for the node to be covered(meters):"))
facilities = int(input("Enter how many facilities will be placed in the available locations(there are "+str(m)+" available):"))

# Compute distances

dist2 = euclidean_distances(posiblelocations, costumerscoords)

# Convert back to dataframe.

df = pd.DataFrame(dist2, columns=costumers.index, index=posiblelocations.index)

# Start the heuristic
df['coverednodes'] = df[df <= maximumdistance].count(1)

# This does the sorting, by covered nodes(it maximizes the covered nodes)
df.sort_values(by=['coverednodes'], ascending=False, inplace=True)

dfheuristic = df.iloc[:facilities]


# Initial Plot

plt.plot(costumers['X'].values.tolist(),
         costumers['Y'].values.tolist(), 'r.', label='Demanded Nodes')
plt.plot(posiblelocations['X'].values.tolist(
), posiblelocations['Y'].values.tolist(), 'b*', label='Available Facilities')
plt.title('MCLP-Initial State')
plt.legend(loc="upper left")
plt.show()

# Selected locations

selectedlocations = list(dfheuristic.index.values)

# Final Plot
plt.plot(costumers['X'].values.tolist(),
         costumers['Y'].values.tolist(), 'r.', label='Demanded Nodes')
plt.plot(posiblelocations.loc[selectedlocations, 'X'].values.tolist(
), posiblelocations.loc[selectedlocations, 'Y'].values.tolist(), 'b*', label='Selected Facilities')
plt.title('MCLP-Heuristic Result')
plt.legend(loc="upper left")
plt.show()

# Binary Path
for i in range(facilities):
    for j in range(n):
        g = np.where(dfheuristic.iloc[i, j] <= maximumdistance, True, False)
        if g:
            dfheuristic.iloc[i, j] = 1
        else:
            dfheuristic.iloc[i, j] = 0

dfheuristic.loc['Total', :] = dfheuristic.sum(axis=0)
dfheuristic[dfheuristic.iloc[-1:] > 1] = 1
Binary = dfheuristic.loc['Total', :].values.tolist()
Binary = Binary[:-1]
costumers['Binary'] = Binary



# Final Result of the heuristic
for j in range(1, n):
    z = np.where(costumers.loc[j, 'Binary'] == 1, True, False)
    if z:
        totalcoverednodes += 1
        totalpopulationserved += costumers.loc[j, 'Demand']

# Get the index of the node covered
indexofnodes = costumers[costumers['Binary'] == 1].index.values

# print all the results
print("\nThe used locations are :", selectedlocations)
print("\nThere are "+str(totalcoverednodes)+" nodes covered\n")
print('\nThis are the covered nodes: ', indexofnodes)
print("\nThe covered population is :", totalpopulationserved)

# print runtime
time_elapsed = (time.perf_counter() - time_start)
print(f"\n\nRuntime of the Heuristic is:{time_elapsed}")
