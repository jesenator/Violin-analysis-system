import time

from pyaxidraw import axidraw   # import module
import math
import time
# from utime import sleep_ms, ticks_ms, ticks_diff


def getXY(radius, angle):
    x = round(radius * -math.cos(angle))
    y = round(radius * -math.sin(angle))
    return x, y


def getCoordinates(angles, radii):
    xCoords = []
    yCoords = []
    for angle in angles:
        for radius in radii:
            angle = (angle + 90) / 360 * 2 * math.pi
            x, y = getXY(radius, angle)
            xCoords.append(x)
            yCoords.append(y)
            # print(str(radius) + ", " + str(angle))
            # print(str(x) + ", " + str(y))
            ad.moveto(x, y)
    return xCoords, yCoords


centerX = 150
centerY = 109
# centerY = 90
maxRadi = min(centerX, centerY)
angleNum = 8
radiusNum = 3
totalPostions = angleNum * radiusNum
print("total positions: " + str(totalPostions))
hits = 1
angles = []
radii = []
xCoords = []
yCoords = []

ad = axidraw.AxiDraw()          # Initialize class
ad.interactive()                # Enter interactive context
ad.connect()                    # Open serial port to AxiDraw

ad.options.units = 2
ad.options.speed_penup = 100
ad.options.pen_rate_raise = 100
ad.options.pen_rate_lower = 100
ad.update()                 # Process changes to options
ad.moveto(centerX, centerY)
print("center hammer on the plate")
time.sleep(2)

for i in range(angleNum):
    angle = 360 * i / angleNum + 90
    angle = angle / 360 * 2 * math.pi
    angles.append(angle)
for i in range(radiusNum):
    radii.append(round(maxRadi * (i+1) / radiusNum, 2))
print(angles)
print(radii)
# xCoords, yCoords = getCoordinates


def current_milli_time():
    return round(time.time() * 1000)


def getSeconds():
    seconds = round((current_milli_time() - start_ms) / 1000, 1)

    return seconds


start_ms = current_milli_time()
cycleLength = 3

for angle in angles:
    for radius in radii:
        # while (getSeconds() % cycleLength) != 0:
        #     time.sleep(.01)

        x, y = getXY(radius, angle)

        # print("polar: " + str(radius) + ", " + str(angle/math.pi) + "pi")
        # print("cartesian: " + str(x) + ", " + str(y))

        ad.moveto(x + centerX, y + centerY)
        xCoords.append(x)
        yCoords.append(y)

        for i in range(hits):

            ad.pendown()
            ad.penup()
            # while (getSeconds() % cycleLength) != 0:
            #     time.sleep(.01)
            # time.sleep(.2)

        # time.sleep(.5)

    # ad.moveto(centerX, centerY)
    # time.sleep(.5)x

ad.moveto(0, 0)
# paste coords lists to main program
print(xCoords)
print(yCoords)
ad.disconnect()                 # Close serial port to AxiDraw
