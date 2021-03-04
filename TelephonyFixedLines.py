import pandas as pd
import numpy as np
from queue import PriorityQueue
import matplotlib.pyplot as plt

number_of_lines = 25
number_of_calls_blocked = 0
number_of_calls_A = 0
number_of_calls_B = 0


class Line:

    def __init__(self, name, created):
        self.name = name
        self.totalTimeActive = 0
        self.created = created
        self.totalTime = 0
        self.efficiency = 0

    def update_total_time_active(self, call_duration):
        self.totalTimeActive = self.totalTimeActive + call_duration

    def calculate_total_time(self):
        self.totalTime = (12 * 3600) - self.created

    def calculate_efficiency(self):
        self.efficiency = (self.totalTimeActive / (12 * 3600)) * 100

    def __str__(self):
        string = str(self.name)
        return string

    def __lt__(self, other):
        return self.name < other.name

    # return comparison
    def __le__(self, other):
        return self.name < other.name


lines = pd.DataFrame(columns=['lines'])
lineVar = 'line-'
queue = PriorityQueue()

for i in range(0, number_of_lines):
    lineName = lineVar + str(i)
    line = Line(lineName, 0)
    lines.at[i, 'lines'] = line
    queue.put((0, line))

totalTime = 12 * 3600
currentTime = 0

callData = pd.DataFrame(
    columns=['callOrigin', 'interCallTime', 'callStartTime', 'callDuration', 'callEndTime', 'Line', 'No of Lines Busy'])

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
        number_of_calls_A = number_of_calls_A + 1
    else:
        callData.at[index, 'callOrigin'] = 'B'
        callData.at[index, 'interCallTime'] = BtoA[index]
        number_of_calls_B = number_of_calls_B + 1

    if index == 0:
        callData.at[index, 'callStartTime'] = callData.loc[index]['interCallTime']
    else:
        callData.at[index, 'callStartTime'] = callData.loc[index - 1]['callStartTime'] + callData.loc[index][
            'interCallTime']
    callData.at[index, 'callDuration'] = callDuration[index]
    callData.at[index, 'callEndTime'] = callData.loc[index]['callStartTime'] + callData.loc[index]['callDuration']
    if latestEndTime < callData.loc[index]['callEndTime']:
        latestEndTime = callData.loc[index]['callEndTime']

    # assigning Line
    head = queue.get()
    exitTime = head[0]
    exitLine = head[1]

    if callData.loc[index]['callStartTime'] > exitTime:
        callData.at[index, 'No of Lines Busy'] = 0
        for i in range(0, queue.qsize()):
            if callData.loc[index]['callStartTime'] > queue.queue[i][0]:
                callData.at[index, 'No of Lines Busy'] = callData.loc[index]['No of Lines Busy'] + 1
        callData.at[index, 'No of Lines Busy'] = number_of_lines - callData.loc[index]['No of Lines Busy']
        exitLine.update_total_time_active(callData.loc[index]['callDuration'])
        callData.at[index, 'Line'] = exitLine.name
        queue.put((callData.loc[index]['callEndTime'], exitLine))
    else:
        callData.at[index, 'No of Lines Busy'] = number_of_lines
        number_of_calls_blocked = number_of_calls_blocked + 1
        queue.put((exitTime, exitLine))
    index = index + 1

for i in range(lines.size):
    lines.at[i, 'total time'] = lines.loc[i]['lines'].totalTimeActive
    lines.loc[i]['lines'].calculate_efficiency()
    lines.at[i, 'efficiency'] = lines.loc[i]['lines'].efficiency

lines["efficiency"] = lines["efficiency"].astype(float)
pd.set_option("display.max_rows", None, "display.max_columns", None)
# print(callData)

f = open("outputFixedLines.txt", "w")

time_avg_number_of_lines_busy = (callData['No of Lines Busy'].sum() / index)
time_avg_proportion_of_lines_busy = (lines['total time'].sum() / (12 * 3600))

f.write('Number of lines: ' + str(number_of_lines) + '\n')
f.write('Number of calls: ' + str(index) + '\n')
f.write("Number of calls attempted from A: " + str(number_of_calls_A) + '\n')
f.write("Number of calls attempted from B: " + str(number_of_calls_B) + '\n')
f.write("Number of calls blocked: " + str(number_of_calls_blocked) + '\n')
f.write("Proportion of calls blocked: " + str(number_of_calls_blocked / index) + '\n')
f.write("Time average number of lines are busy: " + str(time_avg_number_of_lines_busy) + '\n')
f.write("Time average proportion of lines are busy: " + str(time_avg_proportion_of_lines_busy) + '\n\n')

f.write(str(lines))
f.close()
print(callData)
lines.plot.bar(y="efficiency", color='blue')
plt.show()
