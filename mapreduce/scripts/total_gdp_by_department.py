#!/usr/bin/env python3
from mrjob.job import MRJob
import csv
from collections import defaultdict

class MRStatsGDPByDepartment(MRJob):

    def mapper(self, _, line):
        if line.startswith("year"):
            return

        try:
            year, department, value, activity = next(csv.reader([line]))
            value = float(value)
            key = (year, department)
            yield key, (value, activity)
        except Exception:
            pass

    def reducer(self, key, values):
        total = 0
        count = 0
        max_value = float('-inf')
        max_activity = ""
        actividad_gdp = defaultdict(float)

        for value, activity in values:
            total += value
            count += 1
            actividad_gdp[activity] += value
            if value > max_value:
                max_value = value
                max_activity = activity

        promedio = total / count if count else 0

        yield key, {
            "PIB total": round(total, 2),
            "Promedio de PIB": round(promedio, 2),
            "Actividad con maximo PIB": {
                "actividad": max_activity,
                "valor": round(max_value, 2)
            },
            "Datos totales": count,
            "PIB de las actividades": {act: round(gdp, 2) for act, gdp in actividad_gdp.items()}
        }

if __name__ == '__main__':
    MRStatsGDPByDepartment.run()
