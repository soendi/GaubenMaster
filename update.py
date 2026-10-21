"""
Update-Management-Modul
=======================

Verwaltet automatische Updates der Anwendung.
"""

import json
import os
import threading
import webbrowser
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class VersionInfo:
    """Informationen über eine Version."""

    version: str
    release_date: str
    changelog: str
    download_url: str = ""
    size_mb: float = 0.0


class UpdateManager:
    """Verwaltet automatische Updates der Anwendung."""

    def __init__(
        self,
        repo_url: str = "https://github.com/soendi/GaubenMaster",
        current_version: str = "1.2.7",
        version_file: str = "version.json",
        check_interval_days: int = 7,
    ):
        """
        Initialisiert den UpdateManager.

        Args:
            repo_url: URL des GitHub-Repositories
            current_version: Aktuelle Version der Anwendung
            version_file: Pfad zur Versionsdatei
            check_interval_days: Intervall für automatische Checks in Tagen
        """
        self.repo_url = repo_url.rstrip("/")
        self.current_version = current_version
        self.version_file = version_file
        self.check_interval_days = check_interval_days
        self.last_check_file = "last_update_check.json"

        # GitHub API URL für Releases
        self.api_url = self._convert_to_api_url(repo_url)

        self.load_version()
        self.load_last_check()

    def _convert_to_api_url(self, repo_url: str) -> str:
        """Konvertiert GitHub Repo URL zu API URL."""
        # https://github.com/user/repo -> https://api.github.com/repos/user/repo
        if "github.com" in repo_url:
            parts = repo_url.replace("https://github.com/", "").split("/")
            if len(parts) >= 2:
                return f"https://api.github.com/repos/{parts[0]}/{parts[1]}"
        return ""

    def load_version(self):
        """Lädt die aktuelle Version aus der Datei."""
        if os.path.exists(self.version_file):
            try:
                with open(self.version_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.current_version = data.get("version", self.current_version)
            except (json.JSONDecodeError, IOError):
                pass

    def save_version(self, version: str):
        """Speichert die Version in die Datei."""
        try:
            with open(self.version_file, "w", encoding="utf-8") as f:
                json.dump(
                    {"version": version, "updated_at": datetime.now().isoformat()},
                    f,
                    indent=2,
                )
            self.current_version = version
        except IOError as e:
            print(f"Fehler beim Speichern der Version: {e}")

    def load_last_check(self):
        """Lädt den Zeitpunkt des letzten Update-Checks."""
        self.last_check = None
        if os.path.exists(self.last_check_file):
            try:
                with open(self.last_check_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    last_check_str = data.get("last_check")
                    if last_check_str:
                        self.last_check = datetime.fromisoformat(last_check_str)
            except (json.JSONDecodeError, IOError, ValueError):
                pass

    def save_last_check(self):
        """Speichert den Zeitpunkt des letzten Update-Checks."""
        try:
            with open(self.last_check_file, "w", encoding="utf-8") as f:
                json.dump({"last_check": datetime.now().isoformat()}, f, indent=2)
            self.last_check = datetime.now()
        except IOError as e:
            print(f"Fehler beim Speichern des letzten Checks: {e}")

    def should_check_for_updates(self) -> bool:
        """Prüft, ob ein Update-Check fällig ist."""
        if self.last_check is None:
            return True
        next_check = self.last_check + timedelta(days=self.check_interval_days)
        return datetime.now() >= next_check

    def check_for_updates(
        self,
        callback: Optional[Callable[[Optional[VersionInfo]], None]] = None,
        force: bool = False,
    ) -> Optional[VersionInfo]:
        """
        Prüft auf verfügbare Updates.

        Args:
            callback: Callback-Funktion mit VersionInfo oder None
            force: Erzwingt Check auch wenn Intervall nicht abgelaufen

        Returns:
            VersionInfo wenn Update verfügbar, sonst None
        """
        if not force and not self.should_check_for_updates():
            if callback:
                callback(None)
            return None

        def _check():
            try:
                update_info = self._fetch_latest_release()
                self.save_last_check()
                if callback:
                    callback(update_info)
                return update_info
            except Exception as e:
                print(f"Update-Check fehlgeschlagen: {e}")
                if callback:
                    callback(None)
                return None

        # In separatem Thread ausführen um GUI nicht zu blockieren
        thread = threading.Thread(target=_check, daemon=True)
        thread.start()
        return None  # Asynchron, Ergebnis kommt über Callback

    def _fetch_latest_release(self) -> Optional[VersionInfo]:
        """
        Holt das neueste Release von GitHub API.

        Returns:
            VersionInfo oder None
        """
        if not self.api_url:
            return None

        url = f"{self.api_url}/releases/latest"

        try:
            req = urllib.request.Request(url)
            req.add_header("Accept", "application/vnd.github.v3+json")
            req.add_header("User-Agent", "GaubenMaster-UpdateChecker")

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))

            latest_version = data.get("tag_name", "").lstrip("v")
            if not latest_version:
                latest_version = data.get("name", "").lstrip("v")

            if not latest_version:
                return None

            # Version vergleichen
            if self._compare_versions(latest_version, self.current_version) <= 0:
                return None  # Keine neuere Version

            # Release Info extrahieren
            published_at = data.get("published_at", "")
            if published_at:
                release_date = published_at[:10]  # YYYY-MM-DD
            else:
                release_date = datetime.now().strftime("%Y-%m-%d")

            changelog = data.get("body", "Keine Änderungsnotizen verfügbar.")
            if len(changelog) > 500:
                changelog = changelog[:500] + "..."

            # Download URL (erste Asset-Datei)
            download_url = ""
            assets = data.get("assets", [])
            if assets:
                download_url = assets[0].get("browser_download_url", "")

            return VersionInfo(
                version=latest_version,
                release_date=release_date,
                changelog=changelog,
                download_url=download_url,
            )

        except urllib.error.HTTPError as e:
            if e.code == 404:
                # Keine Releases vorhanden
                return None
            print(f"GitHub API Fehler: {e.code} - {e.reason}")
            return None
        except urllib.error.URLError as e:
            print(f"Netzwerkfehler beim Update-Check: {e}")
            return None
        except Exception as e:
            print(f"Unerwarteter Fehler beim Update-Check: {e}")
            return None

    def _compare_versions(self, v1: str, v2: str) -> int:
        """
        Vergleicht zwei Versionen (Semantic Versioning).

        Returns:
            1 wenn v1 > v2, -1 wenn v1 < v2, 0 wenn gleich
        """

        def parse_version(v: str):
            # Entferne 'v' Präfix und teile in Teile
            v = v.lstrip("v")
            parts = []
            for part in v.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # Non-numeric parts (z.B. '1.0.0-beta')
                    parts.append(part)
            return parts

        parts1 = parse_version(v1)
        parts2 = parse_version(v2)

        # Vergleiche Teil für Teil
        for p1, p2 in zip(parts1, parts2):
            if p1 != p2:
                if isinstance(p1, int) and isinstance(p2, int):
                    return 1 if p1 > p2 else -1
                else:
                    return 1 if str(p1) > str(p2) else -1

        # Wenn alle gemeinsamen Teile gleich, längere Version ist "größer"
        if len(parts1) != len(parts2):
            return 1 if len(parts1) > len(parts2) else -1

        return 0

    def apply_update(self, version_info: VersionInfo) -> bool:
        """
        Wendet ein Update an.

        Hinweis: In einer echten Anwendung würde hier der eigentliche
        Update-Prozess implementiert (Download, Entpacken, Ersetzen).

        Args:
            version_info: Informationen über das Update

        Returns:
            True bei Erfolg
        """
        try:
            # Hier würde der eigentliche Update-Prozess stattfinden:
            # 1. Download der neuen Version
            # 2. Backup der aktuellen Version
            # 3. Entpacken und Ersetzen der Dateien
            # 4. Dependencies aktualisieren
            # 5. Neustart der Anwendung

            print(f"Update auf Version {version_info.version} wird angewendet...")

            # Für Demo: Nur Version speichern
            self.save_version(version_info.version)

            return True
        except Exception as e:
            print(f"Update fehlgeschlagen: {e}")
            return False

    def open_repository(self):
        """Öffnet das Repository im Standardbrowser."""
        webbrowser.open(self.repo_url)

    def open_releases_page(self):
        """Öffnet die Releases-Seite im Browser."""
        webbrowser.open(f"{self.repo_url}/releases")

    def get_update_status(self) -> Dict[str, Any]:
        """Gibt Status-Informationen für die UI zurück."""
        return {
            "current_version": self.current_version,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "check_interval_days": self.check_interval_days,
            "repo_url": self.repo_url,
            "update_available": False,  # Wird durch Check aktualisiert
        }


