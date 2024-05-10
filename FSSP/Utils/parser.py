#!/usr/bin/env python

import numpy as np

def parse(path):
    file = open(path, 'r')

    firstLine = file.readline()
    firstLineValues = list(map(int, firstLine.split()[0:2]))

    jobsNb = firstLineValues[0]
    machinesNb = firstLineValues[1]

    jobs = [ [0]*machinesNb for i in range(jobsNb)]

    for i in range(machinesNb):
        currentLine = file.readline()
        # print(currentLine)
        currentLineValues = list(map(int, currentLine.split()))
        # print(currentLineValues)

        j = 0
        # print(len(currentLineValues))
        # print(machinesNb)
        while j < len(currentLineValues):
            procTime = currentLineValues[j]
            jobs[j][i] = procTime
            j = j+1

    file.close()

    print(jobs)

    return {'machinesNb': machinesNb, 'jobs': jobs}
