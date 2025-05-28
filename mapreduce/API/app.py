from flask import Flask, jsonify
import csv

app = Flask(__name__)

@app.route("/api/resultados", methods=["GET"])
def obtener_resultados():
    resultados = []
    with open("resultados.csv", newline='', encoding='utf-8') as csvfile:
        lector = csv.reader(csvfile, delimiter='\t')
        for fila in lector:
            if len(fila) == 2:
                departamento, valor = fila
                resultados.append({
                    "departamento": departamento.strip(),
                    "valor": float(valor.strip())
                })
    return jsonify(resultados)

@app.route("/")
def index():
    return "API de resultados MapReduce funcionando correctamente 🚀"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
