from flask import Flask, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Configuration de la base de données
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'realtime_data'),
    'user': os.getenv('POSTGRES_USER', 'admin'),
    'password': os.getenv('POSTGRES_PASSWORD', 'admin123'),
    'host': os.getenv('POSTGRES_HOST', 'postgres'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

def get_db_connection():
    """Établit une connexion à la base de données PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)

@app.route('/health')
def health_check():
    """Point de terminaison pour vérifier l'état de l'API"""
    return jsonify({'status': 'healthy'})

@app.route('/data')
def get_data():
    """Récupère les dernières données traitées"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM processed_data 
                    ORDER BY timestamp DESC 
                    LIMIT 100
                """)
                data = cur.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def get_stats():
    """Récupère des statistiques agrégées"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        type,
                        AVG(value) as average_value,
                        COUNT(*) as count
                    FROM processed_data 
                    GROUP BY type
                """)
                stats = cur.fetchall()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)