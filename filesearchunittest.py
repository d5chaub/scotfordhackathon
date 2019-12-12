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
    df.iloc[:,1] = pd.to_numeric(df.iloc[:,1], errors='coerce')
    data  = df.iloc[:,1].tolist()
    #print(data)

    for i in data:
        previous = data[data.index(i) -1]
        try:
            print("The current reading is " - + str(i)
            #i = float(i)
            #print(data[data.index(i) -1])
            if i > limit and data[data.index(i) -1]<2000:
                cyclecounter+=1
        except:
            pass

    print('For equipment {}'.format(file[:-4]))
    print('The current method cycle count is - ' + str(cyclecounter))
    print('The rainflow method cycle count is - NULL' + '')
    print('Total data entries - ' + str(len(data)))
    #print('Nan data entries - ' + str(errorcounter))