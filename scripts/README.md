# Scripts

Automatisierungs-Scripts für das ICAP Test Script Projekt.

## 📋 Verfügbare Scripts

### `create-release.sh`

Erstellt automatisch ein neues Release mit:
- Version Bump (major/minor/patch)
- Automatische Release-Notes aus Git-Commits
- CHANGELOG.md Update
- Git Tag und Push
- GitHub Release (mit gh CLI)

## 🚀 Verwendung

### Neues Patch-Release (1.0.0 → 1.0.1)

```bash
./scripts/create-release.sh patch
```

### Neues Minor-Release (1.0.0 → 1.1.0)

```bash
./scripts/create-release.sh minor
```

### Neues Major-Release (1.0.0 → 2.0.0)

```bash
./scripts/create-release.sh major
```

### Vollautomatischer Modus (ohne Editor)

```bash
./scripts/create-release.sh patch --auto
```

## 📝 Workflow

### Mit Editor (Standard)

1. Script ausführen: `./scripts/create-release.sh patch`
2. Neue Version wird berechnet
3. Release-Notes Template wird erstellt und im Editor geöffnet
4. Nach dem Speichern und Schließen: Script erneut ausführen
5. Release wird finalisiert und gepusht

### Vollautomatisch

1. Script mit `--auto` ausführen: `./scripts/create-release.sh patch --auto`
2. Release-Notes werden automatisch aus Git-Commits generiert
3. Alles wird automatisch committed, getaggt und gepusht

## 🔧 Voraussetzungen

### Erforderlich
- Git Repository
- Auf `main` Branch
- Sauberes Working Directory (keine uncommitted Änderungen)

### Optional
- [GitHub CLI (gh)](https://cli.github.com/) - für automatische GitHub Releases
  ```bash
  # Installation
  sudo apt install gh
  
  # Authentifizierung
  gh auth login
  ```

## 📦 Dateien

Nach dem Release werden folgende Dateien erstellt/aktualisiert:

- `VERSION` - Aktuelle Versionsnummer
- `CHANGELOG.md` - Changelog mit allen Releases
- `releases/vX.Y.Z.md` - Detaillierte Release-Notes für jede Version

## 🎯 Beispiele

### Release 1.0.1 mit automatischen Notes

```bash
# Vollautomatisch
./scripts/create-release.sh patch --auto

# Output:
# [INFO] Aktuelle Version: v1.0.0
# [INFO] Neue Version: v1.0.1 (patch bump)
# [SUCCESS] Release-Notes automatisch generiert
# [SUCCESS] GitHub Release erstellt
# 🎉 Release v1.0.1 wurde erfolgreich erstellt!
```

### Release 1.1.0 mit bearbeiteten Notes

```bash
# Schritt 1: Template erstellen
./scripts/create-release.sh minor

# Editor öffnet sich automatisch
# → Release-Notes bearbeiten und speichern

# Schritt 2: Release finalisieren
./scripts/create-release.sh minor

# Release wird erstellt und gepusht
```

## 🐛 Fehlerbehandlung

### "Git-Arbeitsverzeichnis nicht sauber"

```bash
# Lösung: Änderungen committen
git add .
git commit -m "Beschreibung"
```

### "Nicht auf main Branch"

```bash
# Lösung: Zu main wechseln
git checkout main
```

### "gh CLI nicht installiert"

```bash
# Optional: GitHub CLI installieren
sudo apt install gh
gh auth login

# Oder: Release manuell auf GitHub erstellen
# → https://github.com/roimme65/icap-test-script/releases/new
```

## 📚 Semantic Versioning

Das Projekt folgt [Semantic Versioning 2.0.0](https://semver.org/lang/de/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking Changes
- **MINOR** (1.0.0 → 1.1.0): Neue Features (rückwärtskompatibel)
- **PATCH** (1.0.0 → 1.0.1): Bugfixes (rückwärtskompatibel)

## 🔗 Links

- [Keep a Changelog](https://keepachangelog.com/de/1.0.0/)
- [Semantic Versioning](https://semver.org/lang/de/)
- [GitHub CLI Dokumentation](https://cli.github.com/manual/)
