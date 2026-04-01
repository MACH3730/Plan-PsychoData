from flask import Flask, request, jsonify, render_template
import pandas as pd
import logic
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    # 1. Validación de entrada de archivo
    if 'file' not in request.files:
        return jsonify({'error': 'No se ha detectado el archivo en la petición'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se ha seleccionado ningún archivo'}), 400

    # 2. Captura de parámetros del frontend (Configuración del Panel Izquierdo)
    # método puede ser: 'spearman_brown', 'rulon' o 'guttman'
    metodo = request.form.get('metodo_mitades', 'spearman_brown')
    nulos = request.form.get('opcion_nulos', 'Sustituir por 0')
    
    try:
        # 3. Lectura del CSV
        # Usamos engine='python' para mayor compatibilidad con caracteres especiales
        df = pd.read_csv(file, engine='python')
        
        # 4. Procesamiento lógico (TCT con cuasivarianzas)
        resultado = logic.procesar_psicometria(df, metodo, nulos)
        
        # 5. Respuesta exitosa
        return jsonify(resultado)
        
    except Exception as e:
        # Enviamos el error específico para debuggear si el CSV es inválido
        return jsonify({'error': f"Error al procesar: {str(e)}"}), 500

if __name__ == '__main__':
    # Ejecución en modo debug para ver cambios en caliente
    app.run(debug=True)