# Männedorf WebGIS - Bauzonen Karte

Eine interaktive WebGIS-Anwendung für die Visualisierung von Bauzonen in Männedorf, Kanton Zürich.

## 🚀 Live Demo
[Zur Live-Version](https://IHR-BENUTZERNAME.github.io/maennedorf-webgis)

![WebGIS Screenshot](https://via.placeholder.com/800x400.png?text=Männedorf+WebGIS+Screenshot)

## 📋 Funktionen

### 🗺️ Kartenfunktionen
- **Interaktive Karte** mit Leaflet.js
- **Mehrere Basiskarten**: OpenStreetMap, Satellitenbild, Topografische Karte
- **Koordinaten-Anzeige** in Echtzeit
- **Zoom und Panning** mit intuitiver Navigation

### 🏘️ Bauzonen-Daten
- **WFS-Daten** vom Kanton Zürich (Echtzeit)
- **Demo-Daten** für Testzwecke
- **Bauzonen Schweiz** (harmonisiert)
- **Farbkodierte Zonentypen**:
  - 🟥 Wohnzonen
  - 🟦 Gewerbezonen  
  - 🟨 Mischzonen
  - 🟩 Freihaltezonen
  - 🟫 Landwirtschaftszonen

### 🔍 Analyse-Werkzeuge
- **Erweiterte Filter** nach Zonentyp, Fläche und Datenquelle
- **Suchfunktion** für Adressen und Koordinaten
- **Messwerkzeuge** für Distanzen
- **Info-Abfrage** für Layer-Informationen

### 📊 Datenmanagement
- **Attributtabelle** mit allen Bauzonen-Daten
- **Statistik-Dashboard** mit Übersichtsmetriken
- **Datenexport** als CSV
- **Druckfunktion** für Kartenausschnitte

## 🛠️ Installation & Lokale Entwicklung

### Voraussetzungen
- Moderner Webbrowser (Chrome, Firefox, Safari, Edge)
- Lokaler Webserver für Entwicklung

### Lokale Installation
```bash
# Repository klonen
git clone https://github.com/IHR-BENUTZERNAME/maennedorf-webgis.git

# In Verzeichnis wechseln
cd maennedorf-webgis

# Lokalen Server starten
# Python 3:
python -m http.server 8000

# Python 2:
python -m SimpleHTTPServer 8000

# Mit Node.js:
npx http-server

# Mit PHP:
php -S localhost:8000