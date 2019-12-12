import pandas as pd
df = pd.read_csv('tags\V_2215_Outlet_Pressure_MPa.csv')

print(df.head())
print(df.columns)


df['SCTM:22V15CP1:PI22498.PNT'] = pd.to_numeric(df['SCTM:22V15CP1:PI22498.PNT'], errors='coerce')
data = df["SCTM:22V15CP1:PI22498.PNT"].tolist()
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
    if x[0]>=3.2:
        count+=x[1]
    

print('pressure cycle count is')
print(count)

    #elif:
# res = [x[1]*20 for x in res if x[0]>=250]
# print(res)