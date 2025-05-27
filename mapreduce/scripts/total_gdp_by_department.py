#!/usr/bin/env python3
from mrjob.job import MRJob
import csv
class MRTotalGDPByDepartment(MRJob):

    def mapper(self, _, line):
        # Skip the header
        if line.startswith("department"):
            return

        try:
            year, department, value = next(csv.reader([line]))
            value = float(value)
            yield department, value
        except:
            pass  # skip malformed lines

    def reducer(self, department, values):
        yield department, round(sum(values), 2)

if __name__ == '__main__':
    MRTotalGDPByDepartment.run()

