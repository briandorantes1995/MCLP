import pandas as pd
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import collections
from MCLP import df_copy, n, m, costumers, posiblelocations, maximumdistance, facilities, totalpopulationserved
from itertools import combinations
import warnings
warnings.filterwarnings("ignore")

time_start = time.perf_counter()


df_heuristic = df_copy.copy()
for i in range(m):
    for j in range(n):
        g = np.where(df_heuristic.iloc[i, j] <= maximumdistance, True, False)
        if g:
            df_heuristic.iloc[i, j] = 1
        else:
            df_heuristic.iloc[i, j] = 0


class localsearch():

    @staticmethod
    def initialPlot():
        print("*************************")
        print("Initial plot")
        plt.plot(costumers['X'].values.tolist(
        ), costumers['Y'].values.tolist(), 'r.', label='Demanded Nodes')
        plt.plot(posiblelocations['X'].values.tolist(
        ), posiblelocations['Y'].values.tolist(), 'b*', label='Available Facilities')
        plt.title('MCLP-Initial State')
        plt.legend(loc="upper left")
        plt.show()

    @staticmethod
    def finalPlot(value_info, title):
        plt.plot(costumers['X'].values.tolist(
        ), costumers['Y'].values.tolist(), 'r.', label='Demanded Nodes')
        plt.plot(posiblelocations.loc[list(value_info[0]), 'X'].values.tolist(), posiblelocations.loc[list(
            value_info[0]), 'Y'].values.tolist(), 'b*', label='Available Facilities')
        plt.title(title)
        plt.legend(loc="upper left")
        plt.show()

    @staticmethod
    def outputText(selectedlocations, totalcoverednodes, indexofnodes, totalpopulation):
        print("\nThe used locationes are :", selectedlocations)
        print("\nThere are "+str(totalcoverednodes)+" nodes covered\n")
        print('\nThis are the covered nodes: ', indexofnodes)
        print("\nThe covered population is :", totalpopulation)

    def firstFoundStrategy(self):
        print("*************************")
        print("First Found Strategy")
        global possibleChanges
        possibleChanges = self.choosePossibleChanges()
        max_value = max(possibleChanges["totalpopulation"])
        if max_value <= totalpopulationserved:
            print("First Found strategy can not provide a better solution")
            print("*************************")
            return

        first_found = []
        for x in range(len(possibleChanges)):
            if possibleChanges.iloc[x, 3] > totalpopulationserved:
                first_found = possibleChanges.iloc[x]
                break

        self.outputText(first_found[0], first_found[1],
                        first_found[2], first_found[3])
        self.finalPlot(first_found, "First Found Strategy")
        print("*************************")

    def bestFoundStrategy(self):
        print("*************************")
        print("Best Found Strategy")
        global posiblelocations
        possibleChanges = self.choosePossibleChanges()
        max_value = max(possibleChanges["totalpopulation"])
        if max_value <= totalpopulationserved:
            print("Best Found strategy can not provide a better solution")
            print("*************************")
            return

        max_value_index = possibleChanges["totalpopulation"].idxmax()
        max_value_info = possibleChanges.iloc[max_value_index]
        self.outputText(max_value_info[0], max_value_info[1],
                        max_value_info[2], max_value_info[3])
        self.finalPlot(max_value_info, "Best Found Strategy")
        print("*************************")

    @staticmethod
    def checkEachCombination(coords):
        df_coombination = df_heuristic.loc[coords]
        selectedlocations = list(df_coombination.index.values)
        df_coombination.loc['Total', :] = df_coombination.sum(axis=0)
        df_coombination[df_coombination.iloc[-1:] > 1] = 1

        Binary = df_coombination.loc['Total', :].values.tolist()
        costumers['Binary'] = Binary[:-1]
        totalcoverednodes = 0
        totalpopulation = 0
        for j in range(1, n):
            z = np.where(costumers.loc[j, 'Binary'] == 1, True, False)
            if z:
                totalcoverednodes += 1
                totalpopulation += costumers.loc[j, 'Demand']

        indexofnodes = costumers[costumers['Binary'] == 1].index.values
        return [selectedlocations, totalcoverednodes, indexofnodes, totalpopulation]

    def choosePossibleChanges(self):
        global combinations_list
        populationsandfactories = []
        combinations_list = list(combinations(
            df_heuristic.index.values, facilities))

        for x in combinations_list:
            selectedlocations, totalcoverednodes, indexofnodes, totalpopulation = self.checkEachCombination(
                list(x))
            if collections.Counter(list(df_heuristic.index.values)) == collections.Counter(selectedlocations):
                continue
            populationsandfactories.append(
                [selectedlocations, totalcoverednodes, indexofnodes, totalpopulation])

        possibleChanges = pd.DataFrame(data=populationsandfactories, columns=[
            "selectedlocations", "totalcoverednodes", "indexofnodes", "totalpopulation"])

        return possibleChanges


localClass = localsearch()
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

time_elapsed = (time.perf_counter() - time_start)
print(f"\n\nRuntime of the Heuristic is:{time_elapsed}")
