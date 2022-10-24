import pandas as pd
import sys
import time




instance = "inc50-1.csv"
instance2 = "inp50-1.csv"


time_start = time.perf_counter()
posiblelcoations = pd.read_csv(instance2)
info = list(posiblelcoations.columns)
n = int(info[0])
m = int(info[1])
posiblelcoations.rename(columns={info[0]: 'X', info[1]: 'Y'}, inplace=True)
posiblelcoations.index += 1
print(posiblelcoations)

costumers = pd.read_csv(instance,header=None)
costumers.rename(columns={0: 'X', 1: 'Y', 2: 'Demand'}, inplace=True)
costumers.index += 1
print(costumers)

