# GaubenMaster 📐

Eine Python-Anwendung zur Berechnung und Visualisierung von Dreiecken für den **Gaubenbau** basierend auf drei Seitenlängen (A, B, C).

## ✨ Features

- **Eingabe**: Drei Seitenlängen in Zentimetern
- **Berechnung**: Alle Winkel, Fläche, Umfang, Höhen, In-/Umkreisradius
- **Visualisierung**: Grafische Darstellung mit Maßen (Längen & Winkel)
- **Interaktion**: Maus-Drehung (Drag) und Zoom (Mausrad)
- **Silent Updates**: Automatische Update-Prüfung beim Start, silent Installation
- **Cross-Platform**: Läuft auf Windows, macOS, Linux

## 📸 Screenshot

```
+----------------------------------------------------------+
|  Eingabe          |  Visualisierung                      |
|  ┌─────────────┐  |  ┌────────────────────────────────┐  |
|  │ Seite a: 3.0│  |  │        C                       │  |
|  │ Seite b: 4.0│  |  │       / \                      │  |
|  │ Seite c: 5.0│  |  │  b  /   \  a                   │  |
|  ├─────────────┤  |  │    /     \                     │  |
|  │ Winkel α:36.9°│  |  │   /  γ    \                    │  |
|  │ Winkel β:53.1°│  |  │  /_________\                   │  |
|  │ Winkel γ:90.0°│  |  │ A    c     B                   │  |
|  │ Fläche: 6.00 │  |  │                                │  |
|  │ Umfang: 12.00│  |  │  Maus: Ziehen=Drehen, Rad=Zoom │  |
|  └─────────────┘  |  └────────────────────────────────┘  |
+----------------------------------------------------------+
```

## 🚀 Installation

### Windows Installer (empfohlen)

