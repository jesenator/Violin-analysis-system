import matplotlib.pyplot as plt
import csv
from scipy.signal import find_peaks, savgol_filter
import numpy as np
import math
import random
import re


def getXY(radius, angle):
    x = round(radius * -math.cos(angle))
    y = round(radius * math.sin(angle))
    return x, y


def getCoordinates(string):
    radii = [35, 72.5, 114]
    angles = []
    xCoords = []
    yCoords = []
    for i in range(8):
        angles.append(i * 45)
    for position in positions:
        p = re.search("[a-c]", position).group(0)
        q = re.search("[1-8]", position).group(0)
        position = p+q
        radius = radii[ord(position[0]) - ord('a')]
        angle = angles[int(position[1]) - 1]
        angle = (angle + 90) / 360 * 2 * math.pi
        x, y = getXY(radius, angle)
        xCoords.append(x)
        yCoords.append(y)
        # print(str(radius) + ", " + str(angle))
        # print(str(x) + ", " + str(y))
    return xCoords, yCoords


def plot():
    # print(peaks)
    fig = plt.figure()
    ax = plt.subplot()
    # ax.set_xlim([30, len(complexs)])
    ax.set_xlim([30, 450])
    ax.set_ylim([-5, 5])
    ax.set_xscale('log')
    ax.plot(complexs)
    plt.plot(reals, ":")

    plt.plot(peaks, complexs[peaks], "x")
    # plt.plot(np.full(len(complexs), threshold), "--", color="gray")
    # plt.plot(np.full(len(complexs), -threshold), "--", color="gray")

    for frequency in modalFreqs:
        plt.vlines(frequency, complexs[frequency] - .1, complexs[frequency] + .1, color="green", linestyles=":")
    plt.plot(modalFreqs, complexs[modalFreqs], "k.")
    plt.title("position: %s, freq: %i" % (positions[tapNum], freq))
    plt.show()


threshold = 1
testNum = 8
path = "C:\\Users\\jesse\\Desktop\\ObieAppFiles\\circular plate\\circular plate %s\\csv\\"
path = path % str(testNum).zfill(2)
# positions = ["a1", "b4", "a5", "c2", "b8"]
positions = ["1c", "2c", "3c", "4c", "5c", "6c", "7c", "8c"]
# positions = ["b1", "b5"]

# modalFreqs = np.array([39, 65, 91, 209, 212, 365, 372])
# modalFreqs = np.array([65])
# modalFreqs = np.array([91, 209])
modalFreqs = np.array([154, 199, 343])
xCoords, yCoords = getCoordinates(positions)
mags = np.ndarray((len(positions)+1, len(modalFreqs)))

offsetFactor = 0
modalFreqs = modalFreqs - offsetFactor

for tapNum in range(len(positions)):
    filename = "circular plate %s H_%s_trf.tsv"
    filename = filename % (str(testNum).zfill(2), str(tapNum + 1).zfill(3))

    print(path + filename)
    tsv_file = open(path + filename)
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    fields = next(read_tsv)

    data = list(read_tsv)
    tsv_file.close()

    freqs, reals, complexs = [], [], []
    data = np.asarray(list(zip(*data)))

    for i in range(len(data[0])):
        freqs.append(float(data[0][i]))
        reals.append(float(data[1][i]))
        complexs.append(float(data[2][i]))

    complexs = np.asarray(complexs)
    reals = np.asarray(reals)


    # filtered = savgol_filter(complexs, 31, 1)
    def getPeaks(arr, threshold):
        # peaks = find_peaks(arr, height=threshold, distance=200)[0]
        peaks = find_peaks(arr, distance=3, prominence=.2, height=threshold)[0]
        return peaks


    for freqNum in range(len(modalFreqs)):
        freq = modalFreqs[freqNum]

        if freq < 174:
            threshold = .1
        else:
            threshold = 2.5
        peaksPos = getPeaks(complexs, threshold)
        peaksNeg = getPeaks(-complexs, threshold)
        peaks = np.concatenate((peaksPos, peaksNeg))

        index = np.argmin(np.abs(np.array(peaks) - freq))
        adjustedFreq = peaks[index]
        if abs(adjustedFreq - freq) > 5:
            adjustedFreq = freq

        mags[tapNum][freqNum] = complexs[adjustedFreq]
    # plot()

########## creating tsv
fields = ['tapNum', 'x', 'y']
for i in range(len(modalFreqs)):
    fields.append("mode at %ihz" % modalFreqs[i])
    mags[len(positions)][i] = 0

filename = "modalMagnitudes-"
for pos in positions:
    filename += pos + "-"
filename += ".tsv"
# writing to tsv file
additionalZeros = 0
with open(path.replace("csv\\", "") + filename, 'w') as tsvfile:
    tsvwriter = csv.writer(tsvfile, delimiter='\t')
    tsvwriter.writerow(fields)

    for i in range(len(positions)):
        row = [i+1, xCoords[i], yCoords[i]]
        for j in range(len(modalFreqs)):
            row.append(round(mags[i, j], 4))
        tsvwriter.writerow(row)

    row = [0, 0, 0]
    for j in range(len(modalFreqs)):
        row.append(round(mags[len(positions), j], 4))
    for i in range(len(positions)+1, len(positions)+1 + additionalZeros):
        row[0] = i
        row[1] = random.random() * 10
        row[2] = random.random() * 10
        tsvwriter.writerow(row)

# plt.show()
