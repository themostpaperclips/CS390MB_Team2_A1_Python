"""
Stuff for test
"""
from __future__ import division
import numpy as np

stepCount = 0

def onStepDetected(timestamp):
    global stepCount
    stepCount += 1

"""
Copy and paste from other file
"""

# How many data points
count = 0
# Average of all values, used to determine 0 crossing
average = 0
# The side of the average the last point was on
side = 0
# The time stamp of the most recent 0 crossing
latest = 0

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

    # Reference global variables
    global count
    global average
    global side
    global latest

    # Sum of squares of each direction, preserving negatives
    combined = sum(map(lambda x: x * abs(x), filteredValues))

    # Square root of combined, preserving negatives
    if combined < 0:
        combined = -1 * (abs(combined) ** 0.5)
    else:
        combined = combined ** 0.5

    # Multiply the average by the count to add this point to the average
    newSum = average * count
    # Increment the count
    count += 1
    # Calculate the new average
    average = ((newSum + combined) / count)

    # This initializes the side variable by putting it on one side at first
    if (combined != average) and side == 0:
        if combined > average:
            side = 1
        else:
            side = -1

    # If the current point is greater than the average and the last one was less
    if (combined >= average) and side < 0:
        # If the difference between this 0-crossing and the last one is in the step range
        if ((timestamp - latest) < 750) and ((timestamp - latest) > 315):
            onStepDetected(timestamp)
        # Update the latest 0-crossing and side
        latest = timestamp
        side *= (-1)

    # If the current point is less than the average and the last one was greater
    if (combined <= average) and side > 0:
        # If the difference between this 0-crossing and the last one is in the step range
        if ((timestamp - latest) < 750) and ((timestamp - latest) > 315):
            onStepDetected(timestamp)
        # Update the latest 0-crossing and side
        latest = timestamp
        side *= (-1)

    return

"""
Testing Stuff
"""
# Steps per minut (should be between 80-190)
stepRate = 100
# Time window to test
timeInMilliseconds = 50000
x = range(0, timeInMilliseconds)
noisless = map(lambda x: np.sin(((x * 10) / np.pi) * (1 / 1000) * (stepRate / 60)), x)

for i in range(0, timeInMilliseconds):
    detectSteps(x[i], [noisless[i]])

print('Noiseless: ', stepCount)

stepCount = 0

noise = 0.10
rands = [((noise * np.random.rand()) - (noise / 2)) for i in range(0, len(x))]

for i in range(0, timeInMilliseconds):
    detectSteps(x[i], [noisless[i]+ rands[i]])

print('Noise: ', stepCount)

if stepRate < 80 or stepRate > 190:
    print('Projected Step Count: ', 0)
else:
    print('Projected Step Count: ', (timeInMilliseconds / 1000) * (stepRate / 60))
import matplotlib.pyplot as plt

plt.plot(x, noisless)
plt.plot(x, [noisless[i] + rands[i] for i in range(0, len(x))])

plt.show()
