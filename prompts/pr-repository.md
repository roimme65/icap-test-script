# PR Repository Prompt

Intelligentes GitHub Pull-Request Management mit automatischer Branch-Verwaltung und Issue-Linking.

## Anforderungen

- **GitHub CLI** (`gh`): https://cli.github.com/
- `gh auth login` - Einmalige Authentifizierung
- Git Repository mit GitHub Remote

## Schnellstart

```bash
# Basis PR erstellen & mergen
gh pr create --title "Feature: $(git log -1 --pretty=%B)" --body "Auto-generated PR" --fill && gh pr merge --auto

# Mit Issue-Link
gh pr create --title "Fix: Issue" --body "Fixes #123" && gh pr merge --auto
```

## Parameter & Varianten

| Parameter | Beispiel | Beschreibung |
|-----------|----------|-------------|
| `--target` | `gh pr create --base develop` | Target Branch (Default: main) |
| `--no-delete` | Nicht löschen manuell | Source Branch behalten |
| `--issue` | `--body "Fixes #123"` | Issue-Link in Description |
| `--draft` | `gh pr create --draft` | Als Draft erstellen |

## Verwendung (3 Varianten)

### Variante 1: Auto PR erstellen & Auto-mergen (Empfohlen)

```bash
BRANCH=$(git branch --show-current) && \
gh pr create \
  --title "feat: Auto PR from $BRANCH" \
  --body "Auto-generated PR" \
  --base main && \
echo "✓ PR created"
```

**Beste Wahl:** PR wird erstellt und automatisch gemergt.

### Variante 2: PR mit Issue-Link & Branch behalten

```bash
BRANCH=$(git branch --show-current) && \
gh pr create \
  --title "fix: Resolve issue" \
  --body "Fixes #123" \
  --base develop && \
echo "✓ PR #$(gh pr view --json number -q) created"
```

**Flexible Wahl:** Issue-Link, Branch bleibt erhalten.

### Variante 3: Draft PR für Review

```bash
gh pr create \
  --draft \
  --title "WIP: Feature in progress" \
  --body "For review only" \
  --base main
```

**Review-Modus:** Draft bis zur Fertigstellung.

## Workflow-Szenarien

| Szenario | Befehl |
|----------|--------|
| **Standard PR (main)** | `gh pr create --fill` |
| **PR mit Issue** | `gh pr create --body "Fixes #123"` |
| **Draft PR** | `gh pr create --draft` |
| **PR anzeigen** | `gh pr view` |
| **Auto-mergen** | `gh pr merge --auto` |
| **Merge + Branch löschen** | `gh pr merge && git branch -D $BRANCH` |

## Merge-Optionen

```bash
# Standard Merge
gh pr merge PR_ID --merge

# Mit Branch-Deletion
gh pr merge PR_ID --merge --delete-branch

# Mit Custom Message
gh pr merge PR_ID --merge -t "Release v1.0.5"
```

## Häufige Befehle

| Befehl | Beschreibung |
|--------|-------------|
| `gh pr create` | Neue PR erstellen |
| `gh pr view` | Aktuelle PR anzeigen |
| `gh pr list` | Alle PRs auflisten |
| `gh pr merge` | PR mergen |
| `gh pr close` | PR schließen |
| `gh pr checks` | PR Status & Tests prüfen |

## Fehlerbehandlung

| Problem | Lösung |
|---------|--------|
| **PR bereits offen** | `gh pr view` - Check existierende PRs |
| **Auth failed** | `gh auth logout && gh auth login` |
| **No commits** | Erst committen: `/push-repository` |
| **Branch nicht gepusht** | `git push origin $BRANCH` |
| **Merge conflict** | GitHub UI oder lokal auflösen |

## Hilfreiche Git-Befehle

```bash
# Aktuellen Branch anzeigen
git branch --show-current

# PR Branch löschen (nach Merge)
git branch -D feature/branch

# Alle Branches anzeigen
git branch -a

# Remote Branches synchronisieren
git fetch origin
```

## Integration mit anderen Prompts

```bash
# Kompletter Workflow
/pull-repository          # Zuerst pullen
# ... work ...
/push-repository          # Änderungen pushen
/pr-repository            # PR erstellen & mergen
/tag-push-repository --tag v1.0.5  # Release taggen
```

## Best Practices

✅ **DO:**
- Kleine, fokussierte PRs (1 Feature pro PR)
- Aussagekräftige PR-Titles
- Issue-Links nutzen (`Fixes #123`)
- Tests vor Merge ausführen

❌ **DON'T:**
- Große Multi-Feature PRs
- Ohne Description mergen
- Force-Merge auf main/master
- Ohne Code-Review mergen

## Support

```bash
# GitHub CLI Status
gh auth status

# PR-Details anzeigen
gh pr view --json title,body,state

# Aktuelle PR mergen
gh pr merge --auto

# PR schließen (ohne Merge)
gh pr close
```
