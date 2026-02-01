# Git Prompts Dokumentation

Automatisierte Git-Commands für intelligentes Pushing und Pulling mit Diff-Anzeige und automatischen Commit-Messages.

## Global Speichern & Aktivieren

### Linux/macOS

1. **Kopiere alle Prompt-Dateien zur globalen VS Code Copilot-Konfiguration:**

```bash
# Erstelle das Verzeichnis, falls es nicht existiert
mkdir -p ~/.config/Code/User/globalStorage/github.copilot/prompts

# Kopiere alle Prompts
cp push-repository.md pull-repository.md pr-repository.md tag-push-repository.md ~/.config/Code/User/globalStorage/github.copilot/prompts/
```

2. **Überprüfe, dass alle Dateien richtig kopiert wurden:**

```bash
ls -la ~/.config/Code/User/globalStorage/github.copilot/prompts/
```

Expected Output:
```
-rw-r--r-- ... push-repository.md
-rw-r--r-- ... pull-repository.md
-rw-r--r-- ... pr-repository.md
-rw-r--r-- ... tag-push-repository.md
```

### Windows

1. **Kopiere alle Prompt-Dateien zur globalen VS Code Copilot-Konfiguration:**

```powershell
# Erstelle das Verzeichnis, falls es nicht existiert
$promptDir = "$env:APPDATA\Code\User\globalStorage\github.copilot\prompts"
New-Item -ItemType Directory -Force -Path $promptDir

# Kopiere alle Prompts
Copy-Item -Path "push-repository.md", "pull-repository.md", "pr-repository.md", "tag-push-repository.md" -Destination "$promptDir\"
```

2. **Überprüfe die Installation:**

```powershell
Get-ChildItem "$env:APPDATA\Code\User\globalStorage\github.copilot\prompts\"
```

## Übersicht

| Prompt | Command | Funktion |
|--------|---------|----------|
| **Push Repository** | `/push-repository` | Git Push mit Diff-Anzeige & Auto-Commit-Messages |
| **Pull Repository** | `/pull-repository` | Git Pull mit Fehlerbehandlung & Status-Check |
| **PR Repository** | `/pr-repository` | GitHub PR erstellen & mergen mit Branch-Management & Issue-Linking |
| **Tag Push Repository** | `/tag-push-repository` | Tag erstellen, Änderungen committen und pushen |

## Verwendung

Nach der Installation kopierst du die Befehle aus den einzelnen Prompt-Dateien und führst sie in deinem Terminal aus:

### `/push-repository`

**Schnellstart-Befehl:**
```bash
BRANCH=$(git branch --show-current) && git add . && echo "=== Changes ===" && git diff --cached --stat && git diff --cached && if git diff --cached --name-only | grep -qE "\.(py|js|ts)$"; then git commit -m "feat: Update scripts"; elif git diff --cached --name-only | grep -q "\.md$"; then git commit -m "docs: Update documentation"; else git commit -m "chore: Update repository"; fi && git push origin $BRANCH
```

**Features:**
- ✅ Automatische Branch-Erkennung
- ✅ Diff-Anzeige vor dem Commit
- ✅ Intelligente Commit-Messages
- ✅ Automatischer Push zum Remote

Siehe [push-repository.md](push-repository.md) für 3 Varianten und Details.

### `/pull-repository`

**Schnellstart-Befehl:**
```bash
BRANCH=$(git branch --show-current) && echo "=== Pulling from $BRANCH ===" && (git pull origin $BRANCH || git pull --rebase origin $BRANCH) && echo "✓ Pull successful" || echo "✗ Pull failed"
```

**Features:**
- ✅ Automatische Branch-Erkennung
- ✅ Intelligente Fehlerbehandlung
- ✅ Rebase-Fallback bei Konflikten

Siehe [pull-repository.md](pull-repository.md) für 3 Varianten und Details.

### `/pr-repository`

