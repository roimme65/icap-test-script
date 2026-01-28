#!/bin/bash
#
# ICAP Test Script - Automatische Release-Erstellung
#
# Verwendung: ./scripts/create-release.sh [major|minor|patch] [--auto]
#
# Beispiel: ./scripts/create-release.sh patch
#   → Bumpt 1.0.0 zu 1.0.1 (mit Editor)
# Beispiel: ./scripts/create-release.sh patch --auto
#   → Vollautomatisch ohne Editor
#

set -e

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktionen
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse Argumente
BUMP_TYPE="patch"
AUTO_MODE=false

for arg in "$@"; do
    case $arg in
        --auto)
            AUTO_MODE=true
            ;;
        major|minor|patch)
            BUMP_TYPE=$arg
            ;;
        *)
            print_error "Ungültiges Argument: $arg"
            echo "Verwendung: $0 [major|minor|patch] [--auto]"
            exit 1
            ;;
    esac
done

# Prüfe ob im richtigen Verzeichnis
if [ ! -f "icap_test.py" ] || [ ! -f "icap_server.py" ]; then
    print_error "Bitte aus dem Repository-Root ausführen"
    exit 1
fi

# Prüfe ob git sauber ist
if [ -n "$(git status --porcelain)" ]; then
    print_error "Git-Arbeitsverzeichnis nicht sauber. Bitte committe alle Änderungen."
    git status --short
    exit 1
fi

# Prüfe ob auf main Branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    print_error "Nicht auf main Branch. Aktuell auf: $CURRENT_BRANCH"
    exit 1
fi

# Hole aktuelle Version aus VERSION Datei (oder erstelle sie)
if [ ! -f "VERSION" ]; then
    echo "1.0.0" > VERSION
    print_warning "VERSION Datei erstellt mit 1.0.0"
fi

CURRENT_VERSION=$(cat VERSION)
print_info "Aktuelle Version: v$CURRENT_VERSION"

# Parse Version
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Bestimme neue Version
case $BUMP_TYPE in
    major)
        NEW_MAJOR=$((MAJOR + 1))
        NEW_MINOR=0
        NEW_PATCH=0
        ;;
    minor)
        NEW_MAJOR=$MAJOR
        NEW_MINOR=$((MINOR + 1))
        NEW_PATCH=0
        ;;
    patch)
        NEW_MAJOR=$MAJOR
        NEW_MINOR=$MINOR
        NEW_PATCH=$((PATCH + 1))
        ;;
esac

NEW_VERSION="${NEW_MAJOR}.${NEW_MINOR}.${NEW_PATCH}"
print_info "Neue Version: v$NEW_VERSION (${BUMP_TYPE} bump)"

# Frage Nutzer um Bestätigung (außer im Auto-Mode)
if [ "$AUTO_MODE" = false ]; then
    read -p "$(echo -e ${YELLOW}Möchtest du mit dem Release v$NEW_VERSION fortfahren? [y/N] ${NC})" -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Release abgebrochen"
        exit 0
    fi
else
    print_info "Auto-Mode: Fahre automatisch fort mit v$NEW_VERSION"
fi

# Schritt 1: Version aktualisieren
print_info "Aktualisiere VERSION Datei..."
echo "$NEW_VERSION" > VERSION
print_success "Version aktualisiert: v$NEW_VERSION"

# Schritt 2: Release-Notes erstellen
RELEASE_NOTES_FILE="releases/v${NEW_VERSION}.md"

