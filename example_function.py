import pandas as pd
from datetime import datetime
import numpy as np 

def my_logic(inputA, inputB):
    solution = inputA + inputB
    print("function us running")
    return solution

ans = my_logic(2,3)

print(ans)

start_date = datetime.strptime("01/11/2018", "%m/%d/%Y")
end_date = datetime.strptime("09/22/2018", "%m/%d/%Y")
#dates_range = pd.date_range(start_date, end_date).tolist()

#print(dates_range)
#df2 = df[(df2["datetime"] >= start_date) & (df["datetime"] <= end_date)]