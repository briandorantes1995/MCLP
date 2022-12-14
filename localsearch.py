import pandas as pd
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import collections
from MCLP import df_copy, n, m, costumers, posiblelocations, maximumdistance, facilities, totalpopulationserved, costumerscoords, selectedlocations, posiblelocationsX, posiblelocationsY

from itertools import combinations
import warnings
warnings.filterwarnings("ignore")

time_start = time.perf_counter()
df_binary = df_copy.copy()
originalCostumers = costumers.copy()
df_binary = df_binary[df_binary["coverednodes"] > 0]
for i in range(len(df_binary)):
    for j in range(n):
        g = np.where(df_binary.iloc[i, j] <= maximumdistance, True, False)
        if g:
            df_binary.iloc[i, j] = 1
        else:
            df_binary.iloc[i, j] = 0


class localsearch():

    @staticmethod
    def initialPlot():
        fig, ax = plt.subplots()
        ax.plot(originalCostumers['X'].values.tolist(),
                originalCostumers['Y'].values.tolist(), 'r.', label='Demanded Nodes')
        ax.plot(posiblelocations['X'].values.tolist(
        ), posiblelocations['Y'].values.tolist(), 'b*', label='Available Facilities')
        ax.plot(posiblelocations.loc[selectedlocations, 'X'].values.tolist(
        ), posiblelocations.loc[selectedlocations, 'Y'].values.tolist(), 'g*', label='Selected Facilities')

        for i, data in enumerate(zip(posiblelocationsX, posiblelocationsY)):

            j, k = data
            ax.add_patch(plt.Circle((j, k), maximumdistance,
                         color='green', alpha=0.5))

        ax.set_aspect('equal')
        ax.plot()
        plt.title('MCLP-Heuristic Result')
        plt.legend(loc="upper left")
        plt.show()

    @staticmethod
    def finalPlot(value_info, title):
        global aprueba
        aprueba = value_info
        fig, ax = plt.subplots()
        ax.plot(originalCostumers['X'].values.tolist(),
                originalCostumers['Y'].values.tolist(), 'r.', label='Demanded Nodes')
        ax.plot(posiblelocations['X'].values.tolist(
        ), posiblelocations['Y'].values.tolist(), 'b*', label='Available Facilities')
        ax.plot(posiblelocations.loc[list(value_info[0]), 'X'].values.tolist(), posiblelocations.loc[list(
            value_info[0]), 'Y'].values.tolist(), 'g*', label='Available Facilities')

        posiblelocationsX = posiblelocations.loc[list(
            value_info[0]), 'X'].values.tolist()
        posiblelocationsY = posiblelocations.loc[list(
            value_info[0]), 'Y'].values.tolist()
        for i, data in enumerate(zip(posiblelocationsX, posiblelocationsY)):

            j, k = data
            ax.add_patch(plt.Circle((j, k), maximumdistance,
                         color='green', alpha=0.5))

        ax.set_aspect('equal')
        ax.plot()

        # plt.plot(posiblelocations.loc[list(value_info[0]), 'X'].values.tolist(), posiblelocations.loc[list(
        #     value_info[0]), 'Y'].values.tolist(), 'b*', label='Available Facilities')
        plt.title(title)
        plt.legend(loc="upper left")
        plt.show()

    @staticmethod
    def outputText(selectedlocations, totalcoverednodes, indexofnodes, totalpopulation):
        print("\nThe used locationes are :", selectedlocations)
        print("\nThere are "+str(totalcoverednodes)+" nodes covered\n")
        print('\nThis are the covered nodes: ', indexofnodes)
        print("\nThe covered population is :",  totalpopulation)
        print("\nThe improvement is :", (totalpopulation /
              totalpopulationserved) * 100 - 100, "%")

    def firstFoundStrategy(self):
        print("*************************")
        print("First Found Strategy")
        possibleChanges = self.choosePossibleChanges()
        try:
            max_value = max(possibleChanges["totalpopulation"])
        except ValueError:
            max_value = 0

        if max_value <= totalpopulationserved:
            print("First Found strategy can not provide a better solution")
            time_elapsed = (time.perf_counter() - time_start)
            print(f"\n\nRuntime of the Heuristic is:{time_elapsed}")
            print("*************************")
            return

        first_found = []
        for x in range(len(possibleChanges)):
            if possibleChanges.iloc[x, 3] > totalpopulationserved:
                first_found = possibleChanges.iloc[x]
                break

        self.outputText(first_found[0], first_found[1],
                        first_found[2], first_found[3])
        time_elapsed = (time.perf_counter() - time_start)
        print(f"\n\nRuntime of the Heuristic is:{time_elapsed}")
        self.finalPlot(first_found, "First Found Strategy")

        print("*************************")

    def bestFoundStrategy(self):
        print("*************************")
        print("Best Found Strategy")
        possibleChanges = self.choosePossibleChanges()
        try:
            max_value = max(possibleChanges["totalpopulation"])
        except ValueError:
            max_value = 0
        if max_value <= totalpopulationserved:
            print("Best Found strategy can not provide a better solution")
            time_elapsed = (time.perf_counter() - time_start)
            print(f"\n\nRuntime of the Heuristic is:{time_elapsed}")
            print("*************************")
            return

        max_value_index = possibleChanges["totalpopulation"].idxmax()
        max_value_info = possibleChanges.iloc[max_value_index]
        self.outputText(max_value_info[0], max_value_info[1],
                        max_value_info[2], max_value_info[3])
        time_elapsed = (time.perf_counter() - time_start)
        print(f"\n\nRuntime of the Heuristic is:{time_elapsed}")
        self.finalPlot(max_value_info, "Best Found Strategy")

        print("*************************")

    @staticmethod
    def checkEachCombination(coords):
        global aprueba
        df_coombination = df_heuristic.loc[coords]
        df_coombination.loc['Total', :] = df_coombination.sum(axis=0)
        df_coombination[df_coombination.iloc[-1:] > 1] = 1

        Binary = df_coombination.loc['Total', :].values.tolist()
        costumers['Binary'] = Binary[:-1]
        totalcoverednodes = 0
        totalpopulation = 0
        for j in range(1, len(costumers.index)):
            z = np.where(costumers.loc[j, 'Binary'] == 1, True, False)
            if z:
                totalcoverednodes += 1
                totalpopulation += costumers.loc[j, 'Demand']

