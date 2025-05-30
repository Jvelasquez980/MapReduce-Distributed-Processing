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
            key = (department, price_type)
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
            "promedio": round(promedio, 2),
            "maximo": round(maximo, 2),
            "conteo": len(values)
        }

if __name__ == '__main__':
    MRStatsGDPByDepartment.run()
