from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from crud_clientes import ClienteDB  # Asegúrate de que tu clase se llame así

load_dotenv()


app = Flask(__name__)

# Configuración de la base de datos usando las variables de entorno que definiremos en Railway
db = ClienteDB(
    host=os.getenv("DB_HOST"),
    usuario=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    base_datos=os.getenv("DB_NAME")
)

@app.route('/')
def home():
    return "API de Clientes funcionando. Ve a /clientes para ver la lista."

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = db.listar_clientes() # Tu método ya devuelve una lista
    return jsonify(clientes)

@app.route('/clientes', methods=['POST'])
def crear_cliente():
    data = request.get_json()
    db.crear_cliente(data['nombre'], data['correo'], data['telefono'])
    return jsonify({"mensaje": "Cliente creado"}), 201

# ... puedes añadir rutas similares para actualizar y eliminar

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)