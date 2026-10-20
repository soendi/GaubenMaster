"""
Dreiecksvisualisierungs-Modul
=============================

Matplotlib-basierte Visualisierung mit Maus-Interaktion.
"""

import math
import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from typing import Tuple, Optional


class TrianglePlot:
    """Matplotlib-basierte Dreiecksvisualisierung mit Maus-Interaktion."""

    def __init__(
        self, parent_frame: tk.Frame, figsize: Tuple[int, int] = (6, 6), dpi: int = 100
    ):
        """
        Initialisiert den Plot.

        Args:
            parent_frame: Tkinter Parent Frame
            figsize: Figurengröße in Zoll (Breite, Höhe)
            dpi: DPI für die Figur
        """
        self.parent_frame = parent_frame

        # Matplotlib Figur und Canvas
        self.fig = Figure(figsize=figsize, dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Dreieck-Daten
        self.vertices: Optional[Tuple[np.ndarray, np.ndarray, np.ndarray]] = None
        self.side_lengths: Tuple[float, float, float] = (0, 0, 0)
        self.angles: Tuple[float, float, float] = (0, 0, 0)
        self.rotation_angle: float = 0.0

        # Höhen-Teilungs Feature
        self.height_division_enabled: bool = False
        self.height_division_mode: str = "equal_parts"  # "equal_parts" oder "fixed_length"
        self.height_division_selected: str = "ha"  # "ha", "hb", "hc"
        self.height_division_n_parts: int = 5  # für equal_parts
        self.height_division_length: float = 2.0  # für fixed_length (cm)

        # Maus-Interaktion State
        self.dragging: bool = False
        self.last_mouse_pos: Optional[Tuple[float, float]] = None
        self.zoom_factor: float = 1.0

        # Event-Handler registrieren
        self._connect_events()

        # Plot initialisieren
        self.setup_plot()

    def _connect_events(self):
        """Verbindet Maus-Events."""
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.canvas.mpl_connect("resize_event", self.on_resize)

    def setup_plot(self):
        """Initialisiert den Plot mit Grundeinstellungen."""
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.grid(True, linestyle="--", alpha=0.3, color="gray")
        self.ax.set_xlabel("X (cm)", fontsize=10)
        self.ax.set_ylabel("Y (cm)", fontsize=10)
        self.ax.set_title("Dreieck Visualisierung", fontsize=12, fontweight="bold")
        self.ax.tick_params(labelsize=9)

        # Rand entfernen für sauberere Darstellung
        for spine in self.ax.spines.values():
            spine.set_visible(False)

    def set_triangle(self, a: float, b: float, c: float):
        """
        Setzt das Dreieck und berechnet alle Werte neu.

        Args:
            a, b, c: Seitenlängen
        """
        self.side_lengths = (a, b, c)

        # Import hier um Zirkelimport zu vermeiden
        from .calculator import TriangleCalculator

        if TriangleCalculator.validate_triangle(a, b, c):
            self.angles = TriangleCalculator.calculate_angles(a, b, c)
            self.vertices = TriangleCalculator.get_triangle_vertices(a, b, c)
            self.rotation_angle = 0.0
            self.zoom_factor = 1.0
            self.draw_triangle()
        else:
            self.vertices = None
            self.angles = (0, 0, 0)
            self.draw_error()

    def draw_triangle(self):
        """Zeichnet das Dreieck mit allen Maßen."""
        self.ax.clear()
        self.setup_plot()

        if self.vertices is None:
            self.draw_error()
            return

        # Dreieck rotieren
        rotated = self.rotate_vertices(self.vertices, self.rotation_angle)
        A, B, C = rotated

        # Dreieck zeichnen
        triangle = np.array([A, B, C, A])
        self.ax.plot(triangle[:, 0], triangle[:, 1], "b-", linewidth=2.5, zorder=3)
        self.ax.fill(
            triangle[:, 0], triangle[:, 1], alpha=0.1, color="steelblue", zorder=2
        )

        # Ecken markieren
        self.ax.plot(
            [A[0], B[0], C[0]],
            [A[1], B[1], C[1]],
            "ro",
            markersize=10,
            markerfacecolor="red",
            markeredgecolor="darkred",
            markeredgewidth=1.5,
            zorder=4,
        )

        # Ecken beschriften
        self._label_vertex(A, "A", "right", "top")
        self._label_vertex(B, "B", "left", "top")
        self._label_vertex(C, "C", "center", "bottom")

        # Seitenlängen anzeigen
        a, b, c = self.side_lengths
        self._label_sides(A, B, C, a, b, c)

        # Winkelbögen zeichnen
        alpha, beta, gamma = self.angles
        self.draw_angle_arc(A, B, C, alpha, "α")
        self.draw_angle_arc(B, C, A, beta, "β")
        self.draw_angle_arc(C, A, B, gamma, "γ")

        # Höhen-Teilung zeichnen
        self._draw_height_divisions(A, B, C)

        # Achsen skalieren mit Margin
        self._auto_scale(A, B, C)

        self.canvas.draw_idle()

    def _label_vertex(self, vertex: np.ndarray, label: str, ha: str, va: str):
        """Beschriftet einen Eckpunkt."""
        offset = 0.15
        if ha == "right":
            x_offset = -offset
        elif ha == "left":
            x_offset = offset
        else:
            x_offset = 0

        if va == "top":
            y_offset = -offset
        elif va == "bottom":
            y_offset = offset
        else:
            y_offset = 0

        self.ax.text(
            vertex[0] + x_offset,
            vertex[1] + y_offset,
            label,
            fontsize=13,
            ha=ha,
            va=va,
            fontweight="bold",
            color="black",
            zorder=5,
            bbox=dict(
                boxstyle="circle,pad=0.2",
                facecolor="white",
                edgecolor="none",
                alpha=0.8,
            ),
        )

    def _label_sides(
        self, A: np.ndarray, B: np.ndarray, C: np.ndarray, a: float, b: float, c: float
    ):
        """Beschriftet die Seitenlängen."""
        # Mittelpunkte der Seiten
        mid_ab = (A + B) / 2
        mid_bc = (B + C) / 2
        mid_ca = (C + A) / 2

        # Seitenlängen mit Offset beschriften
        offset = 0.4

        # Seite c (AB) - unten
        self.ax.text(
            mid_ab[0],
            mid_ab[1] - offset,
            f"c = {c:.1f} cm",
            ha="center",
            va="top",
            fontsize=10,
            color="navy",
            fontweight="bold",
            zorder=5,
            bbox=dict(
                boxstyle="round,pad=0.2", facecolor="white", edgecolor="navy", alpha=0.9
            ),
        )

        # Seite a (BC) - rechts
        self.ax.text(
            mid_bc[0] + offset,
            mid_bc[1],
            f"a = {a:.1f} cm",
            ha="left",
            va="center",
            fontsize=10,
            color="darkgreen",
            fontweight="bold",
            zorder=5,
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="white",
                edgecolor="darkgreen",
                alpha=0.9,
            ),
        )

        # Seite b (CA) - links
        self.ax.text(
            mid_ca[0] - offset,
            mid_ca[1],
            f"b = {b:.1f} cm",
            ha="right",
            va="center",
            fontsize=10,
            color="darkred",
            fontweight="bold",
            zorder=5,
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="white",
                edgecolor="darkred",
                alpha=0.9,
            ),
        )

    def draw_angle_arc(
        self,
        p1: np.ndarray,
        p2: np.ndarray,
        p3: np.ndarray,
        angle_deg: float,
        label: str,
    ):
        """
        Zeichnet einen Winkelbogen an Ecke p2 zwischen p1-p2 und p2-p3.

        Args:
            p1, p2, p3: Eckpunkte (p2 ist der Scheitelpunkt)
            angle_deg: Winkel in Grad
            label: Beschriftung (z.B. 'α', 'β', 'γ')
        """
        # Vektoren vom Scheitelpunkt
        v1 = p1 - p2
        v2 = p3 - p2

        # Winkel der Vektoren
        ang1 = math.atan2(v1[1], v1[0])
        ang2 = math.atan2(v2[1], v2[0])

        # Sicherstellen, dass wir den inneren Winkel zeichnen (kürzerer Bogen)
        diff = ang2 - ang1
        while diff <= -math.pi:
            diff += 2 * math.pi
        while diff > math.pi:
            diff -= 2 * math.pi

        # Wenn diff negativ, Richtung umkehren
        if diff < 0:
            ang1, ang2 = ang2, ang1

        # Bogen radius (abhängig von Dreiecksgröße)
        radius = min(np.linalg.norm(v1), np.linalg.norm(v2)) * 0.18
        radius = max(radius, 0.3)  # Mindestradius

        # Bogen zeichnen
        theta = np.linspace(ang1, ang2, 40)
        arc_x = p2[0] + radius * np.cos(theta)
        arc_y = p2[1] + radius * np.sin(theta)
        self.ax.plot(arc_x, arc_y, "r-", linewidth=2, zorder=4)

        # Winkelbeschriftung
        mid_angle = (ang1 + ang2) / 2
        label_radius = radius * 1.6
        label_x = p2[0] + label_radius * math.cos(mid_angle)
        label_y = p2[1] + label_radius * math.sin(mid_angle)

        self.ax.text(
            label_x,
            label_y,
            f"{label} = {angle_deg:.1f}°",
            ha="center",
            va="center",
            fontsize=10,
            color="crimson",
            fontweight="bold",
            zorder=5,
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="white",
                edgecolor="crimson",
                alpha=0.9,
            ),
        )

    def draw_error(self):
        """Zeigt Fehlermeldung bei ungültigem Dreieck."""
        self.ax.clear()
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis("off")
        self.ax.text(
            0.5,
            0.5,
            "⚠ Kein gültiges Dreieck!\n\nPrüfen Sie die Seitenlängen.\nDie Dreiecksungleichung muss erfüllt sein:\na + b > c, a + c > b, b + c > a",
            ha="center",
            va="center",
            fontsize=14,
            color="crimson",
            transform=self.ax.transAxes,
            bbox=dict(
                boxstyle="round,pad=1",
                facecolor="#fff0f0",
                edgecolor="crimson",
                alpha=0.9,
            ),
        )
        self.canvas.draw_idle()

    def rotate_vertices(
        self, vertices: Tuple[np.ndarray, np.ndarray, np.ndarray], angle_deg: float
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Rotiert die Ecken um den geometrischen Mittelpunkt."""
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        # Geometrischen Mittelpunkt (Schwerpunkt) berechnen
        center = np.mean(vertices, axis=0)

        rotated = []
        for v in vertices:
            # Zum Ursprung verschieben
            v_translated = v - center
            # Rotieren
            v_rotated = np.array(
                [
                    v_translated[0] * cos_a - v_translated[1] * sin_a,
                    v_translated[0] * sin_a + v_translated[1] * cos_a,
                ],
                dtype=float,
            )
            # Zurückverschieben
            rotated.append(v_rotated + center)

        return tuple(rotated)

    def _auto_scale(self, A: np.ndarray, B: np.ndarray, C: np.ndarray):
        """Skaliert die Achsen automatisch mit Margin."""
        all_points = np.array([A, B, C])
        x_min, x_max = all_points[:, 0].min(), all_points[:, 0].max()
        y_min, y_max = all_points[:, 1].min(), all_points[:, 1].max()

        x_range = x_max - x_min
        y_range = y_max - y_min
        max_range = max(x_range, y_range)

        if max_range == 0:
            max_range = 1.0

        margin = max_range * 0.2 * self.zoom_factor

        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        half_range = max_range / 2 * self.zoom_factor + margin

        self.ax.set_xlim(x_center - half_range, x_center + half_range)
        self.ax.set_ylim(y_center - half_range, y_center + half_range)

    # --- Höhen-Teilungs Methoden ---

    def _get_height_foot_and_line(
        self, A: np.ndarray, B: np.ndarray, C: np.ndarray, height_selection: str
    ) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Berechnet den Fußpunkt der Höhe, den Höhenvektor und die Höhenlänge.

        Args:
            A, B, C: Dreiecksecken (nach Rotation)
            height_selection: "ha", "hb" oder "hc"

        Returns:
            Tuple: (Fußpunkt, Höhenende (Ecke), Höhenlänge)
        """
        a, b, c = self.side_lengths

        if height_selection == "ha":
            # Höhe auf Seite a (BC), von Ecke A aus
            foot = self._project_point_to_line(A, B, C)
            height_vec = A - foot
            height_len = np.linalg.norm(height_vec)
            return foot, A, height_len
        elif height_selection == "hb":
            # Höhe auf Seite b (CA), von Ecke B aus
            foot = self._project_point_to_line(B, C, A)
            height_vec = B - foot
            height_len = np.linalg.norm(height_vec)
            return foot, B, height_len
        else:  # "hc"
            # Höhe auf Seite c (AB), von Ecke C aus
            foot = self._project_point_to_line(C, A, B)
            height_vec = C - foot
            height_len = np.linalg.norm(height_vec)
            return foot, C, height_len

    def _project_point_to_line(self, P: np.ndarray, L1: np.ndarray, L2: np.ndarray) -> np.ndarray:
        """Projiziert Punkt P auf die Linie durch L1 und L2."""
        line_vec = L2 - L1
        line_len_sq = np.dot(line_vec, line_vec)
        if line_len_sq == 0:
            return L1
        t = np.dot(P - L1, line_vec) / line_len_sq
        return L1 + t * line_vec

    def _calculate_division_points(
        self, foot: np.ndarray, vertex: np.ndarray, height_len: float
    ) -> List[float]:
        """
        Berechnet die Teilungspunkte entlang der Höhe (Abstand vom Fußpunkt).

        Returns:
            Liste der Abstände vom Fußpunkt entlang der Höhe
        """
        if self.height_division_mode == "equal_parts":
            n = max(1, self.height_division_n_parts)
            return [height_len * i / n for i in range(1, n)]  # ohne 0 und height_len
        else:  # fixed_length
            length = max(0.1, self.height_division_length)
            points = []
            d = length
            while d < height_len - 1e-9:
                points.append(d)
                d += length
            return points

    def _draw_height_divisions(
        self, A: np.ndarray, B: np.ndarray, C: np.ndarray
    ):
        """Zeichnet die Höhen-Teilungslinien."""
        if not self.height_division_enabled:
            return

        foot, vertex, height_len = self._get_height_foot_and_line(
            A, B, C, self.height_division_selected
        )

        if height_len < 1e-9:
            return

        # Höhe zeichnen (gestrichelt)
        self.ax.plot(
            [foot[0], vertex[0]],
            [foot[1], vertex[1]],
            "g--",
            linewidth=1.5,
            alpha=0.7,
            zorder=3,
            label=f"Höhe {self.height_division_selected.upper()}",
        )

        # Fußpunkt markieren
        self.ax.plot(
            foot[0],
            foot[1],
            "go",
            markersize=8,
            markerfacecolor="green",
            markeredgecolor="darkgreen",
            markeredgewidth=1.5,
            zorder=4,
        )

        # Beschriftung am Fußpunkt
        self.ax.text(
            foot[0],
            foot[1],
            f"F{self.height_division_selected.upper()}",
            fontsize=9,
            ha="center",
            va="bottom",
            fontweight="bold",
            color="darkgreen",
            zorder=5,
            bbox=dict(
                boxstyle="circle,pad=0.2", facecolor="white", edgecolor="darkgreen", alpha=0.9
            ),
        )

        # Höhenlänge beschriften
        mid_height = (foot + vertex) / 2
        self.ax.text(
            mid_height[0],
            mid_height[1],
            f"{self.height_division_selected.upper()} = {height_len:.1f} cm",
            fontsize=9,
            ha="center",
            va="center",
            fontweight="bold",
            color="green",
            zorder=5,
            bbox=dict(
                boxstyle="round,pad=0.2", facecolor="white", edgecolor="green", alpha=0.9
            ),
        )

        # Teilungspunkte berechnen und zeichnen
        division_distances = self._calculate_division_points(foot, vertex, height_len)

        # Höhen-Vektor normieren
        height_vec = vertex - foot
        height_dir = height_vec / height_len if height_len > 0 else np.array([0.0, 0.0])

        # Perpendikuläre Richtung (90° links)
        perp_dir = np.array([-height_dir[1], height_dir[0]])

        # Ausdehnung der Perpendikulären (für visuelle Linieneinzeichnung)
        # Wir zeichnen von der Höhe weg, senkrecht zur Höhe
        perp_length = max(
            np.linalg.norm(B - A), np.linalg.norm(C - B), np.linalg.norm(A - C)
        ) * 0.15

        for i, dist in enumerate(division_distances):
            point_on_height = foot + height_dir * dist

            # Perpendikuläre Linie zeichnen (in beide Richtungen)
            line_start = point_on_height - perp_dir * perp_length
            line_end = point_on_height + perp_dir * perp_length

            self.ax.plot(
                [line_start[0], line_end[0]],
                [line_start[1], line_end[1]],
                "g-",
                linewidth=1,
                alpha=0.8,
                zorder=3,
            )

            # Beschriftung der Teilung
            label_pos = point_on_height + perp_dir * perp_length * 1.1
            if self.height_division_mode == "equal_parts":
                label = f"{i+1}/{self.height_division_n_parts}"
            else:
                label = f"{dist:.1f} cm"
            self.ax.text(
                label_pos[0],
                label_pos[1],
                label,
                fontsize=8,
                ha="center",
                va="center",
                color="darkgreen",
                fontweight="bold",
                zorder=5,
                bbox=dict(
                    boxstyle="round,pad=0.15",
                    facecolor="white",
                    edgecolor="green",
                    alpha=0.9,
                ),
            )

        # Legende für Teilung
        if self.height_division_mode == "equal_parts":
            legend_text = f"Gleichmäßig in {self.height_division_n_parts} Teile"
        else:
            legend_text = f"Teile à {self.height_division_length:.1f} cm"
        self.ax.text(
            0.02,
            0.98,
            f"Höhe {self.height_division_selected.upper()}: {legend_text}",
            transform=self.ax.transAxes,
            fontsize=9,
            va="top",
            ha="left",
            color="darkgreen",
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.3", facecolor="lightgreen", edgecolor="green", alpha=0.8
            ),
        )

    # --- Event Handler ---

    def on_press(self, event):
        """Mausklick-Handler: Linksklick startet Drag."""
        if event.inaxes == self.ax and event.button == 1:
            if event.xdata is not None and event.ydata is not None:
                self.dragging = True
                self.last_mouse_pos = (event.xdata, event.ydata)
                self.canvas.get_tk_widget().config(cursor="fleur")

    def on_release(self, event):
        """Mausloslass-Handler: Beendet Drag."""
        if event.button == 1:
            self.dragging = False
            self.last_mouse_pos = None
            self.canvas.get_tk_widget().config(cursor="")

    def on_motion(self, event):
        """Mausbewegungs-Handler: Dreht das Dreieck bei Drag."""
        if (
            self.dragging
            and event.inaxes == self.ax
            and self.last_mouse_pos is not None
            and event.xdata is not None
            and event.ydata is not None
        ):

            # Winkeländerung basierend auf horizontaler Mausbewegung
            dx = event.xdata - self.last_mouse_pos[0]
            # Empfindlichkeit: 100 Grad pro Einheit
            self.rotation_angle += dx * 100
            self.rotation_angle %= 360
            self.draw_triangle()
            self.last_mouse_pos = (event.xdata, event.ydata)

    def on_scroll(self, event):
        """Mausrad-Handler: Zoom."""
        if event.inaxes == self.ax:
            # Zoom-Faktor
            scale_factor = 0.9 if event.button == "up" else 1.1
            self.zoom_factor *= scale_factor
            self.zoom_factor = max(0.1, min(10.0, self.zoom_factor))  # Begrenzen

            if self.vertices is not None:
                rotated = self.rotate_vertices(self.vertices, self.rotation_angle)
                self._auto_scale(*rotated)
                self.canvas.draw_idle()

    def on_resize(self, event):
        """Fenstergröße geändert - Neuzeichnen."""
        self.canvas.draw_idle()

    def reset_view(self):
        """Setzt Rotation und Zoom zurück."""
        self.rotation_angle = 0.0
        self.zoom_factor = 1.0
        if self.vertices is not None:
            self.draw_triangle()

    def get_state(self) -> dict:
        """Gibt aktuellen State zurück (für Speichern)."""
        return {
            "rotation_angle": self.rotation_angle,
            "zoom_factor": self.zoom_factor,
            "side_lengths": self.side_lengths,
            "angles": self.angles,
        }

    def set_state(self, state: dict):
        """Setzt State (beim Laden)."""
        self.rotation_angle = state.get("rotation_angle", 0.0)
        self.zoom_factor = state.get("zoom_factor", 1.0)
        if self.vertices is not None:
            self.draw_triangle()


