import pandas as pd
import numpy as np
from queue import PriorityQueue


# class Connection:
#     def __init__(self, line, exit_time):
#         self.Line = line
#         self.exit_time = exit_time


class Line:

    def __init__(self, name, created):
        self.name = name
        self.totalTime = 0
        self.created = created

    def update_total_time(self, call_duration):
        self.totalTime = self.totalTime + call_duration


totalTime = 12 * 3600
currentTime = 0

callData = pd.DataFrame(
    columns=['callOrigin', 'interCallTime', 'callStartTime', 'callDuration', 'callEndTime', 'minEndTime', 'Line'])

originSwitch = np.random.uniform(-1, 1, 1000)
AtoB = np.random.uniform(0, 20, 1000)
BtoA = np.random.uniform(0, 24, 1000)
callDuration = np.random.uniform(0, 480, 1000)
index = 0
latestEndTime = 0
minEndTime = 100

while totalTime > latestEndTime:
    if originSwitch[index] < 0:
        callData.at[index, 'callOrigin'] = 'A'
        callData.at[index, 'interCallTime'] = AtoB[index]
    else:
        callData.at[index, 'callOrigin'] = 'B'
        callData.at[index, 'interCallTime'] = BtoA[index]

    if index == 0:
        callData.at[index, 'callStartTime'] = callData.loc[index]['interCallTime']
    else:
        callData.at[index, 'callStartTime'] = callData.loc[index - 1]['callStartTime'] + callData.loc[index][
            'interCallTime']
    callData.at[index, 'callDuration'] = callDuration[index]
    callData.at[index, 'callEndTime'] = callData.loc[index]['callStartTime'] + callData.loc[index]['callDuration']
    latestEndTime = latestEndTime + callData.loc[index]['callEndTime']
    if callData.loc[index]['callEndTime'] < minEndTime:
        minEndTime = callData.loc[index]['callEndTime']
    callData.at[index, 'minEndTime'] = minEndTime
    index = index + 1

pd.set_option("display.max_rows", None, "display.max_columns", None)
print(callData)
