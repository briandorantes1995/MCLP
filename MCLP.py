import pandas as pd
import sys
import time
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import matplotlib.pyplot as plt

# Initialize the plot
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

instance = ""
instance2 = ""
instances_quantity = int(
    input("Enter the number of instances 1)50 2)1000 3)10000 4)100000"))
if (instances_quantity) == 1:
    instance = "inc50-1.csv"
    instance2 = "inp50-1.csv"
elif (instances_quantity) == 2:
    instance = "inc1000-1.csv"
    instance2 = "inp1000-1.csv"
elif (instances_quantity) == 3:
    instance = "inc10000-1.csv"
    instance2 = "inp10000-1.csv"
elif (instances_quantity) == 4:
    instance = "inc100000-1.csv"
    instance2 = "inp100000-1.csv"
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

maximumdistance = int(
    input("Enter the maximum distance in meters for the node to be covered(meters)"))
facilities = int(input(
    "Enter how many facilities will be placed in the available locations(there are "+str(m)+" available facilities"))

# Compute distances

dist2 = euclidean_distances(posiblelocations, costumerscoords)

# Convert back to dataframe.

df = pd.DataFrame(dist2, columns=costumers.index, index=posiblelocations.index)

# Start the heuristic
df['coverednodes'] = df[df <= maximumdistance].count(1)

# This does the sorting, by covered nodes(it maximizes the covered nodes)
df.sort_values(by=['coverednodes'], ascending=False, inplace=True)

df_copy = df.copy()

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


posiblelocationsX = posiblelocations.loc[selectedlocations, 'X'].values.tolist(
)
posiblelocationsY = posiblelocations.loc[selectedlocations, 'Y'].values.tolist(
)


fig, ax = plt.subplots()
ax.plot(costumers['X'].values.tolist(),
        costumers['Y'].values.tolist(), 'r.', label='Demanded Nodes')
ax.plot(posiblelocations['X'].values.tolist(
), posiblelocations['Y'].values.tolist(), 'b*', label='Available Facilities')
ax.plot(posiblelocations.loc[selectedlocations, 'X'].values.tolist(
), posiblelocations.loc[selectedlocations, 'Y'].values.tolist(), 'g*', label='Selected Facilities')

for i, data in enumerate(zip(posiblelocationsX, posiblelocationsY)):

    j, k = data
    ax.add_patch(plt.Circle((j, k), maximumdistance, color='green', alpha=0.5))

ax.set_aspect('equal')
ax.plot()
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
