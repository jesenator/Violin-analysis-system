import matplotlib.pyplot as plt
import csv
from scipy.signal import find_peaks
import numpy as np
import math
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
        position = p + q
        radius = radii[ord(position[0]) - ord('a')]
        angle = angles[int(position[1]) - 1]
        angle = (angle + 90) / 360 * 2 * math.pi
        x, y = getXY(radius, angle)
        xCoords.append(x)
        yCoords.append(y)
        # print(str(radius) + ", " + str(angle))
        # print(str(x) + ", " + str(y))
    return xCoords, yCoords


def openFile(file):
    print(file)
    tsv_file = open(file)
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    fields = next(read_tsv)
    data = list(read_tsv)
    tsv_file.close()
    return data


def getDataArrays(data):
    freqs, reals, complexs = [], [], []
    data = np.asarray(list(zip(*data)))

    for i in range(len(data[0])):
        freqs.append(float(data[0][i]))
        reals.append(float(data[1][i]))
        complexs.append(float(data[2][i]))

    complexs = np.asarray(complexs)
    reals = np.asarray(reals)
    return freqs, reals, complexs


def getPeaks(arr, threshold):
    peaks = find_peaks(arr, distance=3, prominence=.2, height=threshold)[0]
    return peaks


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


def writeTSV():
    print("writing to TSV")
    fields = ['tapNum', 'x', 'y']
    for i in range(len(modalFreqs)):
        fields.append("mode at %ihz" % modalFreqs[i])

    filename = "modalMagnitudes-test %i-pos=%i" % (testNum, positionNum)
    # for pos in positions:
    #     filename += str(pos) + "-"
    filename += ".tsv"

    # writing to tsv file
    with open(path.replace("csv\\", "") + filename, 'w') as tsvfile:
        tsvwriter = csv.writer(tsvfile, delimiter='\t')
        tsvwriter.writerow(fields)

        for i in range(positionNum):
            row = [i + 1, xCoords[i], yCoords[i]]
            for j in range(len(modalFreqs)):
                row.append(round(mags[i, j], 4))
            tsvwriter.writerow(row)
    print("done")


thresholds = [.1, 2.5]
testNum = 9
# change to path of csv folder
path = "C:\\Users\\jesse\\Desktop\\ObieAppFiles\\circular plate\\circular plate %s\\csv\\"
path = path % str(testNum).zfill(2)

positions = []
# positions = ["1c", "2c", "3c", "4c", "5c", "6c", "7c", "8c"]
# positionNum = len(positions)
positionNum = 24
for i in range(positionNum):
    positions.append(i+1)

# modalFreqs = np.array([39, 65, 91, 209, 212, 365, 372])  # first 10 from onscale
modalFreqs = np.array([154, 199, 343])

# xCoords, yCoords = getCoordinates(positions)
xCoords = [0, 0, 0, 26, 51, 77, 36, 73, 109, 26, 51, 77, 0, 0, 0, -26, -51, -77, -36, -73, -109, -26, -51, -77]
yCoords = [-36, -73, -109, -26, -51, -77, 0, 0, 0, 26, 51, 77, 36, 73, 109, 26, 51, 77, 0, 0, 0, -26, -51, -77]
mags = np.ndarray((positionNum + 1, len(modalFreqs)))

for tapNum in range(positionNum):
    filename = "circular plate %s H_%s_trf.tsv"
    filename = filename % (str(testNum).zfill(2), str(tapNum + 1).zfill(3))

    data = openFile(path + filename)
    freqs, reals, complexs = getDataArrays(data)

    for freqNum in range(len(modalFreqs)):
        freq = modalFreqs[freqNum]
        threshold = thresholds[0] if freq < 174 else thresholds[1]

        peaks = np.concatenate((getPeaks(complexs, threshold), getPeaks(-complexs, threshold)))

        # get closest peak to
        index = np.argmin(np.abs(np.array(peaks) - freq))
        adjustedFreq = peaks[index]
        if abs(adjustedFreq - freq) > 5:
            adjustedFreq = freq

        mags[tapNum][freqNum] = complexs[adjustedFreq]
    # plot()

writeTSV()
