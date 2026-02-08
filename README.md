# ICAP Security Testing Suite

[![Version](https://img.shields.io/badge/version-1.1.9-blue.svg)](VERSION)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](docker-compose.yml)
[![Security](https://img.shields.io/badge/security-audit-success.svg)](SECURITY_SCAN.md)

**Languages:** 🇬🇧 [English](README.md) | 🇩🇪 [Deutsch](README.de.md)

> 🛡️ **Professional ICAP Testing & Development Platform**  
> Complete, production-ready ICAP solution with Python server, ClamAV integration, and automated security tests.

---

## 📖 Project Overview

This project provides a **complete test and development environment** for the ICAP protocol (Internet Content Adaptation Protocol - RFC 3507). It combines a minimalist yet fully functional ICAP server with an integrated antivirus engine and comprehensive test framework.

### 🎯 Key Objectives

- **🚀 Quick Start:** Ready to use in 3 minutes with Docker
- **📚 Learning Resource:** Understand and implement the ICAP protocol
- **🧪 Testing Framework:** Automated tests for ICAP implementations
- **🔧 Development Tool:** Foundation for custom ICAP server development
- **✅ Quality Assurance:** Validation of antivirus integrations

### 🌟 Why This Project?

**Simplicity meets functionality:**
- ✨ Pure Python - No complicated C dependencies or build processes
- 📦 Plug & Play - Docker setup in seconds instead of hours
- 🎓 Well documented - Every line of code explained and understandable
- 🔬 Testable - EICAR tests and comprehensive validation included
- 🚀 Production-ready - Real ClamAV integration, multi-threading, robust error handling

**Perfect for:**
- 👨‍💻 Developers who want to test ICAP clients
- 🏢 Organizations that need to validate content filtering
- 🎓 Learners who want to understand ICAP
- 🧑‍🔬 QA engineers for automated testing
- 🔐 Security teams for antivirus validation

## 🔐 Security

This project is **security-audited and vetted**. See [SECURITY_SCAN.md](SECURITY_SCAN.md) for:
- ✅ Complete vulnerability assessment
- ✅ Bandit security scan results (0 vulnerabilities)
- ✅ Production readiness checklist
- ⚠️ Important TLS/SSL recommendations

**Quick verdict:** Safe for lab/test environments • Requires TLS for production networks

---

## 🎯 Features

### Test Script ([icap_test.py](icap_test.py))
- ✓ EICAR test file for virus detection
- ✓ Clean file testing (false-positive check)
- ✓ OPTIONS request support
- ✓ Detailed status output
- ✓ Configurable server parameters
- ✓ Version and author information (`--version`, `--author`)

### ICAP Server ([icap_server.py](icap_server.py))
- ✓ **Pure Python** - ~280 lines of code
- ✓ **ICAP/1.0 compliant** - OPTIONS, REQMOD, RESPMOD
- ✓ **ClamAV Integration** - Direct TCP communication
- ✓ **Multi-threaded** - Multiple simultaneous connections
- ✓ **Logging** - Detailed request/response logs
- ✓ **Version and author information** - Built-in metadata

### Docker Environment
- ✓ **ClamAV** - Current virus definitions
- ✓ **Python ICAP Server** - Minimal Alpine image (~50 MB)
- ✓ **Fast Build** - Seconds instead of minutes
- ✓ **No Dependencies** - Everything out of the box

## 🚀 Quick Start

### With Docker (Recommended)

> **💡 Note:** Use `docker compose` (new version) or `docker-compose` (old version).

```bash
# 1. Start containers
docker compose up -d
# or: docker-compose up -d

# 2. Check status (ClamAV needs ~2 min on first start)
docker compose logs -f
# or: docker-compose logs -f

# 3. Run tests
python3 icap_test.py --host localhost --port 1344 --service avscan --test-options
```

### Expected Result

```
✓ EICAR detection: PASSED - Threat correctly identified
✓ Clean file test: PASSED - File correctly identified as clean
```

## 📋 Prerequisites

- **Python 3.6+** for test script
- **Docker & Docker Compose** for server environment
- No additional dependencies (uses only Python standard library)

## Installation

```bash
# Clone repository
git clone <repository-url>
cd icap-test-script

# No additional dependencies required (uses only Python standard library)
```

## 📖 Usage

### Test Script

#### Basic Test

```bash
python3 icap_test.py --host localhost --port 1344 --service avscan
```

#### With OPTIONS Test

```bash
python3 icap_test.py --host localhost --port 1344 --service avscan --test-options
```

#### With Verbose Output

```bash
python3 icap_test.py --host localhost --port 1344 --service avscan --verbose
```

#### Show Version and Author

```bash
python3 icap_test.py --version
python3 icap_test.py --author
```

#### Parameter Overview

```bash
python3 icap_test.py \
  --host <hostname>        # ICAP server host (default: localhost)
  --port <port>            # ICAP server port (default: 1344)
  --service <service>      # ICAP service path (default: avscan)
  --test-options           # Send OPTIONS request first
  --verbose                # Show full response details
  --version                # Show version information
  --author                 # Show author information
```

### Docker Environment

#### Start Containers

```bash
# Start
docker compose up -d
# or: docker-compose up -d

# With rebuild (after code changes)
docker compose up -d --build
# or: docker-compose up -d --build

# Follow logs
docker compose logs -f
# or: docker-compose logs -f

# Check status
docker compose ps
# or: docker-compose ps
```

#### Stop Containers

```bash
# Stop
docker compose down
# or: docker-compose down

# Stop + remove volumes
docker compose down -v
# or: docker-compose down -v
```

## 📊 Example Output

```
ICAP Test Script
Target: icap://localhost:1344/avscan
============================================================

[1] Testing ICAP OPTIONS...
✓ OPTIONS request successful

[2] Testing EICAR virus test file...

============================================================
Test: EICAR Virus Test
============================================================
Filename: eicar.com
Status: ICAP/1.0 403 Forbidden
Threat Found: YES
Clean: NO
Details: Threat detected - file blocked | X-Virus-ID: Eicar-Test-Signature
============================================================

✓ EICAR detection: PASSED - Threat correctly identified

[3] Testing clean file...

============================================================
Test: Clean File Test
============================================================
Filename: clean.txt
Status: ICAP/1.0 204 No Modifications Needed
Threat Found: NO
Clean: YES
Details: No modification needed - file is clean
============================================================

✓ Clean file test: PASSED - File correctly identified as clean

============================================================
Test completed!
============================================================
```

## 🏗️ Architecture

The system consists of three components:

```
┌─────────────────────────────────────────┐
│         🖥️  HOST SYSTEM                 │
│    ┌──────────────────────────────┐    │
│    │   📄 icap_test.py            │    │
│    │ • Sends EICAR + Clean File   │    │
│    │ • Validates Responses        │    │
│    │ • OPTIONS, REQMOD, RESPMOD   │    │
│    └──────────────────────────────┘    │
└─────────────────────────────────────────┘
              ▼ TCP Port 1344
┌─────────────────────────────────────────┐
│      🐳 DOCKER: icap-server             │
│    ┌──────────────────────────────┐    │
│    │   🐍 icap_server.py          │    │
│    │ • ~280 lines Python          │    │
│    │ • ICAP/1.0 Protocol          │    │
│    │ • Multi-threaded Server      │    │
│    │ • ClamAV TCP/IP Client       │    │
│    └──────────────────────────────┘    │
└─────────────────────────────────────────┘
              ▼ TCP Port 3310
┌─────────────────────────────────────────┐
│        🐳 DOCKER: clamav                │
│    ┌──────────────────────────────┐    │
│    │   🦠 ClamAV Daemon           │    │
│    │ • Official Docker Image      │    │
│    │ • Auto-Updates               │    │
│    │ • INSTREAM Scanning          │    │
│    │ • Virus Definitions          │    │
│    └──────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### 📦 Component Details

| Component | Description | Technology |
|-----------|-------------|-----------|
| **icap_test.py** | Test client for ICAP server | Python 3.6+, Standard Library |
| **icap_server.py** | ICAP server with ClamAV integration | Python 3.11, Alpine Linux (~50 MB) |
| **ClamAV** | Antivirus engine | Official clamav/clamav image |

## 🎯 Advantages of This Solution

| Aspect | Advantage | Details |
|--------|-----------|---------|
| **Simplicity** | ✅ Pure Python | No C code, no complex builds |
| **Stability** | ✅ Few Dependencies | Only Python standard library + ClamAV |
| **Maintainability** | ✅ Clean Code | ~280 lines, well documented |
| **Performance** | ✅ Fast Build | Seconds instead of minutes |
| **Size** | ✅ Small Image | ~50 MB (Alpine-based) |
| **Flexibility** | ✅ Customizable | Easy to extend/modify |

## 🔧 Setting Up ICAP Server

### Option 1: Docker Compose (Recommended)

**✅ Best choice for quick start and testing:**

```bash
# Start containers
docker compose up -d
# or: docker-compose up -d

# Wait until ClamAV is ready (5-10 minutes on first start)
docker compose logs -f clamav
# or: docker-compose logs -f clamav

# Run tests
python3 icap_test.py --host localhost --port 1344 --service avscan
```

**See [DOCKER.md](DOCKER.md) for detailed instructions!**

### Option 2: Python Server Standalone

Start just the ICAP server (without Docker):

```bash
# ClamAV must be running separately
python3 icap_server.py
```

Server options:

```bash
python3 icap_server.py --version    # Show version
python3 icap_server.py --author     # Show author
python3 icap_server.py --host 0.0.0.0 --port 1344  # Custom host/port
```

### Option 3: External ICAP Server

If you already have an ICAP server or want to use a different one:

```bash
# Use only test script
python3 icap_test.py --host <your-icap-server> --port 1344 --service avscan
```

**Note:** The test script can run against any ICAP/1.0 compatible server.

## 🧪 EICAR Test File

The script uses the standard EICAR test file:

```
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
```

**Important:** This is **not a real virus**, but a harmless test signature recognized by all antivirus programs.

## ❗ Troubleshooting

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| **Connection refused** | ICAP server not reachable | `docker-compose ps` - check containers |
| **Connection timeout** | Server not responding | Check firewall, review logs |
| **ClamAV not ready** | Virus definitions still loading | Wait 2-5 min, check `docker-compose logs clamav` |
| **Empty response** | Wrong service URL | Verify service path (default: `avscan`) |

### Debug Commands

```bash
# Container status
docker compose ps
# or: docker-compose ps

# ICAP server logs
docker compose logs icap-server
# or: docker-compose logs icap-server

# ClamAV status
docker exec clamav clamdscan --version

# Manual ICAP test
echo -e "OPTIONS icap://localhost:1344/avscan ICAP/1.0\r\nHost: localhost\r\n\r\n" | nc localhost 1344
```

## 📁 Project Structure

```
icap-test-script/
├── icap_test.py              # Test client
├── icap_server.py            # Python ICAP server
├── docker-compose.yml        # Container orchestration
├── docker/
│   └── icap-server/
│       └── Dockerfile        # Server image
├── scripts/
│   └── create-release.py     # Release creation script
├── .github/
│   ├── ISSUE_TEMPLATE/       # Issue templates
│   └── workflows/            # GitHub Actions
├── README.md                 # This file (English)
├── README.de.md              # German version
└── DOCKER.md                 # Detailed Docker documentation
```

## 🔨 Advanced Customization

### Custom Test Files

Edit [icap_test.py](icap_test.py):

```python
# Add custom test file
CUSTOM_CONTENT = b"Your test content here"
success, status, response = client.send_request(
    CUSTOM_CONTENT, 
    'custom_test.txt'
)
```

### Extend ICAP Server

Edit [icap_server.py](icap_server.py):

```python
# E.g., add additional headers
def send_clean_response(self):
    response = (
        "ICAP/1.0 204 No Modifications Needed\r\n"
        "X-Custom-Header: MyValue\r\n"  # New
        "\r\n"
    )
```

### ClamAV Configuration

Custom ClamAV config in [docker-compose.yml](docker-compose.yml):

```yaml
clamav:
  environment:
    - CLAMAV_NO_FRESHCLAM=false  # Auto-updates
    - CLAMD_MAX_FILE_SIZE=100M   # Max file size
```

## 🎓 Additional Resources

- **ICAP RFC 3507:** https://tools.ietf.org/html/rfc3507
- **ClamAV Documentation:** https://docs.clamav.net/
- **Docker Details:** See [DOCKER.md](DOCKER.md)

## 📄 License

MIT License - Free to use for testing and development.

See [LICENSE](LICENSE) file for details.

## ✨ Credits

Created for ICAP functionality testing and virus scanner validation with a focus on simplicity and maintainability.

**Author:** Roland Imme  
**Version:** 1.1.9
