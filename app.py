import os
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. Configuration via les variables d'environnement
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'clientdb')
DB_USER = os.getenv('DB_USER', 'app_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'app_password')
DB_PORT = int(os.getenv('DB_PORT', 3306))

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

# 2. Initialisation de la table et insertion de données de test au démarrage
def init_db():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )
            """)
            # Insérer des données par défaut si la table est vide
            cursor.execute("SELECT COUNT(*) as count FROM clients")
            if cursor.fetchone()['count'] == 0:
                cursor.execute("INSERT INTO clients (name) VALUES ('Client Alpha'), ('Client Beta')")
                conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")

# Lancer l'initialisation au démarrage de l'app
init_db()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

# 3. Endpoint GET /clients : Récupère les données de MySQL
@app.route('/clients', methods=['GET'])
def get_clients():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
    conn.close()
    return jsonify(clients)

# 4. Endpoint POST /clients : Ajoute un client dans MySQL
@app.route('/clients', methods=['POST'])
def add_client():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "Le nom du client est requis"}), 400

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO clients (name) VALUES (%s)", (name,))
        conn.commit()
    conn.close()
    return jsonify({"message": "Client ajouté avec succès", "name": name}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8022, debug=True)