#!/usr/bin/env python

# This module parses .fjs files as found in the "Monaldo" FJSP dataset.
# More explanations on this file format can be found in the dataset.


def parse(path):
    file = open(path, 'r')

    firstLine = file.readline()
    firstLineValues = list(map(int, firstLine.split()[0:2]))

    jobsNb = firstLineValues[0]
    machinesNb = firstLineValues[1]

    jobs = []

    for i in range(jobsNb):
        currentLine = file.readline()
        # print(currentLine)
        currentLineValues = list(map(int, currentLine.split()))
        # print(currentLineValues)

        operations = []

        j = 1
        # print(currentLineValues[j])
        while j < len(currentLineValues):
            k = currentLineValues[j]
            j = j+1

            operation = []

            # print(k)

            for ik in range(k):
                machine = currentLineValues[j]
                j = j+1
                processingTime = currentLineValues[j]
                j = j+1

                operation.append({'machine': machine, 'processingTime': processingTime})
            #print(operation)
            operations.append(operation)

        jobs.append(operations)

    file.close()

    return {'machinesNb': machinesNb, 'jobs': jobs}
