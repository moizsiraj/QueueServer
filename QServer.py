import numpy as np
import matplotlib.pyplot as plt

noOfCust = 100
interArrivalMax = 10
servingMean = 5
servingSd = 1.5
rows, cols = (noOfCust, 13)
arr = [[0 for i in range(cols)] for j in range(rows)]
# x = np.random.uniform(0, interArrivalMax, noOfCust)
# y = np.random.normal(loc=servingMean, scale=servingSd, size=noOfCust)

# case 1
x = np.random.uniform(4, 6, noOfCust)
y = np.random.uniform(0.05, 0.15, noOfCust)
#
# # case 2 and 3
# x = np.random.uniform(4, 6, noOfCust)
# y = np.random.normal(loc=servingMean, scale=servingSd, size=noOfCust)

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
arr[0][12] = round(arr[0][4] / (arr[0][5]), 3)

for i in range(1, noOfCust):
    arr[i][0] = round(x[i], 1)
    arr[i][1] = round(arr[i - 1][1] + arr[i][0], 1)
    arr[i][2] = round(arr[i - 1][5] - arr[i][1], 1)

    if arr[i][2] < 0:
        arr[i][2] = 0

    arr[i][3] = round(arr[i][1] + arr[i][2], 1)
    if y[i] < 0:
        arr[i][4] = 0.0
    else:
        arr[i][4] = round(y[i], 1)
    arr[i][5] = round(arr[i][3] + arr[i][4], 1)
    arr[i][7] = round(arr[i][5] - arr[i][1], 1)
    data = np.array(arr)
    sums = data.sum(axis=0)
    arr[i][8] = round(sums[2] / (i + 1), 1)
    arr[i][9] = round(sums[7] / (i + 1), 1)
    arr[i][12] = round(sums[4] / arr[i][5], 4)

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

data = np.array(arr)
#
# f = open("output.txt", "a")
#
# f.write("\n\n")
# f.write("Number of Customers: " + str(noOfCust) + "\n")
# f.write("Max Inter-Arrival Time: " + str(interArrivalMax) + "\n")
# f.write("Serving Time Mean: " + str(servingMean) + "\n")
# f.write("Serving Time Standard Deviation: " + str(servingSd) + "\n\n")
#
# f.write("IAT: Inter Arrival Time\n"
#         "AT: Arrival Time\n"
#         "WT: Waiting Time\n"
#         "TAS: Time At Service\n"
#         "ST: Service Time\n"
#         "DT: Departure Time\n"
#         "QL: Queue Length\n"
#         "TIS: Time In System\n"
#         "AWT: Average Waiting Time\n"
#         "ATS: Average Time In System\n"
#         "AQL: Average Queue Length\n"
#         "AUS: Average Users in System\n"
#         "UTF: Utilisation Factor\n")

print("IAT AT\t\tWT\t\tTAS\t\tST\t\tDT\t\tQL\tTIS\t\tAWT\t\tATS\t\tAQL\t\tAUS\t\tUTF\n")
s = [[str(e) for e in row] for row in arr]
lens = [max(map(len, col)) for col in zip(*s)]
fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
table = [fmt.format(*row) for row in s]
print('\n'.join(table))

# Note that even in the OO-style, we use `.pyplot.figure` to create the figure.
fig, ax = plt.subplots()  # Create a figure and an axes.
x = data[:, 8]
y = data[:, 10]
# ax.plot(x)
ax.plot(y)
#
plt.show()
# f.close()

