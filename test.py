from __future__ import division
import numpy as np


# Copy/paste stuff
count = 0
average = 0
side = 0
latest = 0

stepCount = 0

def onStepDetected(timestamp):
    global stepCount
    stepCount += 1

def detectSteps(timestamp, filteredValues):
    """
    Accelerometer-based step detection algorithm.

    In assignment A1, you will implement your step detection algorithm.
    This may be functionally equivalent to your Java step detection
    algorithm if you like. Remember to use the global keyword if you
    would like to access global variables such as counters or buffers.
    When a step has been detected, call the onStepDetected method, passing
    in the timestamp.
    """

    global count
    global average
    global side
    global latest

    combined = sum(map(lambda x: x * abs(x), filteredValues))
    if combined < 0:
        combined = -1 * (abs(combined) ** 0.5)
    else:
        combined = combined ** 0.5

    newSum = average * count
    count += 1
    average = ((newSum + combined) / count)

    if (combined != average) and side == 0:
        if combined > average:
            side = 1
        else:
            side = -1

    if (combined >= average) and side < 0:
        if ((timestamp - latest) < 750) and ((timestamp - latest) > 315):
            onStepDetected(timestamp)
        latest = timestamp
        side *= (-1)

    if (combined <= average) and side > 0:
        if ((timestamp - latest) < 750) and ((timestamp - latest) > 315):
            onStepDetected(timestamp)
        latest = timestamp
        side *= (-1)

    return

# Testing stuff
stepRate = 100
timeInMiliseconds = 50000
x = range(0, timeInMiliseconds)
noisless = map(lambda x: np.sin(((x * 10) / np.pi) * (1 / 1000) * (stepRate / 60)), x)

for i in range(0, timeInMiliseconds):
    detectSteps(x[i], [noisless[i]])

print('Noiseless: ', stepCount)

stepCount = 0

noise = 0.10
rands = [((noise * np.random.rand()) - (noise / 2)) for i in range(0, len(x))]

for i in range(0, timeInMiliseconds):
    detectSteps(x[i], [noisless[i]+ rands[i]])

print('Noise: ', stepCount)

print('Projected Step Count: ', (timeInMiliseconds / 1000) * (stepRate / 60))
import matplotlib.pyplot as plt

plt.plot(x, noisless)
plt.plot(x, [noisless[i] + rands[i] for i in range(0, len(x))])

plt.show()
