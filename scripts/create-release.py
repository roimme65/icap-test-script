#!/usr/bin/env python3
"""
ICAP Test Script - Automatische Release-Erstellung
Erstellt neue Releases, aktualisiert Versionsnummern und verwaltet GitHub Integration
"""

import os
import sys
import re
import argparse
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Optional

# Farben
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(msg: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{msg}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_info(msg: str):
    print(f"{Colors.OKBLUE}[INFO]{Colors.ENDC} {msg}")

def print_success(msg: str):
    print(f"{Colors.OKGREEN}[SUCCESS]{Colors.ENDC} {msg}")

def print_warning(msg: str):
    print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} {msg}")

def print_error(msg: str):
    print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {msg}")

class VersionManager:
    """Verwaltet Versionsnummern im Projekt"""
    
    VERSION_PATTERNS = [
        # icap_test.py - __version__
        {
            'file': 'icap_test.py',
            'pattern': r'(__version__ = ")(\d+\.\d+\.\d+)(")',
            'replacement': r'\g<1>{version}\g<3>'
        },
        # icap_server.py - __version__
        {
            'file': 'icap_server.py',
            'pattern': r'(__version__ = ")(\d+\.\d+\.\d+)(")',
            'replacement': r'\g<1>{version}\g<3>'
        },
        # VERSION file
        {
            'file': 'VERSION',
            'pattern': r'(\d+\.\d+\.\d+)',
            'replacement': '{version}'
        },
        # README.md - Version Badge
        {
            'file': 'README.md',
            'pattern': r'(!\[Version\]\(https://img\.shields\.io/badge/version-)(\d+\.\d+\.\d+)(-blue\.svg\)\(VERSION\))',
            'replacement': r'\g<1>{version}\g<3>'
        },
        # README.de.md - Version Badge
        {
            'file': 'README.de.md',
            'pattern': r'(!\[Version\]\(https://img\.shields\.io/badge/version-)(\d+\.\d+\.\d+)(-blue\.svg\)\(VERSION\))',
            'replacement': r'\g<1>{version}\g<3>'
        }
    ]
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.current_version = self.get_current_version()
        
    def get_current_version(self) -> str:
        """Extrahiert aktuelle Version aus VERSION-Datei"""
        version_file = self.project_root / 'VERSION'
        
        if not version_file.exists():
            print_error("VERSION-Datei nicht gefunden")
            sys.exit(1)
        
        with open(version_file, 'r') as f:
            version = f.read().strip()
        
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            print_error(f"Ungültige Versionsnummer in VERSION-Datei: {version}")
            sys.exit(1)
        
        return version
    
    def bump_version(self, bump_type: str) -> str:
        """Erhöht Versionsnummer"""
        major, minor, patch = map(int, self.current_version.split('.'))
        
        if bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        elif bump_type == 'patch':
            patch += 1
        else:
            raise ValueError(f"Unbekannter Bump-Typ: {bump_type}")
        
        return f"{major}.{minor}.{patch}"
    
    def update_all_versions(self, new_version: str):
        """Aktualisiert alle Versionsnummern im Projekt"""
        print_info(f"Aktualisiere Versionen zu v{new_version}...")
        
        for pattern_info in self.VERSION_PATTERNS:
            file_path = self.project_root / pattern_info['file']
            
            if not file_path.exists():
                print_warning(f"Datei nicht gefunden: {pattern_info['file']}")
                continue
            
            with open(file_path, 'r') as f:
                content = f.read()
            
            replacement = pattern_info['replacement'].replace('{version}', new_version)
            new_content = re.sub(pattern_info['pattern'], replacement, content)
            
            if new_content == content:
                print_warning(f"Keine Versionsmuster gefunden in: {pattern_info['file']}")
            else:
                with open(file_path, 'w') as f:
                    f.write(new_content)
                print_success(f"Aktualisiert: {pattern_info['file']}")
        
        self.current_version = new_version

class ReleaseManager:
    """Verwaltet Release-Prozesse"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.releases_dir = project_root / 'releases'
        
    def create_release_notes_template(self, version: str) -> str:
        """Erstellt Template für Release-Notizen"""
        date = datetime.now().strftime('%Y-%m-%d')
        
        template = f"""# Release v{version} - {date}

## 🎯 Übersicht
Beschreiben Sie die Hauptziele und Highlights dieser Version.

