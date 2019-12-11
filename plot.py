import plotly.express as px
import pandas as pd 


df = pd.read_csv('tags\V_2215_Bed_1_Temp_Bottom_deg_C.csv')
print(df.head())
print(df.columns)

df['SCTM:22DATAHCUCP4:TI22745A.PNT'] = pd.to_numeric(df['SCTM:22DATAHCUCP4:TI22745A.PNT'], errors='coerce')

fig = px.scatter(x=df['timestamp'].tolist(), y =df['SCTM:22DATAHCUCP4:TI22745A.PNT'].tolist())
fig.show()