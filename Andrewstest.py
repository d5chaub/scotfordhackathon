import plotly.express as px
import pandas as pd 

print("STARTXYZ")
df = pd.read_csv('tags\GZ_3701_M1A_kPa.csv')

print(df.head())
#print(df.columns)

df['SCTM:PI37810'] = pd.to_numeric(df['SCTM:PI37810'], errors='coerce')

#count >200
limit = 2000
cyclecounter = 0

data = df['SCTM:PI37810'].tolist()

j = len(data)
i = 1
while i < j:
    if data[i] > limit:
        if data[i-1] < limit:
            cyclecounter = cyclecounter + 1
            #print("This is Cycle " + str(cyclecounter))
            #print(data[i-1])
            #print(data[i])

    i = i+1

print(j)
print(cyclecounter)



#for i in data:
    #print(i)


    #print("Pair")
    #if i > limit:
        #print(i)
        
        #try:
         #   if data[data.index(i)-1] < limit:
          #  if data[i-1] < limit:
           #     cyclecounter +=1
            #    print(data[i-1])
       # except:
           # print("end")

#scatter plot
#fig = px.scatter(x=df['timestamp'].tolist(), y =df['SCTM:PI37810'].tolist())
#fig.show()
#if data[data.index(i)-1] < limit: