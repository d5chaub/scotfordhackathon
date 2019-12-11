# useage example
# myPi=PiPython(pi_server='UPPICOLL')
# Get raw data
# myRawData = myPi.get_raw_data('UK:SW:FICA12251.OP','2018-08-11 00:00','2018-08-12 06:00')
# Get data @ 5m intervals and pivot the results so tags are columns
# myData = myPi.get_data('UK:SW:FICA12251.OP', '2018-08-11 00:00', '2018-08-12 06:00','5m', pivot='Y')
# myData.to_csv('C:\Apps\result.csv')
import time
import argparse
import pandas as pd
from datetime import datetime
#from datetime import timedelta
from win32com.client.dynamic import Dispatch

import re
import os

class PiPython(object):
    # btInside  = All the values equal or after the start time and equal or before the end time
    # btOutside The first value older than or equal to the start time through the first value newer than or equal to the end time
    # btInterp The value on, or first value older, than start time through a value on the end time, or first value newer than the end time.
    # btAuto Same as btInterp
    BTconstants = {'btInside': 0, 'btOutside': 1, 'btInterp': 2, 'btAuto': 3
                   }

    def __init__(self, pi_server='UPPICOLL'):
        try:
            self.pi_srv = Dispatch('PISDK.PISDK').Servers(pi_server)
            self.pi_timeformat = Dispatch('PITimeServer.PITimeFormat')
            print('PI Server set to', pi_server)
        except:
            raise

    def search_initial_dates(self, tags, t_start, pivot='n'):
        print('Getting raw data...')
        self.pivot = pivot.upper()
        list_of_values = []
        if type(tags) == str:
            tags = [tags]
        elif type(tags) != list:
            raise TypeError("input must be a string or a list")
        for tag in tags:
            if self.is_valid_tag(tag):
                df = self.__get_raw_data_item(tag, t_start, str(
                    pd.to_datetime(t_start) + pd.DateOffset(years=1)))
                df = df[~df.index.duplicated()]
                if self.pivot == 'N':
                    df.insert(0, 'tag', tag)
                    df.columns.values[1] = "value"
                try:
                    if df["value"][0] == 'Pt Created':
                        list_of_values.append(df.head(1))
                except KeyError:
                    pass
            else:
                print(tag, 'does not appear to be a valid tag - skipping')
        if len(list_of_values) == 0:
            print('** Warning ** Dataframe is empty')
        else:
            print('Data retrieved for', len(list_of_values), 'tags')
        if self.pivot == 'N':
            try:
                return pd.concat(list_of_values)
            except ValueError:
                pass

    def get_data(self, tags, t_start, t_end, t_interval, pivot='N'):
        print('Getting data...')
        self.pivot = pivot.upper()
        list_of_values = []
        if type(tags) == str:
            tags = [tags]
        elif type(tags) != list:
            raise TypeError("input must be a string or a list")
        for tag in tags:
            if self.is_valid_tag(tag):
                df = self.__get_data_item(tag, t_start, t_end, t_interval)
                df = df[~df.index.duplicated()]
                if self.pivot == 'N':
                    df.insert(0, 'tag', tag)
                    df.columns.values[1] = "value"
                list_of_values.append(df)
            else:
                print(tag, 'does not appear to be a valid tag - skipping')
        if len(list_of_values) == 0:
            print('** Warning ** Dataframe is empty')
        else:
            print('Data retrieved for', len(list_of_values), 'tags')
        if self.pivot == 'N':
            return pd.concat(list_of_values)
        else:
            return pd.DataFrame().join(list_of_values, how='outer')

    def get_raw_data(self, tags, t_start, t_end, pivot='n'):
        print('Getting raw data...')
        self.pivot = pivot.upper()
        list_of_values = []
        if type(tags) == str:
            tags = [tags]
        elif type(tags) != list:
            raise TypeError("input must be a string or a list")
        for tag in tags:
            if self.is_valid_tag(tag):
                df = self.__get_raw_data_item(tag, t_start, t_end)
                df = df[~df.index.duplicated()]
                if self.pivot == 'N':
                    df.insert(0, 'tag', tag)
                    df.columns.values[1] = "value"
                list_of_values.append(df)
            else:
                print(tag, 'does not appear to be a valid tag - skipping')
        if len(list_of_values) == 0:
            print('** Warning ** Dataframe is empty')
        else:
            print('Data retrieved for', len(list_of_values), 'tags')
        if self.pivot == 'N':
            return pd.concat(list_of_values)
        else:
            return pd.DataFrame().join(list_of_values, how='outer')

    def get_snapshot(self, tags):
        if type(tags) == str:
            tags = [tags]
        elif type(tags) != list:
            raise TypeError("input must be a string or a list")
        list_of_datetimes = []
        list_of_values = []
        for tag in tags:
            datetime, value = self.__get_snapshot_item(tag)

            list_of_datetimes.append(datetime)
            list_of_values.append(value)

        return pd.DataFrame({'datetime': list_of_datetimes, 'tag': tags, 'value': list_of_values})

    def __get_data_item(self, tag_name, t_start, t_end, t_interval):
        try:
            tag = self.pi_srv.PIPoints(tag_name)
            pi_values = tag.Data.InterpolatedValues2(
                t_start, t_end, t_interval, asynchStatus=None)
            return (self.pivalues_to_df(pi_values, tag_name))
            #   return pd.Dataframe()
        except:
            raise

    def __get_raw_data_item(self, tag_name, t_start, t_end):
        try:
            tag = self.pi_srv.PIPoints(tag_name)
            pi_values = tag.Data.RecordedValues(
                t_start, t_end, self.BTconstants['btInside'], asynchStatus=None)
            return (self.pivalues_to_df(pi_values, tag_name))
        except:
            raise

    def __get_snapshot_item(self, tag_name):
        try:
            tag = self.pi_srv.PIPoints(tag_name)
            list_of_datetimes, list_of_values = self.pivalues_to_list(
                [tag.Data.Snapshot])
            return list_of_datetimes[0], list_of_values[0]
        except:
            raise

    def is_valid_tag(self, tag_name):
        try:
            self.pi_srv.PIPoints(tag_name)
            return True
        except:
            return False

    def pivalues_to_list(self, pivalues):
        list_of_values = []
        list_of_datetimes = []
        for v in pivalues:
            try:
                list_of_values.append(float(v.Value))
                list_of_datetimes.append(datetime.fromtimestamp(v.TimeStamp))
            except:
                try:
                    list_of_values.append(str(v.Value))
                    list_of_datetimes.append(
                        datetime.fromtimestamp(v.TimeStamp))
                except:
                    pass
        return list_of_datetimes, list_of_values

    def pivalues_to_df(self, pivalues, col_name='value'):
        list_of_datetimes, list_of_values = self.pivalues_to_list(pivalues)
        df = pd.DataFrame(
            {'timestamp': list_of_datetimes, col_name: list_of_values})
        return df.set_index('timestamp')

    def timeformat(self, arg):
        try:
            self.pi_timeformat.InputString = arg
            return self.pi_timeformat.OutputString
        except:
            raise


myPi = PiPython(pi_server='DSAMPICOLL')
#params
#list of tags
#start datetime
#end datetime
#interval
#always pivot

df = pd.read_csv("problem1_data_dictionary.csv")

tag_list = ["SCTM:" + i for i in df["Tag"].tolist()]

namelist = [i.replace(" ", "_") + "_"  + j for i,j in zip(df["Description"].tolist(),df["Units"].tolist())]

print(tag_list)
print(len(tag_list))
for i in tag_list:
    with open("fetchlog.txt", "a") as fl:
        print(i)
        csvname = "singletags/" + namelist[tag_list.index(i)].replace("-","_") + ".csv"
        print(csvname)
        try:
            if not os.path.exists(csvname):
                myData = myPi.get_data(
                    [i],
                    '2017-01-01 00:00',
                    '2019-12-03 00:00', '5m', pivot='Y')
                print(myData.head())
                myData.to_csv(csvname)
            else:
                print(i + " csv already exists.")
        except:
            fl.write("failed to retrieve {}\n {}\n".format(i, i))

