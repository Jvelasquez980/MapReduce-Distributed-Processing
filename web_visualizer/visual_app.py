from flask import Flask, render_template_string, send_file
import requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
from fpdf import FPDF
import base64
import numpy as np
from scipy import stats
import warnings
import tempfile
import os
warnings.filterwarnings('ignore')

app = Flask(__name__)
DATA_URL = "http://174.129.242.86:5000/api/resultados"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis Económico Colombia</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #2d3748;
            line-height: 1.6;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 2rem 0;
            margin-bottom: 3rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            text-align: center;
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            text-align: center;
            font-size: 1.2rem;
            color: #64748b;
            font-weight: 300;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        .indicators {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 2.5rem;
            border-radius: 24px;
            margin-bottom: 3rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .indicators h2 {
            font-size: 2rem;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .indicators h2::before {
            content: "📊";
            font-size: 1.5rem;
        }
        
        .indicators ul {
            list-style: none;
            display: grid;
            gap: 1rem;
        }
        
        .indicators li {
            background: linear-gradient(135deg, #f8fafc, #e2e8f0);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .indicators li:hover {
            transform: translateX(8px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        }
        
        .section-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            margin: 3rem 0 2rem 0;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        
        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .chart-box {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        
        .chart-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .chart-box:hover {
            transform: translateY(-8px);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
        }
        
        .chart-box h3 {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 1.5rem;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
        
        .chart-box h3::before {
            content: "📈";
            font-size: 1.2rem;
        }
        
        .chart-box img {
            width: 100%;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            margin: 3rem auto;
            padding: 1rem 2.5rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1rem;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.5);
        }
        
        .btn-container {
            text-align: center;
            margin: 3rem 0;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 0 1rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .chart-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .chart-box {
                padding: 1.5rem;
            }
            
            .section-title {
                font-size: 2rem;
            }
        }
        
        .fade-in {
            animation: fadeIn 0.8s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <div class="header fade-in">
        <div class="container">
            <h1>Análisis Económico de Colombia</h1>
            <p>Dashboard avanzado de análisis econométrico por departamento</p>
        </div>
    </div>

    <div class="container">
        <div class="indicators fade-in">
            <h2>Análisis Econométrico Avanzado</h2>
            <ul>
                {% for item in indicadores %}
                <li>{{ item }}</li>
                {% endfor %}
            </ul>
        </div>

        <h2 class="section-title">📈 Análisis de Crecimiento y Tendencias del PIB</h2>
        <div class="chart-grid fade-in">
            {% for dept, chart in growth_charts.items() %}
            <div class="chart-box">
                <h3>{{ dept }}</h3>
                <img src="data:image/png;base64,{{ chart }}" alt="Gráfico PIB {{ dept }}">
            </div>
            {% endfor %}
        </div>

        <div class="btn-container fade-in">
            <a href="/descargar_pdf" class="btn">
                <i class="fas fa-download"></i>
                Descargar Informe Econométrico PDF
            </a>
        </div>
    </div>
</body>
</html>
"""

def fetch_data():
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def process_data(data):
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    df["año"] = df["año"].astype(int)
    return df

def generate_growth_charts(df):
    charts = {}
    if df.empty:
        return charts
        
    plt.style.use('default')
    
    for dept in df["departamento"].unique():
        subset = df[df["departamento"] == dept].sort_values("año")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        fig.patch.set_facecolor('white')
        
        # Gráfico 1: PIB y tendencia
        ax1.plot(subset["año"], subset["pib_total"], 
                marker='o', linestyle='-', linewidth=3, 
                markersize=8, color='#667eea', markerfacecolor='#764ba2',
                markeredgecolor='white', markeredgewidth=2, label='PIB Real')
        
        # Agregar línea de tendencia
        if len(subset) > 2:
            z = np.polyfit(subset["año"], subset["pib_total"], 1)
            p = np.poly1d(z)
            ax1.plot(subset["año"], p(subset["año"]), "--", 
                    color='#f093fb', linewidth=2, label='Tendencia Linear')
        
        ax1.fill_between(subset["año"], subset["pib_total"], alpha=0.3, 
                       color='#667eea')
        
        ax1.set_title(f"PIB Total y Tendencia - {dept}", fontsize=14, fontweight='bold', 
                    color='#2d3748', pad=15)
        ax1.set_ylabel("PIB Total (Miles de Millones)", fontsize=10, color='#4a5568')
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.legend()
        
        # Gráfico 2: Tasa de crecimiento anual
        if len(subset) > 1:
            growth_rates = subset["pib_total"].pct_change() * 100
            ax2.bar(subset["año"][1:], growth_rates[1:], 
                   color=['#10b981' if x > 0 else '#ef4444' for x in growth_rates[1:]], 
                   alpha=0.8, width=0.6)
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax2.set_title(f"Tasa de Crecimiento Anual - {dept}", fontsize=14, fontweight='bold', 
                        color='#2d3748', pad=15)
            ax2.set_xlabel("Año", fontsize=10, color='#4a5568')
            ax2.set_ylabel("Crecimiento (%)", fontsize=10, color='#4a5568')
            ax2.grid(True, alpha=0.3, linestyle='--')
        
        # Estilo general
        for ax in [ax1, ax2]:
            ax.set_facecolor('#f8fafc')
            for spine in ax.spines.values():
                spine.set_color('#e2e8f0')
                spine.set_linewidth(1)
            ax.tick_params(colors='#4a5568', labelsize=9)
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        buf.seek(0)
        charts[dept] = base64.b64encode(buf.read()).decode("utf-8")
    
    return charts

def calcular_indicadores_avanzados(df):
    indicadores = []
    
    if df.empty:
        indicadores.append("No hay datos disponibles para el análisis")
        return indicadores

    try:
        # 1. Análisis de volatilidad económica (Coeficiente de Variación)
        volatilidad = []
        for dept in df["departamento"].unique():
            subset = df[df["departamento"] == dept].sort_values("año")
            if len(subset) > 2:
                cv = (subset["pib_total"].std() / subset["pib_total"].mean()) * 100
                volatilidad.append((dept, cv))
        
        if volatilidad:
            volatilidad_sorted = sorted(volatilidad, key=lambda x: x[1])
            indicadores.append("ANALISIS DE VOLATILIDAD ECONOMICA (Coeficiente de Variacion):")
            indicadores.append(f"   Mas estable: {volatilidad_sorted[0][0]} ({volatilidad_sorted[0][1]:.2f}%)")
            indicadores.append(f"   Mas volatil: {volatilidad_sorted[-1][0]} ({volatilidad_sorted[-1][1]:.2f}%)")

        # 2. Tasa de Crecimiento Anual Compuesta (CAGR)
        cagr_data = []
        for dept in df["departamento"].unique():
            subset = df[df["departamento"] == dept].sort_values("año")
            if len(subset) > 1:
                años = subset["año"].max() - subset["año"].min()
                if años > 0:
                    valor_inicial = subset["pib_total"].iloc[0]
                    valor_final = subset["pib_total"].iloc[-1]
                    cagr = ((valor_final / valor_inicial) ** (1/años) - 1) * 100
                    cagr_data.append((dept, cagr))
        
        if cagr_data:
            cagr_sorted = sorted(cagr_data, key=lambda x: x[1], reverse=True)
            indicadores.append("TASA DE CRECIMIENTO ANUAL COMPUESTA (CAGR):")
            for i, (dept, cagr) in enumerate(cagr_sorted[:3]):
                indicadores.append(f"   {i+1}. {dept}: {cagr:.2f}% anual")

        # 3. Análisis de correlación con tendencia temporal
        correlaciones = []
        for dept in df["departamento"].unique():
            subset = df[df["departamento"] == dept].sort_values("año")
            if len(subset) > 3:
                correlation, p_value = stats.pearsonr(subset["año"], subset["pib_total"])
                correlaciones.append((dept, correlation, p_value))
        
        if correlaciones:
            indicadores.append("ANALISIS DE TENDENCIA TEMPORAL (Correlacion con el tiempo):")
            correlaciones_sorted = sorted(correlaciones, key=lambda x: abs(x[1]), reverse=True)
            for dept, corr, p_val in correlaciones_sorted[:3]:
                tendencia = "creciente" if corr > 0 else "decreciente"
                significancia = "significativa" if p_val < 0.05 else "no significativa"
                indicadores.append(f"   {dept}: Tendencia {tendencia} (r={corr:.3f}, {significancia})")

        # 4. Índice de Desarrollo Económico Relativo
        if len(df["departamento"].unique()) > 1:
            pib_promedio_nacional = df.groupby("año")["pib_total"].mean()
            indices_desarrollo = []
            
            for dept in df["departamento"].unique():
                subset = df[df["departamento"] == dept].sort_values("año")
                indices_dept = []
                for _, row in subset.iterrows():
                    if row["año"] in pib_promedio_nacional.index:
                        indice = (row["pib_total"] / pib_promedio_nacional[row["año"]]) * 100
                        indices_dept.append(indice)
                
                if indices_dept:
                    indice_promedio = np.mean(indices_dept)
                    indices_desarrollo.append((dept, indice_promedio))
            
            if indices_desarrollo:
                indices_sorted = sorted(indices_desarrollo, key=lambda x: x[1], reverse=True)
                indicadores.append("INDICE DE DESARROLLO ECONOMICO RELATIVO (Base Nacional = 100):")
                for dept, indice in indices_sorted[:5]:
                    nivel = "Superior" if indice > 100 else "Inferior"
                    indicadores.append(f"   {dept}: {indice:.1f} ({nivel} al promedio nacional)")

    except Exception as e:
        print(f"Error calculating advanced indicators: {e}")
        indicadores.append("Error en el calculo de algunos indicadores avanzados")

    return indicadores

def clean_text(text):
    """Limpia el texto para evitar problemas de codificación en PDF"""
    # Reemplazar caracteres problemáticos
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', '°': 'o', '€': 'EUR', '£': 'GBP',
        '"': '"', '"': '"', ''': "'", ''': "'", '–': '-', '—': '-',
        '🎯': '', '📍': '', '📈': '', '🥇': '', '📊': '', '🛡️': '', '🎖️': ''
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Mantener solo caracteres ASCII seguros
    return ''.join(char for char in text if ord(char) < 128)

def generate_pdf(df):
    """Genera PDF usando archivo temporal para evitar problemas de codificación"""
    try:
        # Crear archivo temporal
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_filename = temp_file.name
        temp_file.close()
        
        # Crear PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, clean_text('Informe Econométrico Avanzado - Colombia'), 0, 1, 'C')
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 5, clean_text('Análisis por Departamento'), 0, 1, 'C')
        pdf.ln(10)
        
        # Resumen ejecutivo
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'RESUMEN EJECUTIVO', 0, 1, 'L')
        pdf.ln(5)
        
        if not df.empty:
            total_depts = len(df["departamento"].unique())
            años_analisis = f"{df['año'].min()} - {df['año'].max()}"
            pib_total_ultimo = df[df['año'] == df['año'].max()]['pib_total'].sum()
            
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, clean_text(f"Este informe analiza {total_depts} departamentos de Colombia durante el periodo {años_analisis}."), 0, 1)
            pdf.cell(0, 6, clean_text(f"PIB total agregado en {df['año'].max()}: ${pib_total_ultimo:,.2f} miles de millones."), 0, 1)
            pdf.ln(10)
        
        # Análisis por departamento
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'ANALISIS DETALLADO POR DEPARTAMENTO', 0, 1, 'L')
        pdf.ln(5)
        
        for dept in df["departamento"].unique():
            subset = df[df["departamento"] == dept].sort_values("año")
            
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, clean_text(f"Departamento: {dept}"), 0, 1)
            
            # Estadísticas básicas
            pib_inicial = subset["pib_total"].iloc[0]
            pib_final = subset["pib_total"].iloc[-1]
            crecimiento_total = ((pib_final / pib_inicial) - 1) * 100
            
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 6, clean_text(f"Periodo de analisis: {subset['año'].min()} - {subset['año'].max()}"), 0, 1)
            pdf.cell(0, 6, clean_text(f"PIB inicial: ${pib_inicial:,.2f} miles de millones"), 0, 1)
            pdf.cell(0, 6, clean_text(f"PIB final: ${pib_final:,.2f} miles de millones"), 0, 1)
            pdf.cell(0, 6, clean_text(f"Crecimiento total: {crecimiento_total:.2f}%"), 0, 1)
            pdf.ln(5)
            
            # Verificar si necesitamos nueva página
            if pdf.get_y() > 250:
                pdf.add_page()
        
        # Indicadores avanzados
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'INDICADORES ECONOMETRICOS AVANZADOS', 0, 1, 'L')
        pdf.ln(5)
        
        indicadores = calcular_indicadores_avanzados(df)
        pdf.set_font('Arial', '', 10)
        for indicador in indicadores:
            clean_indicador = clean_text(indicador)
            # Dividir líneas largas
            if len(clean_indicador) > 80:
                words = clean_indicador.split(' ')
                line = ''
                for word in words:
                    if len(line + word + ' ') < 80:
                        line += word + ' '
                    else:
                        if line.strip():
                            pdf.cell(0, 6, line.strip(), 0, 1)
                        line = word + ' '
                if line.strip():
                    pdf.cell(0, 6, line.strip(), 0, 1)
            else:
                pdf.cell(0, 6, clean_indicador, 0, 1)
            pdf.ln(2)
        
        # Guardar PDF en archivo temporal
        pdf.output(temp_filename)
        
        # Leer el archivo y crear BytesIO
        with open(temp_filename, 'rb') as f:
            pdf_data = f.read()
        
        # Limpiar archivo temporal
        os.unlink(temp_filename)
        
        # Crear BytesIO con los datos del PDF
        output = io.BytesIO(pdf_data)
        output.seek(0)
        return output
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        # Crear un PDF mínimo en caso de error
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_filename = temp_file.name
            temp_file.close()
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Error en la generacion del informe', 0, 1, 'C')
            pdf.output(temp_filename)
            
            with open(temp_filename, 'rb') as f:
                pdf_data = f.read()
            
            os.unlink(temp_filename)
            
            output = io.BytesIO(pdf_data)
            output.seek(0)
            return output
        except:
            return io.BytesIO()

@app.route("/")
def index():
    try:
        data = fetch_data()
        df = process_data(data)
        growth_charts = generate_growth_charts(df)
        indicadores = calcular_indicadores_avanzados(df)
        return render_template_string(HTML_TEMPLATE,
                                      growth_charts=growth_charts,
                                      indicadores=indicadores)
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"Error: {str(e)}", 500

@app.route("/descargar_pdf")
def descargar_pdf():
    try:
        data = fetch_data()
        df = process_data(data)
        pdf = generate_pdf(df)
        return send_file(pdf, as_attachment=True,
                         download_name="informe_econometrico_colombia.pdf",
                         mimetype='application/pdf')
    except Exception as e:
        print(f"Error in PDF download: {e}")
        return f"Error generating PDF: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")