# Funktion: Generiere automatische Release-Notes aus Git-Commits
generate_auto_release_notes() {
    local prev_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
    local new_version="v${NEW_VERSION}"
    
    print_info "Analysiere Commits seit letztem Release..."
    
    # Hole Commits seit letztem Tag
    local commits
    if [ -n "$prev_tag" ]; then
        commits=$(git log ${prev_tag}..HEAD --pretty=format:"%s" 2>/dev/null || echo "")
    else
        commits=$(git log --pretty=format:"%s" 2>/dev/null || echo "")
    fi
    
    # Kategorisiere Commits
    local features=""
    local improvements=""
    local bugfixes=""
    local other=""
    
    while IFS= read -r commit; do
        [[ -z "$commit" ]] && continue
        
        if [[ "$commit" =~ ^(feat|feature|add|✨|Initial) ]] || [[ "$commit" =~ [Nn]ew[[:space:]][Ff]eature ]]; then
            features="${features}- ${commit}\n"
        elif [[ "$commit" =~ ^(fix|bug|🐛) ]]; then
            bugfixes="${bugfixes}- ${commit}\n"
        elif [[ "$commit" =~ ^(improve|enhance|update|refactor|🔧|⚡|docs) ]]; then
            improvements="${improvements}- ${commit}\n"
        else
            other="${other}- ${commit}\n"
        fi
    done <<< "$commits"
    
    # Wenn keine kategorisierten Commits, nutze "other"
    if [[ -z "$features" && -z "$bugfixes" && -z "$improvements" ]]; then
        improvements="$other"
    fi
    
    # Default Werte wenn leer
    [[ -z "$features" ]] && features="- Initial Release mit vollständigem Feature-Set\n"
    [[ -z "$improvements" ]] && improvements="- Dokumentation und Code-Qualität verbessert\n"
    [[ -z "$bugfixes" ]] && bugfixes="- Keine Bugfixes in diesem Release\n"
    
    # Erstelle Release-Notes
    cat > "$RELEASE_NOTES_FILE" << EOF
# Release v${NEW_VERSION}

**Veröffentlicht:** $(date +"%-d. %B %Y" 2>/dev/null || date +"%d. %B %Y")

## 📦 Übersicht

ICAP Test System v${NEW_VERSION} - Python-basierter ICAP-Server mit ClamAV-Integration.

## 🎯 Neue Features

$(echo -e "$features")

## 🔧 Verbesserungen

$(echo -e "$improvements")

## 🐛 Bugfixes

$(echo -e "$bugfixes")

## 🚀 Installation

### Mit Docker (empfohlen)

\`\`\`bash
# Repository klonen
git clone https://github.com/roimme65/icap-test-script.git
cd icap-test-script

# Container starten
docker compose up -d

# Tests ausführen
python3 icap_test.py --host localhost --port 1344 --service avscan
\`\`\`

### Standalone

\`\`\`bash
# Python ICAP-Server
python3 icap_server.py

# Test-Client
python3 icap_test.py --host <icap-server> --port 1344 --service avscan
\`\`\`

## 📋 Systemanforderungen

- **Python:** 3.6 oder höher
- **Docker:** 20.10+ (optional)
- **Docker Compose:** 1.29+ oder Docker Compose Plugin

## 🔗 Links

- [README](../README.md)
- [Docker-Dokumentation](../DOCKER.md)
- [CHANGELOG](../CHANGELOG.md)
- [GitHub Release](https://github.com/roimme65/icap-test-script/releases/tag/v${NEW_VERSION})

---

**Vielen Dank fürs Verwenden! 🙏**
EOF
}

if [ -f "$RELEASE_NOTES_FILE" ]; then
    print_warning "Release-Notes existieren bereits: $RELEASE_NOTES_FILE"
else
    if [ "$AUTO_MODE" = true ]; then
        generate_auto_release_notes
        print_success "Release-Notes automatisch generiert"
    else
        print_info "Erstelle Release-Notes Template..."
        generate_auto_release_notes
        print_success "Release-Notes Template erstellt: $RELEASE_NOTES_FILE"
        print_warning "Bitte bearbeite die Release-Notes und führe das Skript dann erneut aus"
        
        # Öffne Editor
        if command -v ${EDITOR:-nano} &> /dev/null; then
            ${EDITOR:-nano} "$RELEASE_NOTES_FILE"
        fi
        
        print_info "Nach dem Bearbeiten führe das Skript erneut aus:"
        echo "  ./scripts/create-release.sh $BUMP_TYPE"
        exit 0
    fi
fi

# Schritt 3: CHANGELOG.md aktualisieren (oder erstellen)
print_info "Aktualisiere CHANGELOG.md..."

if [ ! -f "CHANGELOG.md" ]; then
    cat > CHANGELOG.md << 'EOFHEAD'
# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

---

EOFHEAD
fi

# Temporäre Datei mit neuem Eintrag
{
    head -n 7 CHANGELOG.md
    cat << EOFCHG

## [${NEW_VERSION}] - $(date +"%Y-%m-%d")

### Siehe
- Detaillierte Release-Notes: [releases/v${NEW_VERSION}.md](releases/v${NEW_VERSION}.md)

---
EOFCHG
    tail -n +8 CHANGELOG.md
} > CHANGELOG.md.new
mv CHANGELOG.md.new CHANGELOG.md

print_success "CHANGELOG.md aktualisiert"

# Schritt 4: Git commit
print_info "Erstelle Git-Commit..."
git add VERSION "$RELEASE_NOTES_FILE" CHANGELOG.md
git commit -m "Release v${NEW_VERSION}

- Bump version to v${NEW_VERSION}
- Add release notes
- Update CHANGELOG"
print_success "Commit erstellt"

# Schritt 5: Git Tag erstellen
print_info "Erstelle Git-Tag v${NEW_VERSION}..."
git tag -a "v${NEW_VERSION}" -m "Release ${NEW_VERSION}"
print_success "Tag erstellt: v${NEW_VERSION}"

# Schritt 6: Push zu GitHub
print_info "Pushe zu GitHub..."
git push origin main
git push origin "v${NEW_VERSION}"
print_success "Gepusht zu GitHub"

# Schritt 7: Erstelle GitHub Release
print_info "Erstelle GitHub Release..."

# Warte kurz, damit GitHub den Tag registriert
sleep 2

# Erstelle Release mit gh CLI
if command -v gh &> /dev/null; then
    if gh release create "v${NEW_VERSION}" \
        --title "v${NEW_VERSION} - ICAP Test System" \
        --notes-file "$RELEASE_NOTES_FILE" \
        icap_test.py \
        icap_server.py; then
        print_success "GitHub Release erstellt: https://github.com/roimme65/icap-test-script/releases/tag/v${NEW_VERSION}"
    else
        print_warning "GitHub Release konnte nicht erstellt werden. Prüfe gh CLI Authentifizierung."
    fi
else
    print_warning "gh CLI nicht installiert. Release manuell auf GitHub erstellen."
    print_info "Oder installiere gh CLI: https://cli.github.com/"
fi

# Fertig!
echo ""
print_success "🎉 Release v${NEW_VERSION} wurde erfolgreich erstellt!"
echo ""
print_info "Das Release ist verfügbar unter:"
echo "  https://github.com/roimme65/icap-test-script/releases/tag/v${NEW_VERSION}"
echo ""
