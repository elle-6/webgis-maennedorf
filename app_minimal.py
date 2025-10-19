"""
MINIMALES WEBGIS BACKEND
Dieses Script ist absichtlich einfach gehalten und enthält nur das Nötigste.
Es funktioniert OHNE komplexe Dependencies wie GeoAlchemy2.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
CORS(app)

# Datenbank-Hilfsfunktionen
def get_db():
    """Einfache SQLite-Verbindung"""
    conn = sqlite3.connect('simple_gis.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Erstellt einfache Tabellen"""
    conn = get_db()
    
    # Users Tabelle
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'viewer'
        )
    ''')
    
    # Features Tabelle (vereinfacht, ohne GeoAlchemy)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            feature_type TEXT,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            properties TEXT,
            created_by INTEGER,
            created_at TEXT
        )
    ''')
    
    # Prüfe ob Admin existiert
    user = conn.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if not user:
        conn.execute(
            'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
            ('admin', 'admin123', 'admin')
        )
        print("✓ Admin-Benutzer erstellt: admin / admin123")
    
    conn.commit()
    conn.close()

# Decorator für geschützte Routen
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token fehlt'}), 401
        
        try:
            token = token.replace('Bearer ', '')
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user_id']
        except:
            return jsonify({'message': 'Token ungültig'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# === ROUTES ===

@app.route('/')
def index():
    return jsonify({
        'message': 'WebGIS Backend läuft',
        'version': '1.0.0',
        'status': 'OK'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', 
        (username,)
    ).fetchone()
    conn.close()
    
    if not user or user['password'] != password:
        return jsonify({'message': 'Ungültige Anmeldedaten'}), 401
    
    # Erstelle Token
    token = jwt.encode({
        'user_id': user['id'],
        'username': user['username'],
        'role': user['role']
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'role': user['role']
        }
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username und Passwort erforderlich'}), 400
    
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
            (username, password, 'viewer')
        )
        conn.commit()
        return jsonify({'message': 'Registrierung erfolgreich'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username bereits vergeben'}), 409
    finally:
        conn.close()

@app.route('/api/features', methods=['GET'])
def get_features():
    conn = get_db()
    features = conn.execute('SELECT * FROM features').fetchall()
    conn.close()
    
    # Konvertiere zu GeoJSON
    geojson = {
        'type': 'FeatureCollection',
        'features': []
    }
    
    for f in features:
        geojson['features'].append({
            'type': 'Feature',
            'id': f['id'],
            'geometry': {
                'type': 'Point',
                'coordinates': [f['lon'], f['lat']]
            },
            'properties': {
                'name': f['name'],
                'description': f['description'],
                'feature_type': f['feature_type'],
                'properties': json.loads(f['properties']) if f['properties'] else {}
            }
        })
    
    return jsonify(geojson)

@app.route('/api/features', methods=['POST'])
@token_required
def create_feature(current_user):
    data = request.json
    
    name = data.get('name')
    lat = data['geometry']['coordinates'][1]
    lon = data['geometry']['coordinates'][0]
    
    conn = get_db()
    cursor = conn.execute(
        '''INSERT INTO features 
        (name, description, feature_type, lat, lon, properties, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            name,
            data.get('description', ''),
            data.get('feature_type', 'poi'),
            lat,
            lon,
            json.dumps(data.get('properties', {})),
            current_user,
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
    feature_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'message': 'Feature erstellt',
        'id': feature_id
    }), 201

@app.route('/api/features/<int:feature_id>', methods=['DELETE'])
@token_required
def delete_feature(current_user, feature_id):
    conn = get_db()
    conn.execute('DELETE FROM features WHERE id = ?', (feature_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Feature gelöscht'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🗺️  Minimales WebGIS Backend")
    print("="*60)
    init_db()
    print("✓ Datenbank initialisiert")
    print("\n👉 Backend läuft auf: http://localhost:5000")
    print("👉 Login: admin / admin123")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
