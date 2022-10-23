import pandas as pd
import sys
import time




instance = "in30-1.csv"


time_start = time.perf_counter()
df = pd.read_csv(instance,sep='\r')
    
print(df)