class MockUpdateManager(UpdateManager):
    """Mock UpdateManager für Tests und Entwicklung."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mock_update_available = False
        self.mock_version_info = None

    def set_mock_update(self, available: bool, version: str = "2.0.0"):
        """Setzt Mock-Update für Tests."""
        self.mock_update_available = available
        if available:
            self.mock_version_info = VersionInfo(
                version=version,
                release_date=datetime.now().strftime("%Y-%m-%d"),
                changelog="Mock Update für Testzwecke",
                download_url="",
            )

    def _fetch_latest_release(self) -> Optional[VersionInfo]:
        if self.mock_update_available:
            return self.mock_version_info
        return None


def check_updates_background(
    update_manager: UpdateManager,
    on_update_found: Callable[[VersionInfo], None],
    on_no_update: Callable[[], None],
    on_error: Callable[[str], None],
):
    """
    Führt Update-Check im Hintergrund durch.

    Args:
        update_manager: UpdateManager Instanz
        on_update_found: Callback bei verfügbarem Update
        on_no_update: Callback bei keinem Update
        on_error: Callback bei Fehler
    """

    def _run():
        try:
            result = update_manager._fetch_latest_release()
            if result:
                on_update_found(result)
            else:
                on_no_update()
        except Exception as e:
            on_error(str(e))

    threading.Thread(target=_run, daemon=True).start()


# Convenience-Funktion
def create_update_manager(
    repo_url: str = None, current_version: str = None
) -> UpdateManager:
    """Factory-Funktion für UpdateManager."""
    return UpdateManager(
        repo_url=repo_url or "https://github.com/soendi/GaubenMaster",
        current_version=current_version or "1.0.0",
    )
