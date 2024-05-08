#!/usr/bin/env python

import numpy as np

def parse(path):
    file = open(path, 'r')

    firstLine = file.readline()
    firstLineValues = list(map(int, firstLine.split()[0:2]))

    jobsNb = firstLineValues[0]
    machinesNb = firstLineValues[1]

    jobs = []

    for i in range(machinesNb):
        currentLine = file.readline()
        # print(currentLine)
        currentLineValues = list(map(int, currentLine.split()))
        # print(currentLineValues)

        j = 0
        # print(currentLineValues[j])
        while j < len(currentLineValues):
            k = 0
            operation = [0] * machinesNb
            while k < machinesNb:
                procTime = currentLineValues[j]
                j = j+1

                # print(procTime)

                operation[k] = procTime
                # print(operation)
                k = k+1
            #print(operation)
            jobs.append(operation)
            # print(jobs)

    file.close()

    # print(jobs)

    return {'machinesNb': machinesNb, 'jobs': jobs}
