# Push Repository Prompt

Intelligentes Git Push mit automatischer Branch-Erkennung, Diff-Anzeige und intelligenten Commit-Messages.

## Schnellstart

Kopiere diesen Befehl und führe ihn aus:

```bash
BRANCH=$(git branch --show-current) && git add . && echo "=== Changes ===" && git diff --cached --stat && git diff --cached && if git diff --cached --name-only | grep -qE "\.(py|js|ts)$"; then git commit -m "feat: Update scripts"; elif git diff --cached --name-only | grep -q "\.md$"; then git commit -m "docs: Update documentation"; else git commit -m "chore: Update repository"; fi && git push origin $BRANCH
```

## Was dieser Befehl macht

1. ✅ **Branch-Erkennung** - Automatisch aktuellen Branch ermitteln
2. ✅ **Änderungen hinzufügen** - `git add .`
3. ✅ **Diffs anzeigen** - Statistik + Detaillierte Diffs
4. ✅ **Auto-Commit-Message** - Intelligente Messages basierend auf Dateitypen
5. ✅ **Push** - Zum Remote pushen

## Verwendung (3 Varianten)

### Variante 1: Automatisch (Empfohlen)

```bash
BRANCH=$(git branch --show-current) && git add . && echo "=== Changes ===" && git diff --cached --stat && git diff --cached && if git diff --cached --name-only | grep -qE "\.(py|js|ts)$"; then git commit -m "feat: Update scripts"; elif git diff --cached --name-only | grep -q "\.md$"; then git commit -m "docs: Update documentation"; else git commit -m "chore: Update repository"; fi && git push origin $BRANCH
```

**Beste Wahl:** Zeigt Diffs, committed automatisch, pusht.

### Variante 2: Mit manueller Commit-Message

```bash
BRANCH=$(git branch --show-current)
git add .
echo "=== Changes ===" && git diff --cached --stat && git diff --cached
read -p "Commit-Message: " MSG
git commit -m "$MSG"
git push origin $BRANCH
```

**Flexible Wahl:** Du kontrollierst die Commit-Message.

### Variante 3: Nur spezifische Dateien

```bash
git add file1.md file2.py
git diff --cached --stat && git diff --cached
git commit -m "Update specific files"
git push origin $(git branch --show-current)
```

**Präzise Wahl:** Nur bestimmte Dateien.

## Auto-Detection Commit-Messages

| Dateityp | Message |
|----------|---------|
| `*.py`, `*.js`, `*.ts` | `feat: Update scripts` |
| `*.md` | `docs: Update documentation` |
| `*.json`, `*.yml` | `chore: Update configuration` |
| Andere | `chore: Update repository` |

## Tipps & Tricks

| Befehl | Beschreibung |
|--------|-------------|
| `git diff --cached --stat` | Übersicht: Welche Dateien, wie viele Änderungen |
| `git diff --cached` | Detaillierte Diffs aller Änderungen |
| `git log --oneline -5` | Letzte 5 Commits anzeigen |
| `git status` | Status vor Commit überprüfen |
| `git reset` | Alle `git add` rückgängig machen |

## Fehlerbehandlung

| Problem | Lösung |
|---------|--------|
| **rejected (fetch first)** | Erst `git pull` machen |
| **SSH-Passphrase gefragt** | `eval $(ssh-agent -s) && ssh-add ~/.ssh/id_ed25519` |
| **Nichts zum Committen** | `git status` - gibt es Änderungen? |
| **Wrong branch** | `git checkout correct-branch` zuerst |
| **Force Push nötig** | `git push --force-with-lease` (vorsichtig!) |

## Workflow-Beispiel

```bash
# 1. Änderungen machen
vim README.md

# 2. Status checken
git status

# 3. Pushen (dieser Prompt)
BRANCH=$(git branch --show-current) && git add . && git diff --cached --stat && git diff --cached && git commit -m "docs: Update README" && git push origin $BRANCH

# 4. Erfolg prüfen
git log --oneline -3
```

## Best Practices

✅ **DO:**
- Diffs vor Commit überprüfen
- Aussagekräftige Commit-Messages
- Kleine, fokussierte Commits
- Regelmäßig pushen (nicht warten)

❌ **DON'T:**
- Unkontrolliert `git add .` nutzen
- Große Multi-Feature Commits
- Ohne zu überprüfen pushen
- Force-Push auf main/master

## Integration mit anderen Prompts

```bash
# Workflow: Pull → Work → Push
/pull-repository        # Zuerst aktualisieren
# ... work ...
/push-repository        # Dann pushen
/pr-repository --target main  # Optional: PR erstellen
```
