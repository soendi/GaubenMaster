#!/usr/bin/env python3
"""
GaubenMaster - Hauptanwendung
=============================

Eine Anwendung zur Berechnung und Visualisierung von Dreiecken
für den Gaubenbau basierend auf drei Seitenlängen (A, B, C).

Features:
- Eingabe von drei Seitenlängen
- Grafische Darstellung mit Maßen (Längen, Winkel)
- Maus-Drehung des Dreiecks
- Silent Auto-Update via GitHub Releases
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import os
import sys
import subprocess
import tempfile
import shutil
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

# Lokale Imports
from GaubenMaster import TriangleCalculator, TrianglePlot, UpdateManager
from GaubenMaster.gui import (InputPanel, VisualizationPanel, StatusBar, 
                               MenuBar, SettingsDialog, AboutDialog, 
                               HelpDialog, UpdateDialog)
from GaubenMaster.update import VersionInfo


class GaubenMasterApp:
    """Hauptanwendungs-Klasse für GaubenMaster."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("GaubenMaster - Dreiecksberechnung für Gaubenbau")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # App-Info
        self.app_name = "GaubenMaster"
        self.github_repo = "soendi/GaubenMaster"
        self.github_api_url = f"https://api.github.com/repos/{self.github_repo}"
        
        # Version laden
        self.version = self._load_version()
        
        # Update Manager
        self.update_manager = UpdateManager(
            repo_url=f"https://github.com/{self.github_repo}",
            current_version=self.version
        )
        
        # Silent Update Flag
        self.silent_update_pending = False
        self.update_info: Optional[VersionInfo] = None
        
        # State
        self.plot_state = {}
        
        # GUI aufbauen
        self._setup_style()
        self._setup_ui()
        self._setup_bindings()
        
        # Initial berechnen
        self.calculate_and_draw()
        
        # Silent Update-Check beim Start (verzögert)
        self.root.after(2000, self._delayed_silent_update_check)
    
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
    
    def _delayed_silent_update_check(self):
        """Verzögerter Silent Update-Check beim Start."""
        # Nur prüfen, nicht anzeigen
        self.update_manager.check_for_updates(callback=self._handle_silent_update_result)
    
    def _handle_silent_update_result(self, version_info: Optional[VersionInfo]):
        """Behandelt das Ergebnis des Silent Update-Checks."""
        self.root.after(0, lambda: self._process_silent_update(version_info))
    
    def _process_silent_update(self, version_info: Optional[VersionInfo]):
        """Verarbeitet Silent Update - zeigt nur Benachrichtigung."""
        if version_info:
            self.update_info = version_info
            self.status_bar.set_status(f"⚡ Update verfügbar: v{version_info.version}")
            # Benachrichtigung anzeigen (nicht modal)
            self._show_update_notification(version_info)
        else:
            self.status_bar.set_status("Kein Update verfügbar")
    
    def _show_update_notification(self, version_info: VersionInfo):
        """Zeigt eine nicht-modale Update-Benachrichtigung."""
        # Toast-Style Notification
        self.notification_frame = tk.Toplevel(self.root)
        self.notification_frame.title("")
        self.notification_frame.geometry("350x120")
        self.notification_frame.resizable(False, False)
        self.notification_frame.overrideredirect(True)
        self.notification_frame.attributes('-topmost', True)
        
        # Position: unten rechts
        self.root.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width() - 370
        y = self.root.winfo_y() + self.root.winfo_height() - 150
        self.notification_frame.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(self.notification_frame, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="🔔 Update verfügbar!", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W)
        ttk.Label(frame, 
                 text=f"Version {version_info.version} ist verfügbar\n"
                      f"(Veröffentlicht: {version_info.release_date})",
                 justify=tk.LEFT).pack(anchor=tk.W, pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Später", 
                  command=self._dismiss_notification).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Jetzt installieren", 
                  command=lambda: self._start_silent_update(version_info),
                  style='Accent.TButton').pack(side=tk.RIGHT)
        
        # Auto-close nach 30 Sekunden
        self.notification_frame.after(30000, self._dismiss_notification)
    
    def _dismiss_notification(self):
        """Schließt die Benachrichtigung."""
        if hasattr(self, 'notification_frame'):
            self.notification_frame.destroy()
    
    def _start_silent_update(self, version_info: VersionInfo):
        """Startet den Silent Update-Prozess."""
        self._dismiss_notification()
        self.status_bar.set_status(f"Lade Update v{version_info.version} herunter...")
        
        def download_and_install():
            try:
                success = self._download_and_run_installer(version_info)
                if success:
                    self.root.after(0, self._apply_silent_update)
                else:
                    self.root.after(0, lambda: self.status_bar.set_status("Update-Download fehlgeschlagen"))
            except Exception as e:
                self.root.after(0, lambda: self.status_bar.set_status(f"Update-Fehler: {e}"))
        
        threading.Thread(target=download_and_install, daemon=True).start()
    
    def _download_and_run_installer(self, version_info: VersionInfo) -> bool:
        """Lädt den Installer herunter und führt ihn silent aus."""
        try:
            # GitHub Release Asset URL für Windows Installer
            # Erwarte: GaubenMaster-Setup-{version}.exe
            asset_name = f"GaubenMaster-Setup-{version_info.version}.exe"
            download_url = f"https://github.com/{self.github_repo}/releases/download/v{version_info.version}/{asset_name}"
            
            # In Temp-Verzeichnis herunterladen
            temp_dir = tempfile.gettempdir()
            installer_path = os.path.join(temp_dir, asset_name)
            
            self.root.after(0, lambda: self.status_bar.set_status(f"Lade {asset_name}..."))
            
            urllib.request.urlretrieve(download_url, installer_path)
            
            self.root.after(0, lambda: self.status_bar.set_status("Installiere Update..."))
            
            # Silent Install: /SILENT /SUPPRESSMSGBOXES /NORESTART /CLOSEAPPLICATIONS
            # Wartet bis Installation fertig ist
            result = subprocess.run([
                installer_path,
                "/SILENT",
                "/SUPPRESSMSGBOXES",
                "/NORESTART",
                "/CLOSEAPPLICATIONS",
                "/RESTARTAPPLICATIONS"
            ], capture_output=True, timeout=120)
            
            # Cleanup
            try:
                os.remove(installer_path)
            except:
                pass
            
            return result.returncode == 0
            
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # Fallback: Versuche generischen Asset-Namen
                return self._try_fallback_download(version_info)
            return False
        except Exception as e:
            print(f"Download/Install Fehler: {e}")
            return False
    
    def _try_fallback_download(self, version_info: VersionInfo) -> bool:
        """Fallback: Versuche andere Asset-Namen."""
        fallback_names = [
            f"GaubenMaster-{version_info.version}-windows.exe",
            f"GaubenMaster-Setup-{version_info.version}.exe",
            f"gaubenmaster-{version_info.version}-win64.exe"
        ]
        
        for asset_name in fallback_names:
            try:
                download_url = f"https://github.com/{self.github_repo}/releases/download/v{version_info.version}/{asset_name}"
                temp_dir = tempfile.gettempdir()
                installer_path = os.path.join(temp_dir, asset_name)
                
                urllib.request.urlretrieve(download_url, installer_path)
                
                result = subprocess.run([
                    installer_path,
                    "/SILENT", "/SUPPRESSMSGBOXES", "/NORESTART",
                    "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS"
                ], capture_output=True, timeout=120)
                
                try:
                    os.remove(installer_path)
                except:
                    pass
                
                if result.returncode == 0:
                    return True
            except:
                continue
        
        return False
    
    def _apply_silent_update(self):
        """Wendet das Update an - startet die App neu."""
        self.status_bar.set_status("Update installiert - starte neu...")
        
        # Version aktualisieren
        if self.update_info:
            self.update_manager.save_version(self.update_info.version)
            self.version = self.update_info.version
            self.input_panel.update_version_label()
        
        # App neu starten
        self.root.after(500, self._restart_application)
    
    def _restart_application(self):
        """Startet die Anwendung neu."""
        python = sys.executable
        script = os.path.abspath(__file__)
        os.execl(python, python, script)
    
    def calculate_and_draw(self):
        """Führt die Berechnung durch und aktualisiert die Anzeige."""
        try:
            a, b, c = self.input_panel.get_values()
            
            if a <= 0 or b <= 0 or c <= 0:
                messagebox.showerror("Fehler", "Alle Seitenlängen müssen positiv sein!")
                return
            
            # Alle Eigenschaften berechnen
            from GaubenMaster.calculator import get_triangle_properties
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
        """Manueller Update-Check mit Dialog."""
        self.status_bar.set_status("Prüfe auf Updates...")
        self.root.update_idletasks()
        
        self.update_manager.check_for_updates(callback=self._handle_update_result, force=True)
    
    def _handle_update_result(self, version_info: Optional[VersionInfo]):
        """Behandelt das Ergebnis des manuellen Update-Checks."""
        self.root.after(0, lambda: self._show_update_result(version_info))
    
    def _show_update_result(self, version_info: Optional[VersionInfo]):
        """Zeigt Update-Ergebnis an."""
        if version_info:
            self.update_info = version_info
            dialog = UpdateDialog(self.root, version_info, self._start_silent_update)
        else:
            messagebox.showinfo("Kein Update", "Sie verwenden bereits die neueste Version.")
            self.status_bar.set_status("Kein Update verfügbar")
    
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
    app = GaubenMasterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()