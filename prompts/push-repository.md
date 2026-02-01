# Push Repository Command

Führe einen Git Push mit automatischem Branch-Erkennung, Diff-Anzeige und intelligenter Commit-Message durch.

## Anweisung (Automatisiert mit Diff-Anzeige)

Führe diesen Combined-Befehl aus, der automatisch arbeitet und Diffs zeigt:

```bash
BRANCH=$(git branch --show-current)
echo "=== Branch: $BRANCH ==="
git add .
echo ""
echo "=== Changes zu committen (Statistik) ==="
git diff --cached --stat
echo ""
echo "=== Detaillierte Diffs ==="
git diff --cached
echo ""
# Auto-Commit mit intelligenter Message
if git diff --cached --name-only | grep -q "\.py$"; then
  git commit -m "Update Python scripts"
elif git diff --cached --name-only | grep -q "\.md$"; then
  git commit -m "Update documentation"
elif git diff --cached --name-only | grep -q "\.json$"; then
  git commit -m "Update configuration"
else
  git commit -m "Update repository"
fi
git push origin $BRANCH
```

## Anweisung (Mit Benutzer-Input und Diff-Anzeige)

Falls du die Commit-Message manuell eingeben möchtest:

```bash
BRANCH=$(git branch --show-current)
echo "=== Branch: $BRANCH ==="
git add .
echo ""
echo "=== Changes zu committen ==="
git diff --cached --stat
echo ""
echo "=== Detaillierte Diffs ==="
git diff --cached
echo ""
read -p "Commit-Message [Auto-generiert]: " CUSTOM_MSG
if [ -n "$CUSTOM_MSG" ]; then
  git commit -m "$CUSTOM_MSG"
else
  if git diff --cached --name-only | grep -q "\.py$"; then
    git commit -m "Update Python scripts"
  elif git diff --cached --name-only | grep -q "\.md$"; then
    git commit -m "Update documentation"
  else
    git commit -m "Update repository"
  fi
fi
git push origin $BRANCH
```

## Anweisung (Nur spezifische Dateien)

```bash
BRANCH=$(git branch --show-current)
git add <datei1> <datei2>
echo "=== Changes zu committen ==="
git diff --cached --stat
git commit -m "Update specific files"
git push origin $BRANCH
```

## Parameter

- `#selection` - Wenn Text ausgewählt ist, als Commit-Nachricht verwenden
- `#file` - Optional: Nur eine bestimmte Datei pushen

## Workflow

### Scenario 1: Automatisch mit Diffs anzeigen (Empfohlen)
```bash
BRANCH=$(git branch --show-current) && git add . && \
echo "=== Changes ===" && git diff --cached --stat && \
git diff --cached && \
if git diff --cached --name-only | grep -q "\.py$"; then \
  git commit -m "Update Python scripts"; \
elif git diff --cached --name-only | grep -q "\.md$"; then \
  git commit -m "Update documentation"; \
else \
  git commit -m "Update repository"; \
fi && \
git push origin $BRANCH
```

### Scenario 2: Mit manueller Bestätigung
```bash
git add .
git diff --cached --stat
echo "Überprüfe die Diffs oben"
read -p "Weiter mit Enter..."
git commit -m "MESSAGE"
git push
```

### Scenario 3: Nur Diffs anzeigen (ohne Push)
```bash
git diff
git diff --stat
```

## Tipps

- `git diff --cached --stat` zeigt eine schöne Statistik
- `git diff --cached` zeigt alle Änderungen im Detail
- Überprüfe die Diffs IMMER vor dem Commit
- Intelligente Messages: Python, Dokumentation, Config etc. werden erkannt
- `git log --oneline -5` zeigt letzte Commits
- Bei Problemen: `git push --force-with-lease` nur wenn wirklich nötig

## Häufige Fehler

- **"rejected (fetch first)":** Erst pullen mit `/pull-repository`
- **SSH-Passphrase:** SSH-Agent starten mit `eval $(ssh-agent -s) && ssh-add`
- **Nichts zu committen:** Nur `git push` ohne add/commit
- **Diff zu groß:** Nutze `git diff --stat` für Überblick statt vollständigem Diff
