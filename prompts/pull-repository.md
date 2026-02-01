# Pull Repository Command

Führe einen Git Pull mit intelligenter Fehlerbehandlung durch.

## Anweisung (Automatisiert)

Führe diesen Combined-Befehl aus, der automatisch den aktuellen Branch ermittelt und pullst:

```bash
BRANCH=$(git branch --show-current) && git pull origin $BRANCH || git pull --rebase origin $BRANCH
```

**Was dieser Befehl macht:**
1. `BRANCH=$(git branch --show-current)` - Ermittelt den aktuellen Branch-Namen
2. `git pull origin $BRANCH` - Pullst vom entsprechenden Remote-Branch
3. Falls das fehlschlägt (`||`) - Fallback zu `git pull --rebase origin $BRANCH`

## Anweisung (Schritt-für-Schritt)

Alternativ, falls du lieber manuelle Kontrolle möchtest:

1. **Aktuellen Branch ermitteln:**
   ```bash
   git branch --show-current
   ```

2. **Git Pull vom Remote-Repository versuchen:**
   ```bash
   git pull origin <BRANCH_NAME>
   ```
   - Ersetzt `<BRANCH_NAME>` mit dem ermittelten Branch (z.B. `main`, `develop`)

3. **Bei Fehler: Rebase-Pull als Fallback:**
   Falls Schritt 2 fehlschlägt:
   ```bash
   git pull --rebase origin <BRANCH_NAME>
   ```

4. **Status überprüfen:**
   ```bash
   git status
   ```

## Parameter

- `#file` - Optional: Nur eine bestimmte Datei aktualisieren
- `#selection` - Optional: Nur selektive Branches pullen

## Workflow

### Scenario 1: Normaler Pull
```bash
BRANCH=$(git branch --show-current)
git pull origin $BRANCH
```

### Scenario 2: Pull mit Rebase bei Konflikt
```bash
BRANCH=$(git branch --show-current)
git pull origin $BRANCH || git pull --rebase origin $BRANCH
```

### Scenario 3: Nur bestimmten Branch pullen
```bash
git pull origin main
git pull --rebase origin main  # Falls Fehler
```

## Tipps

- Verwende `git fetch` um Remote-Changes zu sehen, bevor du pullst
- Bei Rebase-Konflikten: `git rebase --abort` um abzubrechen
- `git log --oneline -5` zeigt die letzten Commits
- Stelle sicher, dass deine lokalen Änderungen committed sind
- Nutze `git status` vor und nach dem Pull

## Häufige Fehler

- **"Your local changes would be overwritten":** Zuerst committen oder stashen
- **Rebase-Konflikt:** Manuell auflösen und `git rebase --continue`
- **Branch diverged:** Mit `git pull --rebase` die History neu aufbauen
