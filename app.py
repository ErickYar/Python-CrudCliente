import os  # <-- ¡ESTA LÍNEA FALTABA!
from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
from crud_clientes import ClienteDB

load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
db = ClienteDB(
    host=os.getenv("DB_HOST"),
    usuario=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    base_datos=os.getenv("DB_NAME")
)

@app.route('/')
def home():
    # Obtenemos los datos (lista de tuplas)
    clientes_raw = db.listar_clientes() 
    
    # Convertimos las tuplas a diccionarios para que el HTML los entienda
    columnas = ['id', 'nombre', 'correo', 'telefono']
    clientes = [dict(zip(columnas, fila)) for fila in clientes_raw]
    
    return render_template('index.html', clientes=clientes)

@app.route('/clientes/web', methods=['POST'])
def crear_cliente_web():
    nombre = request.form['nombre']
    correo = request.form['correo']
    telefono = request.form['telefono']
    db.crear_cliente(nombre, correo, telefono)
    return redirect(url_for('home'))

@app.route('/clientes', methods=['GET'])
def listar_clientes_api():
    clientes = db.listar_clientes()
    return jsonify(clientes)

@app.route('/clientes', methods=['POST'])
def crear_cliente_api():
    data = request.get_json()
    db.crear_cliente(data['nombre'], data['correo'], data['telefono'])
    return jsonify({"mensaje": "Cliente creado"}), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)