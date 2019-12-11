import plotly.express as px
import pandas as pd 


df = pd.read_csv('V_2215_Bed_1_Temp_Bottom_deg_C.csv')
print(df.head())
print(df.columns)

vals = df.astype({'SCTM:22DATAHCUCP4:TI22745A.PNT' :'float'}, errors='ignore')

fig = px.scatter(x=df['timestamp'].tolist(), y =vals)
fig.show()