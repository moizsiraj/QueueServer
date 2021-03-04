import pandas as pd
import numpy as np
from queue import PriorityQueue
import matplotlib.pyplot as plt


class Line:

    def __init__(self, name, created):
        self.name = name
        self.totalTimeActive = 0
        self.created = created
        self.totalTime = 0
        self.efficiency = 0

    def update_total_time(self, call_duration):
        self.totalTimeActive = self.totalTimeActive + call_duration

    def calculate_total_time(self):
        self.totalTime = (12 * 3600) - self.created

    def calculate_efficiency(self):
        self.efficiency = (self.totalTimeActive / (12 * 3600)) * 100

    def __str__(self):
        string = str(self.name)
        return string


totalTime = 12 * 3600
currentTime = 0
lineVar = 'line-'
lineCount = 0

queue = PriorityQueue()

callData = pd.DataFrame(
    columns=['callOrigin', 'interCallTime', 'callStartTime', 'callDuration', 'callEndTime', 'Line'])

lines = pd.DataFrame(columns=['lines'])

originSwitch = np.random.uniform(-1, 1, 5000)
AtoB = np.random.uniform(0, 20, 5000)
BtoA = np.random.uniform(0, 24, 5000)
callDuration = np.random.uniform(0, 480, 5000)
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
    if latestEndTime < callData.loc[index]['callEndTime']:
        latestEndTime = callData.loc[index]['callEndTime']
    if index == 0:
        lineName = lineVar + str(lineCount)
        line = Line(lineName, callData.loc[index]['callStartTime'])
        line.update_total_time(callData.loc[index]['callDuration'])
        lines.at[lineCount, 'lines'] = line
        queue.put((callData.loc[index]['callEndTime'], line))
        callData.at[index, 'Line'] = line.name
    else:
        if queue.qsize() == 0:
            lineCount = lineCount + 1
            newLineName = lineVar + str(lineCount)
            newLine = Line(newLineName, callData.loc[index]['callStartTime'])
            newLine.update_total_time(callData.loc[index]['callDuration'])
            lines.at[lineCount, 'lines'] = newLine
            queue.put((callData.loc[index]['callEndTime'], newLine))
            callData.at[index, 'Line'] = newLine.name
        else:
            head = queue.get()
            exitTime = head[0]
            exitLine = head[1]
            if callData.loc[index]['callStartTime'] > exitTime:
                exitLine.update_total_time(callData.loc[index]['callDuration'])
                callData.at[index, 'Line'] = exitLine.name
                queue.put((callData.loc[index]['callEndTime'], exitLine))
            else:
                queue.put((exitTime, exitLine))
                lineCount = lineCount + 1
                newLineName = lineVar + str(lineCount)
                newLine = Line(newLineName, callData.loc[index]['callStartTime'])
                newLine.update_total_time(callData.loc[index]['callDuration'])
                lines.at[lineCount, 'lines'] = newLine
                queue.put((callData.loc[index]['callEndTime'], newLine))
                callData.at[index, 'Line'] = newLine.name
    index = index + 1

for i in range(lines.size):
    lines.loc[i, 'lines'].calculate_total_time()
    lines.loc[i, 'lines'].calculate_efficiency()
    lines.at[i, 'efficiency'] = lines.loc[i, 'lines'].efficiency
lines["efficiency"] = lines["efficiency"].astype(float)
pd.set_option("display.max_rows", None, "display.max_columns", None)
# print(callData)
print(lines)
lines.plot.bar(y="efficiency", color='blue')
plt.show()
