import numpy as np

count = 0
average = 0
side = 0
latest = 0

def onStepDetected(timestamp):
    print("Ping")

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


for i in range(0, 100000):
    detectSteps(i, [np.sin(i / 100)])