1. Gehe zu [Releases](https://github.com/soendi/GaubenMaster/releases)
2. Lade `GaubenMaster-Setup-<version>.exe` herunter
3. Führe die Datei aus und folge dem Installationsassistenten
4. GaubenMaster ist über das Startmenü oder Desktop-Verknüpfung startbar

### Installation aus Quellcode

**Voraussetzungen:**
- Python 3.8 oder höher
- pip (Python Package Manager)

```bash
# Repository klonen
git clone https://github.com/soendi/GaubenMaster.git
cd GaubenMaster

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# oder
venv\Scripts\activate     # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# Anwendung starten
python main.py
```

### Als Portable Version (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "GaubenMaster" main.py
# Die .exe befindet sich im dist/ Ordner
```

## 📖 Bedienung

### Dreieck eingeben
1. Starten Sie die Anwendung
2. Geben Sie die drei Seitenlängen in die Felder ein
3. Drücken Sie **Enter** oder klicken Sie auf **Berechnen**

### Gültigkeitsprüfung
Das Programm prüft automatisch die **Dreiecksungleichung**:
- a + b > c
- a + c > b  
- b + c > a

Bei ungültigen Werten wird eine Fehlermeldung angezeigt.

### Visualisierung bedienen
| Aktion | Wirkung |
|--------|---------|
| Linke Maustaste + Ziehen | Dreieck drehen |
| Mausrad | Hinein/Herauszoomen |
| Button "Ansicht zurücksetzen" | Ansicht auf 0° Rotation zurücksetzen |

### Berechnete Werte
- **Winkel** α, β, γ (in Grad)
- **Fläche** (in cm²)
- **Umfang** (in cm)
- **Höhen** ha, hb, hc (in cm)
- **Inkreisradius** & **Umkreisradius**

## 🔄 Silent Update-Funktion

GaubenMaster prüft **automatisch beim Start** auf Updates (einstellbar in den Einstellungen).

### Ablauf:
1. **Beim Start**: Hintergrund-Prüfung auf GitHub Releases
2. **Update gefunden**: Nicht-modale Benachrichtigung unten rechts
3. **Klick auf "Jetzt installieren"**: 
   - Installer wird heruntergeladen
   - Silent Installation (/SILENT /NORESTART)
   - Laufendes Programm wird geschlossen
   - Installation läuft im Hintergrund
   - Programm startet automatisch neu mit neuer Version

### Manuelle Update-Prüfung
- Menü: **Extras** → **Nach Updates suchen**
- Oder Button: **Nach Updates suchen** im Eingabepanel

### Repository öffnen
- Menü: **Extras** → **Repository öffnen**
- Öffnet die GitHub-Seite im Standardbrowser

## ⚙️ Konfiguration

Einstellungen über **Extras** → **Einstellungen**:
- Automatische Update-Prüfung beim Start an/aus
- Prüfintervall (Tage)
- Repository-URL anpassen

## 📁 Projektstruktur

```
GaubenMaster/
├── main.py                 # Hauptanwendung
├── requirements.txt        # Python-Abhängigkeiten
├── version.json           # Versionsinformation
├── README.md              # Diese Datei
├── LICENSE                # MIT Lizenz
├── setup.py               # Package-Setup
├── .gitignore             # Git-Ignore-Regeln
├── installer.nsi          # NSIS Installer Script
├── .github/workflows/     # CI/CD Pipelines
├── GaubenMaster/
│   ├── __init__.py
│   ├── calculator.py      # Berechnungslogik
│   ├── plot.py            # Visualisierung
│   ├── update.py          # Update-Management
│   └── gui.py             # GUI-Komponenten
└── tests/
    └── test_calculator.py # Unit Tests
```

## 🧮 Mathematische Grundlagen

### Kosinussatz (Winkelberechnung)
```
cos(α) = (b² + c² - a²) / (2bc)
cos(β) = (a² + c² - b²) / (2ac)
cos(γ) = (a² + b² - c²) / (2ab)
```

### Heronsche Formel (Fläche)
```
s = (a + b + c) / 2  (Halber Umfang)
A = √(s(s-a)(s-b)(s-c))
```

### Höhen
```
ha = 2A / a
hb = 2A / b
hc = 2A / c
```

### Inkreis- und Umkreisradius
```
r = A / s
R = (a * b * c) / (4A)
```

## 🛠️ Entwicklung

### Code-Qualität prüfen
```bash
# Linting
pip install flake8 black
flake8 .
black --check .

# Type Checking
pip install mypy
mypy .
```

### Tests ausführen
```bash
pip install pytest
pytest tests/
```

## 📦 Distribution

### PyPI Package erstellen
```bash
pip install build twine
python -m build
twine upload dist/*
```

### GitHub Release erstellen (baut Installer automatisch)
1. Tag erstellen: `git tag v1.0.0`
2. Push: `git push origin v1.0.0`
3. GitHub Actions erstellt automatisch:
   - Windows Installer (NSIS)
   - Portable .exe
   - Docker Image
   - PyPI Package

### Installer lokal bauen (Windows)
```bash
# NSIS installieren (https://nsis.sourceforge.io/Download)
# Dann:
makensis installer.nsi
# Output: GaubenMaster-Setup-<version>.exe
```

## 🤝 Mitwirken

1. Fork das Repository
2. Feature-Branch erstellen: `git checkout -b feature/amazing-feature`
3. Committen: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Pull Request erstellen

## 📄 Lizenz

Dieses Projekt steht unter der **MIT Lizenz** - siehe [LICENSE](LICENSE) für Details.

## 👨‍💻 Autor

**soendi**
- GitHub: [@soendi](https://github.com/soendi)
- Repository: [GaubenMaster](https://github.com/soendi/GaubenMaster)

## 🙏 Danksagungen

- [Matplotlib](https://matplotlib.org/) für die Visualisierung
- [NumPy](https://numpy.org/) für numerische Berechnungen
- [Tkinter](https://docs.python.org/3/library/tkinter.html) für die GUI
- [NSIS](https://nsis.sourceforge.io/) für den Windows Installer

---

⭐ **Wenn Ihnen das Projekt gefällt, geben Sie ihm einen Stern auf GitHub!**