#!/usr/bin/env python3
from mrjob.job import MRJob
import csv

class MRStatsGDPByDepartment(MRJob):

    def mapper(self, _, line):
        # Saltar encabezado
        if line.startswith("year"):
            return

        try:
            year, department, value, price_type = next(csv.reader([line]))
            value = float(value)
            key = (year, department)
            yield key, value
        except Exception:
            pass  # omitir líneas malformadas

    def reducer(self, key, values):
        values = list(values)
        total = sum(values)
        promedio = total / len(values)
        maximo = max(values)
        yield key, {
            "total": round(total, 2),
            "promedio por sector": round(promedio, 2),
        }

if __name__ == '__main__':
    MRStatsGDPByDepartment.run()