## ✨ Neue Features
- Feature 1: Beschreibung
- Feature 2: Beschreibung

## 🐛 Bug Fixes
- Bug 1: Beschreibung
- Bug 2: Beschreibung

## 🔧 Verbesserungen
- Verbesserung 1: Beschreibung
- Verbesserung 2: Beschreibung

## 📚 Dokumentation
- Dokumentations-Update 1
- Dokumentations-Update 2

## 🙏 Credits
Danke an alle Beitragenden dieser Version!

## 📥 Installation

### Mit Docker (empfohlen)
```bash
docker compose up -d --pull always
```

### Manuelle Installation
```bash
git clone https://github.com/roimme65/icap-test-script.git
cd icap-test-script
git checkout v{version}
```

## ⚠️ Breaking Changes
Keine Breaking Changes in dieser Version.

## 🔗 Links
- [Full Changelog](../CHANGELOG.md)
- [Source Code](https://github.com/roimme65/icap-test-script)
- [Report Issue](https://github.com/roimme65/icap-test-script/issues)
"""
        return template

    def create_release_file(self, version: str) -> Path:
        """Erstellt Release-Notes-Datei"""
        if not self.releases_dir.exists():
            self.releases_dir.mkdir(parents=True)
        
        release_file = self.releases_dir / f"v{version}.md"
        
        if release_file.exists():
            print_warning(f"Release-Notizen-Datei existiert bereits: {release_file}")
            return release_file
        
        template = self.create_release_notes_template(version)
        
        with open(release_file, 'w') as f:
            f.write(template)
        
        print_success(f"Release-Notizen erstellt: {release_file}")
        return release_file
    
    def validate_release_files(self, version: str) -> bool:
        """Validiert dass alle notwendigen Release-Dateien existieren"""
        print_info("Validiere Release-Dateien...")
        
        release_file = self.releases_dir / f"v{version}.md"
        if not release_file.exists():
            print_error(f"Release-Notizen fehlen: {release_file}")
            return False
        
        print_success("Release-Dateien validiert")
        return True

class GitManager:
    """Verwaltet Git-Operationen"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        
    def is_git_repo(self) -> bool:
        """Prüft ob Verzeichnis ein Git-Repository ist"""
        return (self.project_root / '.git').exists()
    
    def get_git_status(self) -> str:
        """Gibt Git-Status aus"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout
        except Exception as e:
            print_error(f"Git-Fehler: {e}")
            return ""
    
    def has_uncommitted_changes(self) -> bool:
        """Prüft ob unversionierte Änderungen existieren"""
        status = self.get_git_status()
        return bool(status.strip())
    
    def create_tag(self, version: str, message: str = "") -> bool:
        """Erstellt Git-Tag für Release"""
        tag_name = f"v{version}"
        
        try:
            if not message:
                message = f"Release {tag_name}"
            
            subprocess.run(
                ['git', 'tag', '-a', tag_name, '-m', message],
                cwd=self.project_root,
                check=True,
                capture_output=True
            )
            
            print_success(f"Git-Tag erstellt: {tag_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print_error(f"Git-Tag-Fehler: {e}")
            return False
    
    def push_tag(self, version: str) -> bool:
        """Push Git-Tag zu Remote"""
        tag_name = f"v{version}"
        
        try:
            subprocess.run(
                ['git', 'push', 'origin', tag_name],
                cwd=self.project_root,
                check=True,
                capture_output=True
            )
            
            print_success(f"Tag gepusht: {tag_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print_error(f"Git-Push-Fehler: {e}")
            return False
    
    def push_branch(self, branch: str = 'main') -> bool:
        """Push Branch zu Remote"""
        try:
            subprocess.run(
                ['git', 'push', 'origin', branch],
                cwd=self.project_root,
                check=True,
                capture_output=True
            )
            
            print_success(f"Branch gepusht: {branch}")
            return True
            
        except subprocess.CalledProcessError as e:
            print_error(f"Git-Push-Fehler beim Branch-Push: {e}")
            return False

class ReleaseBuilder:
    """Orchestriert den kompletten Release-Prozess"""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.version_manager = VersionManager(self.project_root)
        self.release_manager = ReleaseManager(self.project_root)
        self.git_manager = GitManager(self.project_root)
        
    def run(self, bump_type: str, skip_git: bool = False, skip_push: bool = False, auto: bool = False):
        """Führt den kompletten Release-Prozess durch"""
        print_header("🚀 ICAP Test Script Release Builder")
        
        if auto:
            print_info("🤖 Automatischer Modus aktiviert")
        
        # Validierungen
        if not self.git_manager.is_git_repo():
            print_error("Nicht in einem Git-Repository!")
            sys.exit(1)
        
        if self.git_manager.has_uncommitted_changes():
            print_warning("Unversionierte Änderungen vorhanden!")
            if not auto:
                response = input("Fortfahren? (j/n): ")
                if response.lower() != 'j':
                    print_info("Abgebrochen")
                    return
            else:
                print_info("⏭️  Ignoriere Warnung im automatischen Modus")
        
        # Versionsnummer aktualisieren
        print_info(f"Aktuelle Version: {self.version_manager.current_version}")
        new_version = self.version_manager.bump_version(bump_type)
        print_info(f"Neue Version: {new_version}")
        
        # Versions-Updates
        self.version_manager.update_all_versions(new_version)
        
        # Release-Notizen erstellen
        self.release_manager.create_release_file(new_version)
        
        # Validierung
        if not self.release_manager.validate_release_files(new_version):
            print_error("Release-Validierung fehlgeschlagen!")
            sys.exit(1)
        
        # Git-Operationen
        if not skip_git:
            print_info("Committen von Änderungen...")
            try:
                subprocess.run(
                    ['git', 'add', '-A'],
                    cwd=self.project_root,
                    check=True,
                    capture_output=True
                )
                
                subprocess.run(
                    ['git', 'commit', '-m', f"Release v{new_version}"],
                    cwd=self.project_root,
                    check=True,
                    capture_output=True
                )
                print_success("Änderungen committed")
            except subprocess.CalledProcessError as e:
                print_error(f"Git-Commit-Fehler: {e}")
                sys.exit(1)
            
            # Branch zu Remote pushen
            if not skip_push:
                print_info("Pushe main Branch...")
                if not self.git_manager.push_branch('main'):
                    print_error("Branch-Push fehlgeschlagen")
                    sys.exit(1)
            
            # Tag erstellen
            if self.git_manager.create_tag(new_version):
                # Tag zu Remote pushen
                if not skip_push:
                    print_info("Pushe Release-Tag...")
                    self.git_manager.push_tag(new_version)
        
        print_header("✅ Release erfolgreich erstellt!")
        print_info(f"Version: v{new_version}")
        print_info(f"Release-Notizen: releases/v{new_version}.md")
        print_info("\nNächste Schritte:")
        print_info("1. Release-Notizen unter releases/v{}.md überprüfen und anpassen".format(new_version))
        print_info("2. Bei Bedarf lokal testen: docker compose up -d")
        print_info("3. GitHub Actions wird automatisch eine Release erstellen")

def main():
    parser = argparse.ArgumentParser(
        description='ICAP Test Script Release Builder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
    ./scripts/create-release.py patch          # Version: 1.0.9 -> 1.0.10
    ./scripts/create-release.py minor          # Version: 1.0.9 -> 1.1.0
    ./scripts/create-release.py major          # Version: 1.0.9 -> 2.0.0
    ./scripts/create-release.py patch --auto   # Vollautomatisch
    ./scripts/create-release.py patch --no-git # Ohne Git-Operationen
        """
    )
    
    parser.add_argument(
        'bump_type',
        choices=['major', 'minor', 'patch'],
        help='Versionsnummern-Bump-Typ'
    )
    
    parser.add_argument(
        '--no-git',
        action='store_true',
        help='Keine Git-Operationen (nur lokale Versionsierung)'
    )
    
    parser.add_argument(
        '--no-push',
        action='store_true',
        help='Nicht zu Remote pushen'
    )
    
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Automatischer Modus - keine interaktiven Fragen, alles automatisch generieren'
    )
    
    parser.add_argument(
        '--project-root',
        type=Path,
        default=Path(__file__).parent.parent,
        help='Projektroot-Verzeichnis (Standard: übergeordnetes Verzeichnis von scripts/)'
    )
    
    args = parser.parse_args()
    
    # Release Builder ausführen
    builder = ReleaseBuilder(args.project_root)
    builder.run(
        bump_type=args.bump_type,
        skip_git=args.no_git,
        skip_push=args.no_push,
        auto=args.auto
    )

if __name__ == '__main__':
    main()
