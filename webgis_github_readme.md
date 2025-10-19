# 🗺️ WebGIS Männedorf

Ein einfaches, aber leistungsstarkes WebGIS (Geographisches Informationssystem) für die Verwaltung und Visualisierung von geografischen Daten.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-green.svg)

## ✨ Features

- 🗺️ **Interaktive Karte** mit OpenStreetMap
- 👤 **Benutzer-Authentifizierung** (Login/Register)
- 📍 **Features erstellen** - Punkte auf der Karte setzen
- 💾 **Persistente Speicherung** in SQLite-Datenbank
- 🔒 **JWT-Token-basierte API** für sichere Kommunikation
- 🎨 **Modernes, responsives Design**
- 🚀 **Einfache Installation** - keine komplexen Dependencies

## 📸 Screenshots

![WebGIS Login](https://via.placeholder.com/800x400?text=Screenshot+hier+einfügen)

## 🚀 Quick Start

### Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)
- Webbrowser (Chrome, Firefox, Edge)

### Installation

1. **Repository klonen**
```bash
git clone https://github.com/IHR-USERNAME/webgis-maennedorf.git
cd webgis-maennedorf
```

2. **Backend einrichten**
```bash
cd backend
pip install flask flask-cors pyjwt
```

3. **Backend starten**
```bash
python app_minimal.py
```

Das Backend läuft nun auf `http://localhost:5000`

4. **Frontend starten** (neues Terminal-Fenster)
```bash
cd frontend
python -m http.server 8080
```

Das Frontend ist nun unter `http://localhost:8080/test.html` erreichbar

### 🎯 Standard-Login

- **Username:** `admin`
- **Passwort:** `admin123`

⚠️ **WICHTIG:** Ändern Sie das Passwort sofort nach dem ersten Login!

## 📖 Verwendung

### Features erstellen

1. Melden Sie sich an
2. Klicken Sie auf "📍 Punkt hinzufügen"
3. Klicken Sie auf die Karte
4. Geben Sie Name und Beschreibung ein
5. Fertig! Der Punkt wird gespeichert

### Features anzeigen

- Klicken Sie auf "🔄 Features laden" um alle gespeicherten Punkte anzuzeigen
- Klicken Sie auf einen Marker um Details zu sehen

## 🏗️ Architektur

```
webgis-maennedorf/
├── backend/
│   ├── app_minimal.py      # Flask Backend-Server
│   └── simple_gis.db       # SQLite Datenbank (wird automatisch erstellt)
├── frontend/
│   └── test.html           # Single-Page-Application
├── README.md
├── LICENSE
└── .gitignore
```

### Technologie-Stack

**Backend:**
- Flask 3.0 - Web Framework
- Flask-CORS - Cross-Origin Resource Sharing
- PyJWT - JSON Web Token Authentifizierung
- SQLite3 - Leichtgewichtige Datenbank

**Frontend:**
- Vanilla JavaScript - Keine Frameworks!
- Leaflet.js - Interaktive Karten
- OpenStreetMap - Kartenmaterial

## 🔌 API-Endpunkte

### Authentifizierung

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

### Features

```http
GET /api/features
```

```http
POST /api/features
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Rathaus",
  "description": "Gemeindeverwaltung",
  "feature_type": "poi",
  "geometry": {
    "type": "Point",
    "coordinates": [8.71, 47.26]
  }
}
```

```http
DELETE /api/features/{id}
Authorization: Bearer {token}
```

## 🛠️ Entwicklung

### Datenbank-Schema

**users**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'viewer'
);
```

**features**
```sql
CREATE TABLE features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    feature_type TEXT,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    properties TEXT,
    created_by INTEGER,
    created_at TEXT
);
```

### Entwickler-Modus

```bash
# Backend mit Debug-Modus
cd backend
python app_minimal.py  # Debug ist bereits aktiviert
```

## 🔒 Sicherheit

### Aktuelle Einschränkungen (Für Entwicklung OK, nicht für Produktion!)

⚠️ **Dieses System ist für Entwicklung/Demo konzipiert. Für Produktion beachten Sie:**

- Passwörter werden **im Klartext** gespeichert
- Kein HTTPS
- Einfacher Secret Key
- Keine Input-Validierung
- Keine Rate-Limiting

### Für Produktion

```python
# Passwörter hashen
from werkzeug.security import generate_password_hash, check_password_hash

# Sichere Secrets
import secrets
SECRET_KEY = secrets.token_hex(32)

# HTTPS verwenden
# Rate-Limiting hinzufügen
# Input-Sanitization
```

## 🤝 Beitragen

Contributions sind willkommen! Bitte:

1. Forken Sie das Repository
2. Erstellen Sie einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Pushen Sie zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

## 📋 Roadmap

- [ ] Linien und Polygone zeichnen
- [ ] Feature-Bearbeitung
- [ ] Erweiterte Filter-Funktionen
- [ ] Layer-System
- [ ] Export als GeoJSON/KML
- [ ] Passwort-Hashing
- [ ] Benutzer-Verwaltung (Admin-Panel)
- [ ] Responsive Design verbessern
- [ ] Docker-Support
- [ ] PostgreSQL/PostGIS Support

## 🐛 Bekannte Probleme

- Nur Punkt-Features unterstützt (keine Linien/Polygone)
- Keine räumlichen Abfragen (z.B. "Features in der Nähe")
- Passwörter unsicher gespeichert

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagungen

- [Leaflet](https://leafletjs.com/) - Für die großartige Kartenbibliothek
- [OpenStreetMap](https://www.openstreetmap.org/) - Für die freien Kartendaten
- [Flask](https://flask.palletsprojects.com/) - Für das einfache Web-Framework

## 📧 Kontakt

Projekt Link: [https://github.com/IHR-USERNAME/webgis-maennedorf](https://github.com/IHR-USERNAME/webgis-maennedorf)

---

⭐ Gefällt Ihnen das Projekt? Geben Sie ihm einen Stern!
