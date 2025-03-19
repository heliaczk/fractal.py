# 3D Fraktal Explorer

Ein interaktiver Fraktal-Explorer, der verschiedene mathematische Fraktale in einer 3D-ähnlichen Umgebung visualisiert. Das Programm wurde mit Python, Pygame und Numba entwickelt.

## Funktionen

- Drei verschiedene Fraktale zur Auswahl:
  - Mandelbrot-Set
  - Julia-Set
  - Burning Ship-Fraktal
- Interaktive 3D-ähnliche Visualisierung
- Echtzeit-Rotation und Z-Achsen-Bewegung
- Dynamische Iterationsanpassung
- Zoom- und Pan-Funktionalität

## Installation

1. Stellen Sie sicher, dass Python 3.x installiert ist
2. Installieren Sie die erforderlichen Pakete:
```bash
pip install numpy pygame numba
```

## Steuerung

- **Mausrad**: Hinein- und Herauszoomen
- **Linke Maustaste + Ziehen**: Verschieben der Ansicht
- **Leertaste**: Zwischen den Fraktalen wechseln
- **W/S**: Z-Position anpassen (3D-Effekt)
- **Q/E**: Rotation der Ansicht
- **Pfeiltasten (↑/↓)**: Anzahl der Iterationen erhöhen/verringern

## Technische Details

- Verwendung von Numba (@jit) für beschleunigte Berechnungen
- Dynamische Iterationsanpassung basierend auf dem Zoom-Level
- Echtzeit-Farbberechnungen für visuelle Effekte
- Optimierte Performance durch NumPy-Arrays

## Systemanforderungen

- Python 3.x
- Pygame
- NumPy
- Numba
- Mindestens 2GB RAM
- Grafikkarte mit OpenGL-Unterstützung

## Start des Programms

```bash
python main.py
```
