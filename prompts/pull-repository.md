# Pull Repository Prompt

Intelligentes Git Pull mit automatischer Branch-Erkennung und Fehlerbehandlung mit Rebase-Fallback.

## Schnellstart

Kopiere diesen Befehl und führe ihn aus:

```bash
BRANCH=$(git branch --show-current) && echo "=== Pulling from $BRANCH ===" && (git pull origin $BRANCH || git pull --rebase origin $BRANCH) && echo "✓ Pull successful" || echo "✗ Pull failed"
```

## Was dieser Befehl macht

1. ✅ **Branch-Erkennung** - Automatisch aktuellen Branch ermitteln
2. ✅ **Pull versuchen** - `git pull origin $BRANCH`
3. ✅ **Fallback bei Fehler** - Bei Konflikt: Rebase-Pull
4. ✅ **Status-Meldung** - Erfolg/Fehler anzeigen

## Verwendung (3 Varianten)

### Variante 1: Automatisch mit Fehlerbehandlung (Empfohlen)

```bash
BRANCH=$(git branch --show-current) && echo "=== Pulling from $BRANCH ===" && (git pull origin $BRANCH || git pull --rebase origin $BRANCH) && echo "✓ Pull successful" || echo "✗ Pull failed"
```

**Beste Wahl:** Auto-Pull mit Rebase-Fallback bei Konflikten.

### Variante 2: Nur normaler Pull (ohne Rebase)

```bash
BRANCH=$(git branch --show-current)
git pull origin $BRANCH
git status
```

**Einfach & Direkt:** Nur Pull ohne Rebase-Fallback.

### Variante 3: Spezifischen Branch pullen

```bash
git pull origin main      # Oder: develop, feature/branch, etc.
git status               # Status überprüfen
```

**Flexibel:** Explizit einen bestimmten Branch angeben.

## Pull-Szenarien

| Szenario | Befehl | Wann nutzen |
|----------|--------|-----------|
| **Normal Pull** | `git pull origin $BRANCH` | Keine lokalen Änderungen |
| **Mit Rebase** | `git pull --rebase origin $BRANCH` | Lineare History erwünscht |
| **Fetch first** | `git fetch && git rebase origin/$BRANCH` | Nur informieren, nicht sofort mergen |
| **Stash + Pull** | `git stash && git pull && git stash pop` | Lokale Änderungen, aber wollen nicht committen |

## Fehlerbehandlung

| Problem | Ursache | Lösung |
|---------|--------|--------|
| **Local changes overwritten** | Uncommitted Änderungen | `git stash` dann nochmal pullen |
| **Rebase conflict** | Unterschiedliche Historien | Manuell auflösen: `git rebase --continue` |
| **Branch not found** | Falscher Branch-Name | `git branch -a` - alle Branches anzeigen |
| **Pull timeout** | Netzwerkproblem | `git fetch` versuchen |
| **Already up to date** | Nichts Neues zu pullen | OK - alles aktuell |

## Hilfsbefehle

| Befehl | Beschreibung |
|--------|-------------|
| `git status` | Aktuellen Status anzeigen |
| `git branch --show-current` | Aktuellen Branch anzeigen |
| `git branch -a` | Alle Branches (lokal + remote) |
| `git fetch` | Nur Remote-Infos abrufen (kein Merge) |
| `git log --oneline -5` | Letzte 5 Commits |
| `git stash` | Lokale Änderungen speichern |
| `git stash pop` | Gespeicherte Änderungen wiederherstellen |

## Workflow-Beispiel

```bash
# 1. Status vor Pull
git status

# 2. Pull mit Auto-Fallback
BRANCH=$(git branch --show-current) && git pull origin $BRANCH || git pull --rebase origin $BRANCH

# 3. Status nach Pull
git status

# 4. Neue Commits anschauen
git log --oneline -3
```

## Best Practices

✅ **DO:**
- Pull am Anfang der Arbeit
- Status vor & nach Pull überprüfen
- Lokale Änderungen vor Pull committen oder stashen
- Bei Konflikten: Rebase abbrechen & neu starten

❌ **DON'T:**
- Pull ohne Status zu prüfen
- Force-Pull auf gemeinsamen Branches
- Pull mit uncommitted Änderungen
- Rebase auf öffentlichen Branches

## Integration mit anderen Prompts

```bash
# Workflow: Pull → Work → Push
/pull-repository            # Zuerst aktualisieren
# ... work ...
/push-repository            # Dann pushen
/pr-repository --target main  # Optional: PR erstellen
```
