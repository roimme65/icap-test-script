# Git Prompts Dokumentation

Automatisierte Git-Commands für intelligentes Pushing und Pulling mit Diff-Anzeige und automatischen Commit-Messages.

## Global Speichern & Aktivieren

### Linux/macOS

1. **Kopiere die Prompt-Dateien zur globalen VS Code Copilot-Konfiguration:**

```bash
# Erstelle das Verzeichnis, falls es nicht existiert
mkdir -p ~/.config/Code/User/globalStorage/github.copilot/prompts

# Kopiere die Prompts
cp push-repository.md ~/.config/Code/User/globalStorage/github.copilot/prompts/
cp pull-repository.md ~/.config/Code/User/globalStorage/github.copilot/prompts/
```

2. **Überprüfe, dass die Dateien richtig kopiert wurden:**

```bash
ls -la ~/.config/Code/User/globalStorage/github.copilot/prompts/
```

Expected Output:
```
-rw-r--r-- ... push-repository.md
-rw-r--r-- ... pull-repository.md
```

### Windows

1. **Kopiere die Prompt-Dateien zur globalen VS Code Copilot-Konfiguration:**

```powershell
# Erstelle das Verzeichnis, falls es nicht existiert
$promptDir = "$env:APPDATA\Code\User\globalStorage\github.copilot\prompts"
New-Item -ItemType Directory -Force -Path $promptDir

# Kopiere die Prompts
Copy-Item -Path "push-repository.md" -Destination "$promptDir\"
Copy-Item -Path "pull-repository.md" -Destination "$promptDir\"
```

2. **Überprüfe die Installation:**

```powershell
Get-ChildItem "$env:APPDATA\Code\User\globalStorage\github.copilot\prompts\"
```

## Verwendung

Nach der Installation kannst du die Commands in VS Code nutzen:

### `/push-repository`

Führt einen intelligenten Git Push aus mit:
- ✅ Automatische Branch-Erkennung
- ✅ Diff-Anzeige vor dem Commit
- ✅ Intelligente Commit-Messages (Python, Markdown, Config, etc.)
- ✅ Automatischer Push zum Remote

**Beispiel:**
```bash
/push-repository
```

Output:
```
=== Branch: main ===
=== Changes zu committen (Statistik) ===
 README.md | 5 +++++
 1 file changed, 5 insertions(+)

=== Detaillierte Diffs ===
[...Diffs werden angezeigt...]

[main abc1234] Update documentation
 1 file changed, 5 insertions(+)
To github.com:username/repo.git
   old..new  main -> main
```

### `/pull-repository`

Führt einen intelligenten Git Pull aus mit:
- ✅ Automatische Branch-Erkennung
- ✅ Intelligente Fehlerbehandlung mit Rebase-Fallback
- ✅ Status-Überprüfung

**Beispiel:**
```bash
/pull-repository
```

Output:
```
Aktualisieren von abc1234..def5678
Fast-forward
 README.md | 3 +++
 1 file changed, 3 insertions(+)
```

## Dateistruktur

```
prompts/
├── README.md                 # Diese Datei
├── push-repository.md        # Push-Prompt mit Diff-Anzeige
└── pull-repository.md        # Pull-Prompt mit Fehlerbehandlung
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

1. **Immer die Diffs überprüfen** - Der Prompt zeigt dir immer die Changes vor dem Commit
2. **Regelmäßig pullen** - Nutze `/pull-repository` am Anfang der Arbeit
3. **Aussagekräftige Commits** - Die Auto-Detection basiert auf Dateitypen
4. **Testen vor Push** - Bei wichtigen Changes: erst lokal testen, dann pushen

## Weitere Dokumentation

- [push-repository.md](push-repository.md) - Detaillierte Push-Anweisungen
- [pull-repository.md](pull-repository.md) - Detaillierte Pull-Anweisungen

## Support

Bei Fragen oder Problemen:

1. Überprüfe `git status`
2. Nutze `git log --oneline -5` um letzte Commits zu sehen
3. Konsultiere die einzelnen Prompt-Dateien für Szenarien