**Schnellstart-Befehl:**
```bash
gh pr create --title "Feature: $(git log -1 --pretty=%B)" --body "Auto-generated PR" --fill && gh pr merge --auto
```

**Anforderung:** GitHub CLI (`gh`) installiert

**Features:**
- ✅ GitHub PR erstellen
- ✅ Auto-Merge
- ✅ Issue-Linking (Fixes #123)
- ✅ Draft-PRs

Siehe [pr-repository.md](pr-repository.md) für 3 Varianten und Details.

### `/tag-push-repository`

**Schnellstart-Befehl:**
```bash
git add . && git commit -m "chore: Release v1.0.5" && git tag -a v1.0.5 -m "Release v1.0.5" && git push origin main --tags
```

**Features:**
- ✅ Semantic Versioning (v.X.Y.Z)
- ✅ Tag-Erstellung
- ✅ Pre-Release Support
- ✅ Automatischer Push

Siehe [tag-push-repository.md](tag-push-repository.md) für 3 Varianten und Details.

## Dateistruktur

```
prompts/
├── README.md                 # Diese Datei
├── push-repository.md        # Push-Prompt mit Diff-Anzeige
├── pull-repository.md        # Pull-Prompt mit Fehlerbehandlung
├── pr-repository.md          # PR-Prompt mit GitHub Integration
└── tag-push-repository.md    # Tag-Prompt für Versioning & Releases
```

## Anforderungen

- VS Code mit GitHub Copilot Extension
- Git installiert und konfiguriert
- SSH-Key für GitHub konfiguriert (optional, aber empfohlen)

## Konfiguration

### Git-Identität setzen (Global)

```bash
git config --global user.email "deine@email.com"
git config --global user.name "Dein Name"
```

### SSH-Key konfigurieren (Optional)

Falls du Multiple SSH-Keys für verschiedene GitHub-Accounts nutzt:

Bearbeite `~/.ssh/config`:

```
Host github.com-myaccount
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_my_account
    IdentitiesOnly yes
```

Passe dann dein Repository-Remote an:

```bash
git remote set-url origin git@github.com-myaccount:username/repo.git
```

## Häufige Fehler & Lösungen

### "rejected (fetch first)"
**Lösung:** Nutze `/pull-repository` zuerst, um Remote-Changes zu pullen

```bash
/pull-repository
```

### "Your local changes would be overwritten"
**Lösung:** Committen oder Änderungen stashen

```bash
git stash  # Speichert Änderungen temporär
/pull-repository
```

### "Passphrase for key ..." wird immer gefragt
**Lösung:** SSH-Agent starten

```bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_ed25519  # Ersetze mit deinem Key
```

### Prompt wird nicht erkannt
**Lösung:** Überprüfe den Pfad:

```bash
ls -la ~/.config/Code/User/globalStorage/github.copilot/prompts/push-repository.md
```

Falls nicht vorhanden, kopiere die Dateien nochmal.

## Tipps & Best Practices

1. **Kopiere die Schnellstart-Befehle** - Alle Prompts haben Copy-Ready Befehle am Anfang
2. **3 Varianten pro Prompt** - Wähle zwischen Automatisch, Flexibel oder Einfach
3. **Befehle kombinieren** - Pull → Work → Push → PR → Tag-Release Workflow
4. **Tabellen nutzen** - Parameter, Befehle und Fehlerbehandlung sind in Tabellen organisiert

## Weitere Dokumentation

- [push-repository.md](push-repository.md) - Detaillierte Push-Anweisungen
- [pull-repository.md](pull-repository.md) - Detaillierte Pull-Anweisungen
- [pr-repository.md](pr-repository.md) - Detaillierte PR-Management-Anweisungen
- [tag-push-repository.md](tag-push-repository.md) - Detaillierte Tag & Release-Anweisungen

## Support

Bei Fragen oder Problemen:

1. Überprüfe `git status`
2. Nutze `git log --oneline -5` um letzte Commits zu sehen
3. Konsultiere die einzelnen Prompt-Dateien für Szenarien
