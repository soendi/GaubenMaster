# Triangle Calculator 📐

Eine Python-Anwendung zur Berechnung und Visualisierung von Dreiecken basierend auf drei Seitenlängen (A, B, C).

## ✨ Features

- **Eingabe**: Drei Seitenlängen in Zentimetern
- **Berechnung**: Alle Winkel, Fläche, Umfang, Höhen
- **Visualisierung**: Grafische Darstellung mit Maßen (Längen & Winkel)
- **Interaktion**: Maus-Drehung (Drag) und Zoom (Mausrad)
- **Updates**: Automatische Update-Prüfung mit Benachrichtigung
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

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Installation aus Quellcode

```bash
# Repository klonen
git clone https://github.com/IHR_USERNAME/TriangleCalculator.git
cd TriangleCalculator

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

### Als ausführbare Datei (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "TriangleCalculator" main.py
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
| Button "Zurücksetzen" | Ansicht auf 0° Rotation zurücksetzen |

### Berechnete Werte
- **Winkel** α, β, γ (in Grad)
- **Fläche** (in cm²)
- **Umfang** (in cm)
- **Höhen** ha, hb, hc (in cm)

## 🔄 Update-Funktion

Die Anwendung prüft automatisch beim Start auf Updates (einstellbar in den Einstellungen).

### Manuelle Update-Prüfung
- Menü: **Extras** → **Nach Updates suchen**
- Oder Button: **Nach Updates suchen** im Eingabepanel

### Repository öffnen
- Menü: **Extras** → **Repository öffnen**
- Öffnet die GitHub-Seite im Standardbrowser

## ⚙️ Konfiguration

Einstellungen über **Extras** → **Einstellungen**:
- Automatische Update-Prüfung beim Start an/aus
- Repository-URL anpassen

## 📁 Projektstruktur

```
TriangleCalculator/
├── main.py              # Hauptanwendung
├── requirements.txt     # Python-Abhängigkeiten
├── version.json         # Versionsinformation
├── README.md           # Diese Datei
├── LICENSE             # MIT Lizenz
├── setup.py            # Package-Setup
├── .gitignore          # Git-Ignore-Regeln
└── TriangleCalculator/
    ├── __init__.py
    ├── calculator.py   # Berechnungslogik
    ├── plot.py         # Visualisierung
    ├── update.py       # Update-Management
    └── gui.py          # GUI-Komponenten
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

### GitHub Release erstellen
1. Tag erstellen: `git tag v1.0.0`
2. Push: `git push origin v1.0.0`
3. GitHub Actions erstellt automatisch Release

## 🤝 Mitwirken

1. Fork das Repository
2. Feature-Branch erstellen: `git checkout -b feature/amazing-feature`
3. Committen: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Pull Request erstellen

## 📄 Lizenz

Dieses Projekt steht unter der **MIT Lizenz** - siehe [LICENSE](LICENSE) für Details.

## 👨‍💻 Autor

**Ihr Name**
- GitHub: [@IHR_USERNAME](https://github.com/IHR_USERNAME)
- E-Mail: ihre.email@example.com

## 🙏 Danksagungen

- [Matplotlib](https://matplotlib.org/) für die Visualisierung
- [NumPy](https://numpy.org/) für numerische Berechnungen
- [Tkinter](https://docs.python.org/3/library/tkinter.html) für die GUI

---

⭐ **Wenn Ihnen das Projekt gefällt, geben Sie ihm einen Stern auf GitHub!**