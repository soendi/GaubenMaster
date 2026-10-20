#!/usr/bin/env python3
"""
Triangle Calculator - Hauptanwendung
====================================

Eine Anwendung zur Berechnung und Visualisierung von Dreiecken
basierend auf drei Seitenlängen (A, B, C).

Features:
- Eingabe von drei Seitenlängen
- Grafische Darstellung mit Maßen (Längen, Winkel)
- Maus-Drehung des Dreiecks
- Automatische Update-Funktion
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import os
import sys

# Lokale Imports
from TriangleCalculator import TriangleCalculator, TrianglePlot, UpdateManager
from TriangleCalculator.gui import (InputPanel, VisualizationPanel, StatusBar, 
                                     MenuBar, SettingsDialog, AboutDialog, 
                                     HelpDialog, UpdateDialog)


class TriangleApp:
    """Hauptanwendungs-Klasse."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Triangle Calculator - Dreiecksberechnung")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Version laden
        self.version = self._load_version()
        
        # Update Manager
        self.update_manager = UpdateManager(current_version=self.version)
        
        # State
        self.plot_state = {}
        
        # GUI aufbauen
        self._setup_style()
        self._setup_ui()
        self._setup_bindings()
        
        # Initial berechnen
        self.calculate_and_draw()
        
        # Update-Check beim Start (verzögert)
        self.root.after(2000, self._delayed_update_check)
    
    def _load_version(self) -> str:
        """Lädt Version aus version.json."""
        try:
            with open('version.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('version', '1.0.0')
        except:
            return '1.0.0'
    
    def _setup_style(self):
        """Konfiguriert TTK Styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Accent Button Style
        style.configure('Accent.TButton', 
                       font=('Arial', 10, 'bold'),
                       foreground='white',
                       background='#0078d4')
        style.map('Accent.TButton',
                 background=[('active', '#106ebe'), ('pressed', '#005a9e')])
    
    def _setup_ui(self):
        """Erstellt die Benutzeroberfläche."""
        # Hauptcontainer
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid-Konfiguration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Callbacks für Panels
        callbacks = {
            'new': self.reset_values,
            'quit': self.root.quit,
            'check_updates': self.manual_update_check,
            'open_repo': self.update_manager.open_repository,
            'settings': self.show_settings,
            'about': self.show_about,
            'help': self.show_help,
        }
        
        # Menüleiste
        menubar = MenuBar(self.root, callbacks)
        self.root.config(menu=menubar)
        
        # Linke Seite: Eingabepanel
        self.input_panel = InputPanel(
            main_frame,
            on_calculate=self.calculate_and_draw,
            on_reset=self.reset_values,
            on_update_check=self.manual_update_check,
            update_manager=self.update_manager
        )
        self.input_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Rechte Seite: Visualisierung
        self.viz_panel = VisualizationPanel(main_frame)
        self.viz_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Statusleiste
        self.status_bar = StatusBar(main_frame)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def _setup_bindings(self):
        """Richtet Tastenkürzel ein."""
        self.root.bind('<Control-n>', lambda e: self.reset_values())
        self.root.bind('<F5>', lambda e: self.calculate_and_draw())
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _delayed_update_check(self):
        """Verzögerter Update-Check beim Start."""
        if self.update_manager.should_check_for_updates():
            self.update_manager.check_for_updates(callback=self._handle_update_result)
    
    def calculate_and_draw(self):
        """Führt die Berechnung durch und aktualisiert die Anzeige."""
        try:
            a, b, c = self.input_panel.get_values()
            
            if a <= 0 or b <= 0 or c <= 0:
                messagebox.showerror("Fehler", "Alle Seitenlängen müssen positiv sein!")
                return
            
            # Alle Eigenschaften berechnen
            props = get_triangle_properties(a, b, c)
            
            # Input Panel aktualisieren
            self.input_panel.update_results(props)
            
            # Visualisierung aktualisieren
            self.viz_panel.set_triangle(a, b, c)
            
            # Status
            if props.get("valid", False):
                angles = props["angles"]
                self.status_bar.set_status(
                    f"Berechnet: a={a:.1f}, b={b:.1f}, c={c:.1f} | "
                    f"α={angles['alpha']:.1f}°, β={angles['beta']:.1f}°, γ={angles['gamma']:.1f}°"
                )
            else:
                self.status_bar.set_status("Ungültiges Dreieck")
            
        except tk.TclError:
            messagebox.showerror("Fehler", "Bitte gültige Zahlen eingeben!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Berechnungsfehler: {str(e)}")
    
    def reset_values(self):
        """Setzt alle Werte auf Standardwerte zurück."""
        self.input_panel.set_values(3.0, 4.0, 5.0)
        self.viz_panel.reset_view()
        self.plot_state = {}
        self.calculate_and_draw()
        self.status_bar.set_status("Zurückgesetzt auf Standardwerte (3-4-5 Dreieck)")
    
    def manual_update_check(self):
        """Manueller Update-Check."""
        self.status_bar.set_status("Prüfe auf Updates...")
        self.root.update_idletasks()
        
        self.update_manager.check_for_updates(callback=self._handle_update_result, force=True)
    
    def _handle_update_result(self, version_info: VersionInfo):
        """Behandelt das Ergebnis des Update-Checks."""
        # Zurück in Main Thread
        self.root.after(0, lambda: self._show_update_result(version_info))
    
    def _show_update_result(self, version_info: Optional[VersionInfo]):
        """Zeigt Update-Ergebnis an."""
        if version_info:
            # Update-Dialog anzeigen
            dialog = UpdateDialog(self.root, version_info, self._apply_update)
        else:
            messagebox.showinfo("Kein Update", "Sie verwenden bereits die neueste Version.")
            self.status_bar.set_status("Kein Update verfügbar")
    
    def _apply_update(self, version_info: VersionInfo):
        """Wendet Update an."""
        if self.update_manager.apply_update(version_info):
            self.input_panel.update_version_label()
            messagebox.showinfo("Erfolg", 
                f"Update auf Version {version_info.version} erfolgreich!\n"
                "Bitte starten Sie die Anwendung neu.")
            self.status_bar.set_status(f"Update auf {version_info.version} installiert")
        else:
            messagebox.showerror("Fehler", "Update fehlgeschlagen!")
            self.status_bar.set_status("Update fehlgeschlagen")
    
    def show_settings(self):
        """Zeigt Einstellungen-Dialog."""
        def on_save():
            self.input_panel.update_version_label()
        
        SettingsDialog(self.root, self.update_manager, on_save)
    
    def show_about(self):
        """Zeigt Über-Dialog."""
        AboutDialog(self.root, self.version)
    
    def show_help(self):
        """Zeigt Hilfe-Dialog."""
        HelpDialog(self.root)
    
    def _on_closing(self):
        """Wird beim Schließen des Fensters aufgerufen."""
        # Plot-State speichern
        self.plot_state = self.viz_panel.get_plot_state()
        self.root.destroy()


def main():
    """Haupteinstiegspunkt."""
    # High DPI Support für Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    root = tk.Tk()
    app = TriangleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()