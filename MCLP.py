import pandas as pd
import sys
import time



if not sys.argv:
    instance = "in100-1.csv"
else:
    print("\nYou choose this instance:" + sys.argv[1])
    instance = str(sys.argv[1])

time_start = time.perf_counter()
df = pd.read_csv(instance)
print(df)