def create_standalone_plot(
    a: float,
    b: float,
    c: float,
    output_path: str = "triangle.png",
    figsize: Tuple[int, int] = (8, 8),
    dpi: int = 150,
) -> bool:
    """
    Erstellt eine statische Dreiecks-Grafik als Bilddatei.

    Args:
        a, b, c: Seitenlängen
        output_path: Ausgabepfad
        figsize: Figurengröße
        dpi: Auflösung

    Returns:
        True bei Erfolg
    """
    from .calculator import TriangleCalculator

    if not TriangleCalculator.validate_triangle(a, b, c):
        return False

    angles = TriangleCalculator.calculate_angles(a, b, c)
    vertices = TriangleCalculator.get_triangle_vertices(a, b, c)

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_xlabel("X (cm)")
    ax.set_ylabel("Y (cm)")
    ax.set_title(f"Dreieck: a={a}, b={b}, c={c}")

    A, B, C = vertices
    triangle = np.array([A, B, C, A])
    ax.plot(triangle[:, 0], triangle[:, 1], "b-", linewidth=2)
    ax.fill(triangle[:, 0], triangle[:, 1], alpha=0.1, color="blue")
    ax.plot([A[0], B[0], C[0]], [A[1], B[1], C[1]], "ro", markersize=8)

    # Beschriftungen
    for v, label in zip([A, B, C], ["A", "B", "C"]):
        ax.text(
            v[0], v[1], label, fontsize=12, ha="center", va="center", fontweight="bold"
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close()
    return True
