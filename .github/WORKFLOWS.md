# GitHub Workflows Documentation

Dokumentation für die GitHub Actions Workflows im `.github/workflows/` Verzeichnis.

## Verfügbare Workflows

### 1. Release Workflow (`release.yml`)

Verwaltet die automatische Release-Erstellung auf GitHub.

**Trigger:** Wenn ein Tag im Format `v*.*.*` gepusht wird
- z.B. `v1.0.10`, `v2.1.0`

**Schritte:**
1. **Validate Release**
   - Prüft Python-Syntax
   - Verifiziert dass Tag-Version mit Script-Version übereinstimmt
   - Prüft ob Release-Notizen existieren

2. **Create GitHub Release**
   - Erstellt neues GitHub Release
   - Fügt Release-Notizen aus `releases/v{version}.md` hinzu

**Beispiel-Trigger:**
```bash
git tag -a v1.0.10 -m "Release v1.0.10"
git push origin v1.0.10
```

### 2. Tests Workflow (`test.yml`)

Führt automatische Tests und Quality Checks aus.

**Trigger:** 
- Push zu `main` oder `develop` Branch
- Änderungen an `icap_*.py`, Docker-Dateien oder diesem Workflow

**Checks:**
1. **Syntax Check** - Python-Syntax Validierung
2. **Docker Build** - Test für Docker-Image Build
3. **Code Quality** - Dateigröße, Versionskonsistenz
4. **Linting** - Python Code Style mit flake8 und pylint

### 3. Pull Request Check Workflow (`pr-check.yml`)

Validiert Pull Requests vor dem Merge.

**Trigger:** Wenn eine PR zu `main` oder `develop` geöffnet wird

**Validierungen:**
1. **PR Validation**
   - Prüft PR-Beschreibung
   - Prüft ob Merge-Konflikte existieren

2. **Python Quality Checks**
   - Syntax-Validierung
   - Import-Checks

3. **Changed Files Analysis**
   - Analysiert welche Dateien geändert wurden
   - Prüft ob VERSION und CHANGELOG aktualisiert wurden

## Automatische GitHub Releases

Die Release-Workflow erstellt automatisch ein GitHub Release mit den folgenden Details:

- **Release Name:** Release v{version}
- **Tag:** v{version}
- **Body:** Inhalt aus `releases/v{version}.md`

### Manuelles Release erstellen

Mit dem [create-release.py](../scripts/create-release.py) Skript:

```bash
python3 scripts/create-release.py patch
```

Das Skript:
1. Erhöht Versionsnummer (patch/minor/major)
2. Aktualisiert alle Versionsnummern im Projekt
3. Erstellt Release-Notizen Template
4. Committed und pusht einen Tag
5. GitHub Actions erstellt automatisch das Release

## Workflow Status

Die Workflow-Status können unter [GitHub Actions](https://github.com/roimme65/icap-test-script/actions) verfolgt werden.

### Status-Badges

In README einzufügen:
```markdown
![Tests](https://github.com/roimme65/icap-test-script/workflows/Tests/badge.svg)
![Release](https://github.com/roimme65/icap-test-script/workflows/Release/badge.svg)
```

## Secrets und Permissions

Die Release-Workflow benötigt:
- **GITHUB_TOKEN** - Automatisch verfügbar
- **Environment:** `production`

## Fehlerbehandlung

### Release schlägt fehl

Häufige Gründe:
1. Version-Mismatch - Tag != Script Version
   - Lösung: Release-Notizen manuell in `releases/v{version}.md` erstellen

2. Ungültige Syntax im Python-Code
   - Lösung: `python -m py_compile icap_*.py` ausführen

3. Release-Notizen fehlen
   - Lösung: Datei `releases/v{version}.md` erstellen

### PR-Check fehlgeschlagen

Häufige Gründe:
1. Merge-Konflikte
   - Lösung: Konflikte lokal auflösen und neu pushen

2. Tests fehlgeschlagen
   - Lösung: Lokal testen und Fehler beheben

## Zusammenfassung

| Workflow | Trigger | Zweck |
|----------|---------|-------|
| Release | Tag push | GitHub Release erstellen |
| Tests | Push/PR | Code Quality validieren |
| PR Check | PR offen | PR validieren |
