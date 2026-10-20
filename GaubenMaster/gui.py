"""
GUI-Modul für GaubenMaster
==========================

Enthält alle Tkinter-basierten GUI-Komponenten.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Optional, Callable, Dict, Any

from .calculator import TriangleCalculator, get_triangle_properties
from .plot import TrianglePlot
from .update import UpdateManager, VersionInfo


class InputPanel(ttk.LabelFrame):
    """Eingabe-Panel für Dreiecksseiten."""
    
    def __init__(self, parent, on_calculate: Callable, on_reset: Callable,
                 on_update_check: Callable, update_manager: UpdateManager):
        super().__init__(parent, text="Dreiecks-Eingabe", padding="15")
        
        self.on_calculate = on_calculate
        self.on_reset = on_reset
        self.on_update_check = on_update_check
        self.update_manager = update_manager
        
        # Variablen
        self.side_a = tk.DoubleVar(value=3.0)
        self.side_b = tk.DoubleVar(value=4.0)
        self.side_c = tk.DoubleVar(value=5.0)
        
        self._setup_ui()
        self.columnconfigure(1, weight=1)
    
    def _setup_ui(self):
        """Erstellt die UI-Elemente."""
        # Seitenlängen
        self._create_input_row(0, "Seite a (cm):", self.side_a)
        self._create_input_row(1, "Seite b (cm):", self.side_b)
        self._create_input_row(2, "Seite c (cm):", self.side_c)
        
        # Trennlinie
        ttk.Separator(self, orient='horizontal').grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # Berechnete Werte
        ttk.Label(self, text="Berechnete Werte:", 
                 font=('Arial', 11, 'bold')).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Winkel
        self.alpha_label = self._create_result_row(5, "Winkel α:")
        self.beta_label = self._create_result_row(6, "Winkel β:")
        self.gamma_label = self._create_result_row(7, "Winkel γ:")
        
        ttk.Separator(self, orient='horizontal').grid(
            row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Weitere Eigenschaften
        self.area_label = self._create_result_row(9, "Fläche:")
        self.perimeter_label = self._create_result_row(10, "Umfang:")
        self.ha_label = self._create_result_row(11, "Höhe ha:")
        self.hb_label = self._create_result_row(12, "Höhe hb:")
        self.hc_label = self._create_result_row(13, "Höhe hc:")
        
        ttk.Separator(self, orient='horizontal').grid(
            row=14, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=15, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        
        ttk.Button(btn_frame, text="Berechnen", command=self._on_calculate_click,
                  style='Accent.TButton').grid(row=0, column=0, sticky=(tk.W, tk.E), padx=2)
        ttk.Button(btn_frame, text="Zurücksetzen", command=self.on_reset).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=2)
        
        # Update-Button
        ttk.Button(self, text="Nach Updates suchen", command=self.on_update_check).grid(
            row=16, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Version
        self.version_label = ttk.Label(self, 
            text=f"Version: {self.update_manager.current_version}",
            font=('Arial', 8), foreground='gray')
        self.version_label.grid(row=17, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Validierung
        self.validation_label = ttk.Label(self, text="", font=('Arial', 9), foreground='red')
        self.validation_label.grid(row=18, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
    
    def _create_input_row(self, row: int, label_text: str, variable: tk.DoubleVar):
        """Erstellt eine Eingabezeile."""
        ttk.Label(self, text=label_text, font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        entry = ttk.Entry(self, textvariable=variable, width=15, font=('Arial', 11))
        entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        entry.bind('<KeyRelease>', lambda e: self._on_input_change())
        entry.bind('<Return>', lambda e: self._on_calculate_click())
        return entry
    
    def _create_result_row(self, row: int, label_text: str) -> ttk.Label:
        """Erstellt eine Ergebniszeile."""
        ttk.Label(self, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=2)
        label = ttk.Label(self, text="--", font=('Arial', 10, 'bold'), foreground='blue')
        label.grid(row=row, column=1, sticky=tk.W, pady=2, padx=5)
        return label
    
    def _on_input_change(self):
        """Validierung bei Eingabeänderung."""
        try:
            a = self.side_a.get()
            b = self.side_b.get()
            c = self.side_c.get()
            
            if a > 0 and b > 0 and c > 0:
                if TriangleCalculator.validate_triangle(a, b, c):
                    self.validation_label.config(text="✓ Gültiges Dreieck", foreground='green')
                else:
                    self.validation_label.config(
                        text="✗ Dreiecksungleichung verletzt", foreground='red')
            else:
                self.validation_label.config(text="")
        except tk.TclError:
            pass
    
    def _on_calculate_click(self):
        """Wrapper für Calculate-Callback."""
        self.on_calculate()
    
    def get_values(self) -> tuple:
        """Gibt die aktuellen Werte zurück."""
        return (self.side_a.get(), self.side_b.get(), self.side_c.get())
    
    def set_values(self, a: float, b: float, c: float):
        """Setzt die Werte."""
        self.side_a.set(a)
        self.side_b.set(b)
        self.side_c.set(c)
    
    def update_results(self, props: Dict[str, Any]):
        """Aktualisiert die Ergebnis-Labels."""
        if not props.get("valid", False):
            self._show_error(props.get("error", "Ungültiges Dreieck"))
            return
        
        angles = props["angles"]
        self.alpha_label.config(text=f"{angles['alpha']:.2f}°")
        self.beta_label.config(text=f"{angles['beta']:.2f}°")
        self.gamma_label.config(text=f"{angles['gamma']:.2f}°")
        
        self.area_label.config(text=f"{props['area']:.2f} cm²")
        self.perimeter_label.config(text=f"{props['perimeter']:.2f} cm")
        
        heights = props["heights"]
        self.ha_label.config(text=f"{heights['ha']:.2f} cm")
        self.hb_label.config(text=f"{heights['hb']:.2f} cm")
        self.hc_label.config(text=f"{heights['hc']:.2f} cm")
        
        self.validation_label.config(text="✓ Gültiges Dreieck", foreground='green')
    
    def _show_error(self, message: str):
        """Zeigt Fehlerzustand."""
        for label in [self.alpha_label, self.beta_label, self.gamma_label,
                      self.area_label, self.perimeter_label,
                      self.ha_label, self.hb_label, self.hc_label]:
            label.config(text="--")
        self.validation_label.config(text=f"✗ {message}", foreground='red')
    
    def update_version_label(self):
        """Aktualisiert Versionsanzeige."""
        self.version_label.config(text=f"Version: {self.update_manager.current_version}")
    
    
class VisualizationPanel(ttk.LabelFrame):
    """Visualisierungs-Panel mit Matplotlib Canvas."""
    
    def __init__(self, parent):
        super().__init__(parent, text="Dreieck Visualisierung", padding="5")
        
        self.triangle_plot = None
        self._setup_ui()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
    
    def _setup_ui(self):
        """Erstellt die UI."""
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(toolbar, text="Maus: Ziehen=Drehen  |  Rad=Zoom", 
                 font=('Arial', 9), foreground='gray').pack(side=tk.LEFT)
        
        ttk.Button(toolbar, text="Ansicht zurücksetzen", 
                  command=self.reset_view).pack(side=tk.RIGHT, padx=5)
        
        # Plot Frame
        plot_frame = ttk.Frame(self)
        plot_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        
        self.triangle_plot = TrianglePlot(plot_frame)
    
    def set_triangle(self, a: float, b: float, c: float):
        """Setzt das anzuzeigende Dreieck."""
        if self.triangle_plot:
            self.triangle_plot.set_triangle(a, b, c)
    
    def reset_view(self):
        """Setzt die Ansicht zurück."""
        if self.triangle_plot:
            self.triangle_plot.reset_view()
    
    def get_plot_state(self) -> dict:
        """Gibt Plot-State zurück."""
        if self.triangle_plot:
            return self.triangle_plot.get_state()
        return {}
    
    def set_plot_state(self, state: dict):
        """Setzt Plot-State."""
        if self.triangle_plot:
            self.triangle_plot.set_state(state)
    
    
class StatusBar(ttk.Frame):
    """Statusleiste am unteren Fensterrand."""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.status_var = tk.StringVar(value="Bereit")
        self.status_label = ttk.Label(self, textvariable=self.status_var, 
                                     relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        self.status_label.pack(fill=tk.X)
    
    def set_status(self, message: str):
        """Setzt Status-Text."""
        self.status_var.set(message)
    
    
class MenuBar(tk.Menu):
    """Hauptmenü der Anwendung."""
    
    def __init__(self, parent, callbacks: Dict[str, Callable]):
        super().__init__(parent)
        
        self.callbacks = callbacks
        self._create_menus()
    
    def _create_menus(self):
        """Erstellt alle Menüs."""
        # Datei
        file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Neu", command=self.callbacks.get('new', lambda: None),
                             accelerator="Strg+N")
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.callbacks.get('quit', lambda: None),
                             accelerator="Alt+F4")
        
        # Extras
        tools_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Extras", menu=tools_menu)
        tools_menu.add_command(label="Nach Updates suchen",
                              command=self.callbacks.get('check_updates', lambda: None))
        tools_menu.add_command(label="Repository öffnen",
                              command=self.callbacks.get('open_repo', lambda: None))
        tools_menu.add_separator()
        tools_menu.add_command(label="Einstellungen",
                              command=self.callbacks.get('settings', lambda: None))
        
        # Hilfe
        help_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Hilfe", menu=help_menu)
        help_menu.add_command(label="Über", command=self.callbacks.get('about', lambda: None))
        help_menu.add_command(label="Hilfe", command=self.callbacks.get('help', lambda: None))
    
    
class SettingsDialog(tk.Toplevel):
    """Einstellungen-Dialog."""
    
    def __init__(self, parent, update_manager: UpdateManager, on_save: Callable):
        super().__init__(parent)
        self.update_manager = update_manager
        self.on_save = on_save
        
        self.title("Einstellungen")
        self.geometry("450x300")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        
        self._setup_ui()
        self._center_window()
    
    def _setup_ui(self):
        """Erstellt die UI."""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Einstellungen", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 20))
        
        # Auto-Update
        self.auto_update_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, 
                       text="Automatisch auf Updates prüfen beim Start",
                       variable=self.auto_update_var).pack(anchor=tk.W, pady=5)
        
        # Check-Intervall
        interval_frame = ttk.Frame(main_frame)
        interval_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(interval_frame, text="Prüfintervall (Tage):").pack(side=tk.LEFT)
        self.interval_var = tk.IntVar(value=self.update_manager.check_interval_days)
        ttk.Spinbox(interval_frame, from_=1, to=30, textvariable=self.interval_var,
                   width=5).pack(side=tk.LEFT, padx=10)
        
        # Repository URL
        ttk.Label(main_frame, text="Repository URL:").pack(anchor=tk.W, pady=(15, 0))
        self.repo_var = tk.StringVar(value=self.update_manager.repo_url)
        ttk.Entry(main_frame, textvariable=self.repo_var, width=50).pack(
            fill=tk.X, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Abbrechen", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Speichern", command=self._save).pack(side=tk.RIGHT)
    
    def _save(self):
        """Speichert Einstellungen."""
        self.update_manager.check_interval_days = self.interval_var.get()
        self.update_manager.repo_url = self.repo_var.get()
        self.on_save()
        self.destroy()
    
    def _center_window(self):
        """Zentriert das Fenster über dem Parent."""
        self.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() - self.winfo_width()) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    
class AboutDialog(tk.Toplevel):
    """Über-Dialog."""
    
    def __init__(self, parent, version: str):
        super().__init__(parent)
        self.title("Über GaubenMaster")
        self.geometry("400x350")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        
        self._setup_ui(version)
        self._center_window()
    
    def _setup_ui(self, version: str):
        """Erstellt die UI."""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon/Title
        ttk.Label(main_frame, text="📐", font=('Arial', 48)).pack(pady=(0, 10))
        ttk.Label(main_frame, text="GaubenMaster", 
                 font=('Arial', 16, 'bold')).pack()
        ttk.Label(main_frame, text=f"Version {version}", 
                 font=('Arial', 10), foreground='gray').pack(pady=(0, 20))
        
        # Beschreibung
        desc = ("Eine Anwendung zur Berechnung und Visualisierung\n"
                "von Dreiecken für den Gaubenbau basierend auf drei Seitenlängen.\n\n"
                "Features:\n"
                "• Berechnung aller Winkel, Fläche, Umfang, Höhen\n"
                "• Interaktive grafische Darstellung\n"
                "• Maus-Drehung und Zoom\n"
                "• Silent Auto-Update via GitHub Releases")
        ttk.Label(main_frame, text=desc, justify=tk.CENTER).pack(pady=10)
        
        # Tech Stack
        tech = "Basierend auf: Python, Tkinter, Matplotlib, NumPy"
        ttk.Label(main_frame, text=tech, font=('Arial', 8), 
                 foreground='gray').pack(pady=10)
        
        ttk.Button(main_frame, text="OK", command=self.destroy).pack(pady=20)
    
    def _center_window(self):
        self.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() - self.winfo_width()) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    
class HelpDialog(tk.Toplevel):
    """Hilfe-Dialog."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Hilfe")
        self.geometry("550x550")
        self.transient(parent)
        
        self._setup_ui()
        self._center_window()
    
    def _setup_ui(self):
        """Erstellt die UI mit scrollbarem Text."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Text Widget mit Scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, padx=10, pady=10,
                                  font=('Consolas', 9))
        self.text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL,
                                 command=self.text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text_widget.config(yscrollcommand=scrollbar.set)
        
        # Hilfe-Text
        help_text = self._get_help_text()
        self.text_widget.insert(tk.END, help_text)
        self.text_widget.config(state=tk.DISABLED)
        
        # Close Button
        ttk.Button(main_frame, text="Schließen", command=self.destroy).grid(
            row=1, column=0, pady=10)
    
    def _get_help_text(self) -> str:
            """Gibt den Hilfe-Text zurück."""
            lines = [
                "GaubenMaster - Hilfe",
                "",
                "═══════════════════════════════════════════════════════════",
                "EINGABE",
                "═══════════════════════════════════════════════════════════",
                "• Geben Sie die drei Seitenlängen a, b, c in Zentimetern ein",
                "• Drücken Sie Enter oder klicken Sie auf \"Berechnen\"",
                "• Das Programm prüft automatisch die Dreiecksungleichung",
                "",
                "DREIECKSUNGLEICHUNG (muss erfüllt sein):",
                "  a + b > c",
                "  a + c > b",
                "  b + c > a",
                "",
                "Bei ungültigen Werten erscheint eine Fehlermeldung.",
                "",
                "═══════════════════════════════════════════════════════════",
                "BERECHNETE WERTE",
                "═══════════════════════════════════════════════════════════",
                "• Winkel α, β, γ (in Grad) - via Kosinussatz",
                "• Fläche (in cm²) - via Heronscher Formel",
                "• Umfang (in cm)",
                "• Höhen ha, hb, hc (in cm)",
                "• Inkreisradius & Umkreisradius",
                "",
                "═══════════════════════════════════════════════════════════",
                "VISUALISIERUNG BEDIENEN",
                "═══════════════════════════════════════════════════════════",
                "┌─────────────────────┬────────────────────────────────────┐",
                "│ Aktion              │ Wirkung                            │",
                "├─────────────────────┼────────────────────────────────────┤",
                "│ Linke Maustaste +   │ Dreieck drehen (Rotation)          │",
                "│ Ziehen              │                                    │",
                "│ Mausrad             │ Hinein/Herauszoomen                │",
                "│ \"Ansicht            │ Setzt Rotation und Zoom zurück     │",
                "│  zurücksetzen\"      │                                    │",
                "└─────────────────────┴────────────────────────────────────┘",
                "",
                "═══════════════════════════════════════════════════════════",
                "SILENT UPDATE-FUNKTION",
                "═══════════════════════════════════════════════════════════",
                "• Automatische Prüfung beim Start (einstellbar)",
                "• Update gefunden → Benachrichtigung unten rechts",
                "• \"Jetzt installieren\" → Silent Install + Auto-Restart",
                "• Manuelle Prüfung: Extras → Nach Updates suchen",
                "• Repository öffnen: Extras → Repository öffnen",
                "• Einstellungen: Extras → Einstellungen",
                "",
                "═══════════════════════════════════════════════════════════",
                "TASTATURKÜRZEL",
                "═══════════════════════════════════════════════════════════",
                "• Strg+N    : Neue Berechnung (Zurücksetzen)",
                "• Enter     : Berechnen (wenn Eingabefeld fokussiert)",
                "• Alt+F4    : Beenden",
                "",
                "═══════════════════════════════════════════════════════════",
                "MATHEMATISCHE GRUNDLAGEN",
                "═══════════════════════════════════════════════════════════",
                "Kosinussatz (Winkel):",
                "  cos(α) = (b² + c² - a²) / (2bc)",
                "  cos(β) = (a² + c² - b²) / (2ac)",
                "  cos(γ) = (a² + b² - c²) / (2ab)",
                "",
                "Heronsche Formel (Fläche):",
                "  s = (a + b + c) / 2",
                "  A = √(s(s-a)(s-b)(s-c))",
                "",
                "Höhen:",
                "  ha = 2A / a",
                "  hb = 2A / b",
                "  hc = 2A / c",
                "",
                "Inkreis- & Umkreisradius:",
                "  r = A / s",
                "  R = (a * b * c) / (4A)",
                "",
                "═══════════════════════════════════════════════════════════",
                "BEISPIELE",
                "══════════════════════════════════════════════════════════",
                "• 3-4-5 Dreieck: a=3, b=4, c=5 (Rechtwinklig, γ=90°)",
                "• Gleichseitig: a=5, b=5, c=5 (Alle Winkel 60°)",
                "• Gleichschenklig: a=5, b=5, c=8",
                "• 5-12-13: a=5, b=12, c=13 (Rechtwinklig)",
            ]
            return "\n".join(lines)
    
    def _center_window(self):
        self.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() - self.winfo_width()) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    
class UpdateDialog(tk.Toplevel):
    """Update-Benachrichtigungs-Dialog."""
    
    def __init__(self, parent, version_info: VersionInfo, on_update: Callable):
        super().__init__(parent)
        self.version_info = version_info
        self.on_update = on_update
        
        self.title("Update verfügbar")
        self.geometry("450x350")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        
        self._setup_ui()
        self._center_window()
    
    def _setup_ui(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon
        ttk.Label(main_frame, text="🔔", font=('Arial', 36)).pack(pady=(0, 10))
        
        ttk.Label(main_frame, text="Update verfügbar!", 
                 font=('Arial', 14, 'bold')).pack()
        
        ttk.Label(main_frame, 
                 text=f"Version {self.version_info.version} ist verfügbar\n"
                      f"(Veröffentlicht: {self.version_info.release_date})",
                 justify=tk.CENTER).pack(pady=10)
        
        # Changelog
        ttk.Label(main_frame, text="Änderungen:", font=('Arial', 10, 'bold')).pack(
            anchor=tk.W, pady=(15, 5))
        
        changelog_frame = ttk.Frame(main_frame)
        changelog_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        changelog_text = tk.Text(changelog_frame, wrap=tk.WORD, height=6, 
                                font=('Consolas', 9), padx=10, pady=10)
        changelog_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        changelog_text.insert(tk.END, self.version_info.changelog)
        changelog_text.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(changelog_frame, orient=tk.VERTICAL,
                                 command=changelog_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        changelog_text.config(yscrollcommand=scrollbar.set)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(btn_frame, text="Später", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Jetzt aktualisieren", 
                  command=self._do_update, style='Accent.TButton').pack(side=tk.RIGHT)
    
    def _do_update(self):
        """Führt Update durch."""
        self.on_update(self.version_info)
        self.destroy()
    
    def _center_window(self):
        self.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() - self.winfo_width()) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")