import numpy as np
import sys
import pandas as pd

noOfCust = 100
rows, cols = (noOfCust, 12)
arr = [[0 for i in range(cols)] for j in range(rows)]
x = np.random.uniform(0, 5, noOfCust)
y = np.random.normal(loc=10, scale=5, size=noOfCust)

arr[0][0] = round(x[0], 1)
arr[0][1] = round(arr[0][0], 1)
arr[0][2] = float(0.0)
arr[0][3] = round(arr[0][1] + arr[0][2], 1)
if y[0] < 0:
    arr[0][4] = 0.0
else:
    arr[0][4] = round(y[0], 1)
arr[0][5] = round(arr[0][3] + arr[0][4], 1)
arr[0][6] = 0
arr[0][7] = round(arr[0][5] - arr[0][1], 1)

for i in range(1, noOfCust):
    arr[i][0] = round(x[i], 1)
    arr[i][1] = round(arr[i - 1][1] + arr[i][0], 1)
    arr[i][2] = round(arr[i - 1][5] - arr[i][1], 1)
    arr[i][3] = round(arr[i][1] + arr[i][2], 1)
    if y[i] < 0:
        arr[i][4] = 0.0
    else:
        arr[i][4] = round(y[i], 1)
    arr[i][5] = round(arr[i][3] + arr[i][4], 1)
    arr[i][7] = round(arr[i][5] - arr[i][1], 1)
    data = np.array(arr)
    sums = data.sum(axis=0)
    arr[i][8] = round(sums[2] / (i+1), 1)
    arr[i][9] = round(sums[7] / (i+1), 1)

for i in range(1, noOfCust):
    count = 0
    index = i + 1
    while index <= (noOfCust - 1) and arr[i][5] >= arr[index][1]:
        count = count + 1
        index = index + 1
    arr[i][6] = count
    data = np.array(arr)
    sums = data.sum(axis=0)
    arr[i][10] = round(sums[6] / i, 1)
    arr[i][11] = round((sums[6] + 1) / i, 1)

print("ICK AT\t\tWT\t\tTAS\t\tST\t\tDT\t\tQS\tTIS\t\tAWT\t\tATS\t\tAQL\t\tASL")
s = [[str(e) for e in row] for row in arr]
lens = [max(map(len, col)) for col in zip(*s)]
fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
table = [fmt.format(*row) for row in s]
print('\n'.join(table))