import numpy as np
import pygame
import sys
from typing import Callable, Dict, Tuple
from numba import jit
import math

# Konstanten
BREITE = 800
HOEHE = 600
MIN_ITERATIONEN = 100
MAX_ITERATIONEN = 1000
SCROLL_SPEED = 0.1
ROTATION_SPEED = 0.02
ITERATION_STEP = 50  # Schrittweite für Iterationsänderung

# Initialisierung von Pygame
pygame.init()
screen = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("3D Fraktal Explorer")
pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

@jit(nopython=True)
def mandelbrot(h: float, w: float, max_iter: int) -> int:
    c = complex(w, h)
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

@jit(nopython=True)
def julia(h: float, w: float, max_iter: int) -> int:
    c = complex(-0.4, 0.6)  # Julia-Set Parameter
    z = complex(w, h)
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

@jit(nopython=True)
def burning_ship(h: float, w: float, max_iter: int) -> int:
    c = complex(w, h)
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = complex(abs(z.real), abs(z.imag))
        z = z*z + c
    return max_iter

def rotate_point(x: float, y: float, theta: float) -> Tuple[float, float]:
    """Rotiert einen Punkt um den Ursprung."""
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    return (x * cos_t - y * sin_t, x * sin_t + y * cos_t)

def berechne_fraktal(
    x_min: float, 
    x_max: float, 
    y_min: float, 
    y_max: float,
    rotation: float,
    max_iter: int,
    formel: Callable = mandelbrot
) -> np.ndarray:
    """Berechnet das Fraktal basierend auf den gegebenen Parametern."""
    y, x = np.ogrid[y_min:y_max:HOEHE*1j, x_min:x_max:BREITE*1j]
    
    # Mesh für die Rotation erstellen
    x_mesh, y_mesh = np.meshgrid(np.linspace(x_min, x_max, BREITE), 
                                np.linspace(y_min, y_max, HOEHE))
    
    # Rotation anwenden
    cos_t = math.cos(rotation)
    sin_t = math.sin(rotation)
    x_rot = x_mesh * cos_t - y_mesh * sin_t
    y_rot = x_mesh * sin_t + y_mesh * cos_t
    
    # Fraktal berechnen
    fraktal = np.frompyfunc(lambda h, w: formel(h, w, max_iter), 2, 1)(y_rot, x_rot).astype(np.float64)
    return fraktal

def main():
    # Anfängliche Ansicht
    x_min, x_max = -2, 1
    y_min, y_max = -1.5, 1.5
    zoom_faktor = 0.1
    rotation = 0.0
    z_position = 0.0
    aktuelle_iterationen = MIN_ITERATIONEN
    basis_zoom = abs(x_max - x_min)
    
    # Verfügbare Fraktale
    fraktale: Dict[int, Tuple[Callable, str]] = {
        0: (mandelbrot, "Mandelbrot"),
        1: (julia, "Julia"),
        2: (burning_ship, "Burning Ship")
    }
    aktuelles_fraktal = 0
    
    clock = pygame.time.Clock()
    laufend = True
    mouse_pressed = False
    last_mouse_pos = (0, 0)

    while laufend:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                laufend = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [4, 5]:  # Mausrad
                    maus_pos = pygame.mouse.get_pos()
                    maus_x = maus_pos[0] / BREITE
                    maus_y = maus_pos[1] / HOEHE
                    
                    # Berechne Zielpunkt für Zoom
                    ziel_x = x_min + (x_max - x_min) * maus_x
                    ziel_y = y_min + (y_max - y_min) * maus_y
                    
                    if event.button == 4:  # Reinzoomen
                        faktor = 1.0 - zoom_faktor
                    else:  # Rauszoomen
                        faktor = 1.0 + zoom_faktor
                    
                    # Zoom um Mausposition
                    x_min = ziel_x - (ziel_x - x_min) * faktor
                    x_max = ziel_x + (x_max - ziel_x) * faktor
                    y_min = ziel_y - (ziel_y - y_min) * faktor
                    y_max = ziel_y + (y_max - ziel_y) * faktor
                    
                    # Iterationen basierend auf Zoom-Level anpassen
                    aktueller_zoom = abs(x_max - x_min)
                    zoom_faktor_relativ = aktueller_zoom / basis_zoom
                    aktuelle_iterationen = min(
                        MAX_ITERATIONEN,
                        int(MIN_ITERATIONEN * (1 + math.log(1 / zoom_faktor_relativ + 1)))
                    )
                    
                elif event.button == 1:  # Linke Maustaste
                    mouse_pressed = True
                    last_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressed = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Wechsel zwischen Fraktalen
                    aktuelles_fraktal = (aktuelles_fraktal + 1) % len(fraktale)
                elif event.key == pygame.K_w:
                    z_position += SCROLL_SPEED
                elif event.key == pygame.K_s:
                    z_position -= SCROLL_SPEED
                elif event.key == pygame.K_q:
                    rotation -= ROTATION_SPEED
                elif event.key == pygame.K_e:
                    rotation += ROTATION_SPEED
                elif event.key == pygame.K_UP:
                    # Erhöhe Iterationen
                    aktuelle_iterationen = min(MAX_ITERATIONEN, aktuelle_iterationen + ITERATION_STEP)
                elif event.key == pygame.K_DOWN:
                    # Verringere Iterationen
                    aktuelle_iterationen = max(MIN_ITERATIONEN, aktuelle_iterationen - ITERATION_STEP)

        # Maus-Drag für Pan
        if mouse_pressed:
            current_pos = pygame.mouse.get_pos()
            dx = (current_pos[0] - last_mouse_pos[0]) / BREITE
            dy = (current_pos[1] - last_mouse_pos[1]) / HOEHE
            bereich_x = x_max - x_min
            bereich_y = y_max - y_min
            x_min -= dx * bereich_x
            x_max -= dx * bereich_x
            y_min -= dy * bereich_y
            y_max -= dy * bereich_y
            last_mouse_pos = current_pos

        # Fraktal berechnen
        fraktal = berechne_fraktal(
            x_min, x_max, y_min, y_max,
            rotation,
            aktuelle_iterationen,
            fraktale[aktuelles_fraktal][0]
        )
        
        # 3D-Effekt durch z_position
        zoom_scale = 1.0 + z_position
        fraktal = fraktal * zoom_scale
        
        # Farbgebung
        farben = (fraktal * 255 / (aktuelle_iterationen * zoom_scale)).astype(np.uint8)
        surf = pygame.surfarray.make_surface(np.stack((
            farben,
            (farben * 2) % 256,
            (farben * 4) % 256
        ), axis=-1))
        
        screen.blit(surf, (0, 0))
        
        # UI-Text rendern
        text = font.render(f"Fraktal: {fraktale[aktuelles_fraktal][1]} (Leertaste zum Wechseln)", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        text = font.render(f"Z-Position: {z_position:.2f} (W/S)", True, (255, 255, 255))
        screen.blit(text, (10, 30))
        text = font.render(f"Rotation: {rotation:.2f} (Q/E)", True, (255, 255, 255))
        screen.blit(text, (10, 50))
        text = font.render(f"Iterationen: {aktuelle_iterationen} (Pfeiltasten ↑↓)", True, (255, 255, 255))
        screen.blit(text, (10, 70))
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 