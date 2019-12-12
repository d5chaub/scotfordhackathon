import pandas as pd
df = pd.read_csv('tags\V_2215_Bed_1_Temp_Bottom_deg_C.csv')
print(df.head())
print(df.columns)


df['SCTM:22DATAHCUCP4:TI22745A.PNT'] = pd.to_numeric(df['SCTM:22DATAHCUCP4:TI22745A.PNT'], errors='coerce')
data = df["SCTM:22DATAHCUCP4:TI22745A.PNT"].tolist()
#print(data)

def getKey(item):
    return item[0]

import rainflow
rfcycles=rainflow.count_cycles(data)
#print(sorted(rfcycles, key=getKey))
#print(rfcycles[25:])

# for low, high, mult in rainflow.extract_cycles(data[:50]):
#     mean = 0.5 * (high + low)
#     rng = high - low

#     print(mean)
#     print(rng)
#     print(high, low, mult)

#     print('hello world')

res = rainflow.count_cycles(data[:])
count = 0
for x in res:
    if x[0]>=250:
        count+=x[1]*20
    if x[0]<250 and x[0]>=195:
        count+=x[1]*12
    if x[0]<195 and x[0]>=140:
        count+=x[1]*8
    if x[0]<140 and x[0]>=83:
        count+=x[1]*4
    if x[0]<83 and x[0]>=56:
        count+=x[1]*2
    if x[0]<56 and x[0]>=28:
        count+=x[1]*1
    


print('temperature cycle count is')
print(count)

    #elif:
# res = [x[1]*20 for x in res if x[0]>=250]
# print(res)