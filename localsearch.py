import pandas as pd
import sys
import time
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import matplotlib.pyplot as plt
import collections
from MCLP import posiblelocations, n, costumerscoords, costumers, maximumdistance, facilities, totalpopulationserved
from itertools import combinations


dist2 = euclidean_distances(posiblelocations, costumerscoords)

# Convert back to dataframe.
df = pd.DataFrame(dist2, columns=costumers.index, index=posiblelocations.index)

df['coverednodes'] = df[df <= maximumdistance].count(1)
df.sort_values(by=['coverednodes'], ascending=False, inplace=True)
# This does the sorting, by covered nodes(it maximizes the covered nodes)

dfheuristic = df.iloc[:facilities]


def outputText(selectedlocations, totalcoverednodes, indexofnodes, totalpopulationserved):
    print("\nThe used locationes are :", selectedlocations)
    print("\nThere are "+str(totalcoverednodes)+" nodes covered\n")
    print('\nThis are the covered nodes: ', indexofnodes)
    print("\nThe covered population is :", totalpopulationserved)


def binary(x, y):
    dfheuristic = df.iloc[[x, y]]
    selectedlocations = list(dfheuristic.index.values)
    for i in range(facilities):
        for j in range(n):
            g = np.where(dfheuristic .iloc[i, j]
                         >= maximumdistance, True, False)
            if g:
                dfheuristic.iloc[i, j] = 1
            else:
                dfheuristic.iloc[i, j] = 0

    dfheuristic.loc['Total', :] = dfheuristic.sum(axis=0)
    dfheuristic[dfheuristic.iloc[-1:] > 1] = 1
    Binary = dfheuristic.loc['Total', :].values.tolist()
    Binary = Binary[:-1]
    costumers['Binary'] = Binary

    totalcoverednodes = 0
    totalpopulationserved = 0
    for j in range(1, n):
        z = np.where(costumers.loc[j, 'Binary'] == 1, True, False)
        if z:
            totalcoverednodes += 1
            totalpopulationserved += costumers.loc[j, 'Demand']

    # Get the index of the node covered
    indexofnodes = costumers[costumers['Binary'] == 1].index.values
    #outputText(selectedlocations, totalcoverednodes, indexofnodes,totalpopulationserved)
    return [selectedlocations, totalcoverednodes, indexofnodes, totalpopulationserved]


def choosePossibleChanges():
    populationsandfactories = []
    combinations_list = list(combinations(df.index.values, 2))

    for x in combinations_list:
        selectedlocations, totalcoverednodes, indexofnodes, totalpopulationserved = binary(
            x[0]-1, x[1]-1)
        if collections.Counter(list(dfheuristic.index.values)) == collections.Counter(selectedlocations):
            continue
        populationsandfactories.append(
            [selectedlocations, totalcoverednodes, indexofnodes, totalpopulationserved])

    possibleChanges = pd.DataFrame(data=populationsandfactories, columns=[
                                   "selectedlocations", "totalcoverednodes", "indexofnodes", "totalpopulationserved"])
    return possibleChanges


def firstFoundStrategy():
    print("*************************")
    print("First Found Strategy")
    possibleChanges = choosePossibleChanges()
    max_value = max(possibleChanges["totalpopulationserved"])
    if max_value <= totalpopulationserved:
        return "First Found strategy can not provide a better solution"

    first_found = []
    for x in range(len(possibleChanges)):
        if possibleChanges.iloc[x, 3] >= totalpopulationserved:
            first_found = possibleChanges.iloc[x]

    outputText(first_found[0], first_found[1], first_found[2], first_found[3])
    print("*************************")


def bestFoundStrategy():
    print("*************************")
    print("Best Found Strategy")
    possibleChanges = choosePossibleChanges()
    max_value = max(possibleChanges["totalpopulationserved"])
    if max_value <= totalpopulationserved:
        return "Best Found strategy can not provide a better solution"

    max_value_index = possibleChanges["totalpopulationserved"].idxmax()
    max_value_info = possibleChanges.iloc[max_value_index]
    outputText(max_value_info[0], max_value_info[1],
               max_value_info[2], max_value_info[3])
    print("*************************")


exitOption = False
while exitOption == False:
    print("Local Search")
    print("1. First Found")
    print("2. Best Found")
    print("3. First and Best Found")
    print("4. Exit")
    option = int(input("Choose an option"))

    if option == 1:
        firstFoundStrategy()
    elif option == 2:
        bestFoundStrategy()
    elif option == 3:
        firstFoundStrategy()
        bestFoundStrategy()
    else:
        exitOption = True
