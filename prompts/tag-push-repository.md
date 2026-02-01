# Tag Push Repository Prompt

Automatisiertes Versionieren mit Tag-Erstellung, Commit aller Änderungen und Push zum Remote.

## Schnellstart

```bash
# Standard Release Tag
git add . && git commit -m "chore: Release v1.0.5" && git tag -a v1.0.5 -m "Release v1.0.5" && git push origin main --tags
```

## Syntax

```bash
git tag -a TAG_VERSION -m "Message"
git push origin --tags
```

## Parameter & Varianten

| Parameter | Beispiel | Beschreibung |
|-----------|----------|-------------|
| `--tag` | `v1.0.5` | Semantic Versioning (v.MAJOR.MINOR.PATCH) |
| `--message` | `"Release v1.0.5"` | Custom Tag-Message |
| `--prerelease` | `v2.0.0-beta.1` | Pre-Release Tag |

## Verwendung (3 Varianten)

### Variante 1: Standard Release (Empfohlen)

```bash
# Änderungen committen
git add .
git commit -m "chore: Release v1.0.5"

# Tag erstellen
git tag -a v1.0.5 -m "Release v1.0.5"

# Push
git push origin main --tags
```

**Beste Wahl:** Clean Release mit Tag.

### Variante 2: Pre-Release (Alpha/Beta/RC)

```bash
git add .
git commit -m "chore: Pre-Release v2.0.0-rc.1"
git tag -a v2.0.0-rc.1 -m "Release Candidate 1"
git push origin develop --tags
```

**Für Testing:** Pre-Release Tags für Beta-Testing.

### Variante 3: Nur Tag (ohne Commit)

```bash
# Falls alles bereits committed ist
git tag -a v1.0.5 -m "Release v1.0.5"
git push origin --tags
```

**Flexible Wahl:** Für bereits committetete Änderungen.

## Semantic Versioning

```
v{MAJOR}.{MINOR}.{PATCH}[-{PRERELEASE}]

Beispiele:
- v1.0.0      → Erste Release
- v1.0.1      → Patch (Bugfixes)
- v1.1.0      → Minor (neue Features)
- v2.0.0      → Major (Breaking Changes)
- v2.0.0-alpha.1   → Alpha Pre-Release
- v2.0.0-beta.1    → Beta Pre-Release
- v2.0.0-rc.1      → Release Candidate
```

## Workflow-Szenarien

| Szenario | Befehle |
|----------|---------|
| **Patch Release** | `git commit -m "chore: v1.0.5"` → `git tag v1.0.5` → `git push --tags` |
| **Minor Release** | `git commit -m "feat: v1.1.0"` → `git tag v1.1.0` → `git push --tags` |
| **Major Release** | `git commit -m "feat: v2.0.0"` → `git tag v2.0.0` → `git push --tags` |
| **Pre-Release** | `git commit -m "rc1"` → `git tag v2.0.0-rc.1` → `git push --tags` |

## Häufige Befehle

| Befehl | Beschreibung |
|--------|-------------|
| `git tag -a TAG -m "Message"` | Annotated Tag erstellen |
| `git tag -l` | Alle Tags auflisten |
| `git show TAG` | Tag-Details anzeigen |
| `git push origin --tags` | Alle Tags pushen |
| `git push origin TAG` | Einzelnen Tag pushen |
| `git tag -d TAG` | Tag lokal löschen |
| `git push origin --delete TAG` | Tag remote löschen |

## Fehlerbehandlung

| Problem | Lösung |
|---------|--------|
| **Tag bereits vorhanden** | `git tag -d v1.0.5` → neu erstellen |
| **Vergessen zu committen** | `git add . && git commit -m "..."` zuerst |
| **Push fehlgeschlagen** | `git push origin main` zuerst, dann `git push --tags` |
| **Falscher Branch** | `git checkout main` zuerst |

## Hilfreiche Git-Befehle

```bash
# Aktuellen Status
git status

# Letzte Commits
git log --oneline -5

# Alle Tags anzeigen
git tag -l

# Tag-Details
git show v1.0.5

# Branch anzeigen
git branch --show-current
```

## Integration mit anderen Prompts

```bash
# Kompletter Workflow
/pull-repository            # Zuerst pullen
# ... work ...
/push-repository            # Änderungen pushen
/pr-repository              # PR erstellen & mergen
/tag-push-repository        # Release tagging
```

## Best Practices

✅ **DO:**
- Semantic Versioning nutzen (v.X.Y.Z)
- Vor Release testen
- CHANGELOG aktualisieren
- VERSION File synchron halten
- Aussagekräftige Tag-Messages

❌ **DON'T:**
- Ohne zu testen taggen
- Ungültige Tag-Formate (z.B. `release1`)
- Auf Feature-Branches taggen
- Force-Push nach Tagging

## Support

```bash
# Tag-Liste
git tag -l | tail -5

# Aktuellstes Tag anzeigen
git describe --tags --abbrev=0

# Commits seit letztem Tag
git log v1.0.4..v1.0.5

# Tag löschen + neu erstellen
git tag -d v1.0.5
git tag -a v1.0.5 -m "Fixed version"
git push origin --delete v1.0.5
git push origin v1.0.5
```
