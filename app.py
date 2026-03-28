from flask import Flask, request, jsonify, render_template
import pandas as pd
import logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    if 'file' not in request.files:
        return jsonify({'error': 'No hay archivo'}), 400
    
    file = request.files['file']
    metodo = request.form.get('metodo_mitades', 'spearman_brown')
    nulos = request.form.get('opcion_nulos', 'Sustituir por 0')
    
    try:
        df = pd.read_csv(file)
        resultado = logic.procesar_psicometria(df, metodo, nulos)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)