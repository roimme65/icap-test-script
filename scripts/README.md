# Scripts - Release Management

Dieses Verzeichnis enthält Hilfs-Skripte für die Projektverwaltung.

## create-release.py

Automatisches Release-Management-Skript. Erstellt neue Releases, aktualisiert Versionsnummern automatisch und synchronisiert alle Projekt-Dateien.

### Funktionen

- 🔢 **Automatische Versionierung** - Smart Version Bumping (major/minor/patch)
- 📝 **Release-Notizen-Generator** - Template-basierte Erstellung
- 🔖 **Git-Integration** - Automatische Tagging und Commits
- 🚀 **GitHub-Ready** - Direkt kompatibel mit CI/CD-Workflows
- 📋 **Validierung** - Umfassenden Checks vor Release

### Verwendung

#### Basis-Befehle

```bash
# Patch Version (1.0.9 -> 1.0.10)
python3 scripts/create-release.py patch

# Minor Version (1.0.9 -> 1.1.0)
python3 scripts/create-release.py minor

# Major Version (1.0.9 -> 2.0.0)
python3 scripts/create-release.py major
```

#### Erweiterte Optionen

```bash
# Ohne Git-Operationen (nur lokal)
python3 scripts/create-release.py patch --no-git

# Ohne zu Remote pushen
python3 scripts/create-release.py patch --no-push

# Mit spezifischem Projektroot
python3 scripts/create-release.py patch --project-root /path/to/project
```

### Was macht das Skript?

1. **Versionierung**
   - Analysiert aktuelle Version aus `VERSION`-Datei
   - Berechnet neue Versionsnummer
   - Aktualisiert: `icap_test.py`, `icap_server.py`, `VERSION`

2. **Release-Notizen**
   - Erstellt Datei in `releases/v{version}.md`
   - Includes Template mit Sections für:
     - Features
     - Bug Fixes
     - Verbesserungen
     - Breaking Changes
   - Editierbar vor dem Finalisieren

3. **Git-Operationen**
   - Staged alle geänderten Dateien
   - Erstellt Commit: "Release v{version}"
   - Erstellt annotiertes Tag: `v{version}`
   - Pusht Tag zu Remote (falls `--no-push` nicht gesetzt)

4. **Validierung**
   - Prüft Git-Repository Status
   - Warnt vor unversionierten Änderungen
   - Validiert Release-Notizen existieren

### Beispiel-Workflow

```bash
# 1. Features entwickeln und committen
git add .
git commit -m "Add new ICAP server features"

# 2. Release vorbereiten (patch bump)
python3 scripts/create-release.py patch

# 3. Release-Notizen überprüfen und anpassen
editor releases/v1.0.10.md

# 4. In Release-Notizen committen und pushen
git add releases/v1.0.10.md
git commit -m "Update release notes for v1.0.10"
git push origin main

# 5. GitHub Actions erstellt automatisch ein Release auf GitHub
# (ausgelöst durch den v1.0.10 Tag)
```

### Fehlerbehandlung

| Fehler | Ursache | Lösung |
|--------|--------|--------|
| "Nicht in einem Git-Repository!" | Skript außerhalb Git-Repo ausgeführt | `cd` ins Projektroot-Verzeichnis |
| "VERSION-Datei nicht gefunden" | VERSION-Datei nicht im Root | Datei erstellen oder `--project-root` angeben |
| "Unversionierte Änderungen vorhanden!" | Arbeitsverzeichnis nicht sauber | `git add` und `git commit` oder `--no-git` nutzen |
| "Git-Tag-Fehler" | Tag existiert bereits | `git tag -d v{version}` und erneut versuchen |

### Voraussetzungen

- Python 3.6+
- Git installiert und verfügbar
- Git-Repository mit Remote (für `--no-push` nicht nötig)
- Schreibberechtigung für Projektdateien

