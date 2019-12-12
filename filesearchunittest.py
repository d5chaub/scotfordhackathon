from os import listdir
from os.path import isfile, join
import pandas as pd

errorcounter = 0
cyclecounter=0
limit = 2000

pt_indicator = 'Temp'

equipment = 'GZ-3701'
#equipment = 'V-2215'

mypath = 'tags/'
relfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) if f.endswith('.csv') and 
equipment.replace("-","_") in f]
print(relfiles)

for file in relfiles:
    df = pd.read_csv(mypath + file)
    print(df.head)

    data  = df.iloc[:,1].tolist()
    #print(data)

    for i in data:
        try:
            i = float(i)
            print(data[data.index(i) -1])
            if i > limit and data[data.index(i) -1]<2000:
                cyclecounter+=1
        except:
            pass
# Metal temperature differential oC	Factor
# <28	0
# 28 to 56	1
# 57 to 83	2
# 84 to 139	4
# 140 to 194	8
# 195 to 250	12
# >251	20

    print('For equipment {}'.format(file[:-4]))
    print('The current method cycle count is - ' + str(cyclecounter))
    print('The rainflow method cycle count is - NULL' + '')
    print('Total data entries - ' + str(len(data)))
    #print('Nan data entries - ' + str(errorcounter))