# Get the index of the node covered
        indexofnodes = costumers[costumers['Binary'] == 1].index.values

        return [coords, totalcoverednodes, indexofnodes, totalpopulation]

    def choosePossibleChanges(self):
        global possibleChanges
        global lastIndex
        global new_combination_list
        populationsandfactories = []
        combinations_list = list(combinations(
            df_heuristic.index.values, facilities))
        i = 0
        lastIndex = 0
        while (i < facilities):
            i = i + 1
            lastIndex = lastIndex + (len(df_heuristic.index) - i)

        new_combination_list = []
        for x in range(lastIndex):
            new_combination_list.append(combinations_list[x])

        for x in new_combination_list:
            selectedlocations, totalcoverednodes, indexofnodes, totalpopulation = self.checkEachCombination(
                list(x))

            populationsandfactories.append(
                [selectedlocations, totalcoverednodes, indexofnodes, totalpopulation])

        possibleChanges = pd.DataFrame(data=populationsandfactories, columns=[
            "selectedlocations", "totalcoverednodes",  "indexofnodes", "totalpopulation"])

        return possibleChanges


localClass = localsearch()
localClass.initialPlot()
if (len(df_binary) < facilities):
    print("localsearch can??t improve current solution")

df_heuristic = df_binary.copy()
for x in range(len(df_heuristic.columns)):
    if x == 0:
        continue
    if ((df_heuristic[x] == 0).all()):
        df_heuristic.drop(x, inplace=True, axis=1)
        costumers.drop(labels=[x], inplace=True, axis=0)


costumers.index = np.arange(1, len(costumers) + 1)
df_heuristic.columns = range(1, len(df_heuristic.columns)+1)
df_heuristic.rename(
    columns={int(len(df_heuristic.columns)): 'coverednodes'}, inplace=True)


exitOption = False
while exitOption == False:
    print("Local Search")
    print("1. First Found")
    print("2. Best Found")
    print("3. First and Best Found")
    print("4. Exit")
    option = int(input(
        "Choose an option \n 1. First Found 2. Best Found 3. First and Best Found 4. Exit"))

    if option == 1:
        localClass.firstFoundStrategy()
    elif option == 2:
        localClass.bestFoundStrategy()
    elif option == 3:
        localClass.firstFoundStrategy()
        localClass.bestFoundStrategy()
    else:
        exitOption = True
