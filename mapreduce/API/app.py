from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)
S3_URL = "https://proyectotelematica.s3.us-east-1.amazonaws.com/output/resultados.csv"

@app.route("/api/resultados", methods=["GET"])
def obtener_resultados():
    try:
        response = requests.get(S3_URL)
        response.raise_for_status()
        contenido = response.content.decode('utf-8')

        resultados = []
        for linea in contenido.strip().split("\n"):
            try:
                clave, valor_json = linea.strip().split("\t")
                year, departamento = eval(clave)  # clave es una tupla en string
                departamento = departamento.replace('"', '').strip().encode("utf-8").decode("unicode_escape")
                datos = json.loads(valor_json)
                resultados.append({
                    "año": year,
                    "departamento": departamento,
                    "pib_total": datos.get("PIB total"),
                    "promedio_actividad": datos.get("Promedio de PIB"),
                    "maximo_actividad": datos.get("Actividad con maximo PIB"),
                    "total_actividades": datos.get("Datos totales"),
                    "actividades": datos.get("PIB de las actividades", [])
                })
            except Exception as e:
                print(f"⚠️ Error en línea: {linea} → {e}")

        # Filtro por departamento (opcional)
        filtro = request.args.get("departamento")
        if filtro:
            resultados = [r for r in resultados if r["departamento"].lower() == filtro.lower()]

        return jsonify(resultados)

    except requests.RequestException as e:
        return jsonify({"error": "No se pudo acceder al archivo S3", "detalles": str(e)}), 500

@app.route("/")
def index():
    return "✅ API funcionando con filtro por departamento y resultados extendidos"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
