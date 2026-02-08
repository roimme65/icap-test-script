# Security Policy

## 🛡️ Supported Versions

This project currently supports the following versions for security updates:

| Version | Status | Security Updates | End of Life |
|---------|--------|------------------|------------|
| 1.1.x | ✅ Active | Yes | TBD |
| 1.0.x | ⚠️ Maintenance | Limited | 2026-01-31 |
| < 1.0 | ❌ Unsupported | No | Expired |

## 📋 Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in this project, please follow these guidelines:

### ⚠️ Please DO NOT

- ❌ Do not open a public GitHub issue for security vulnerabilities
- ❌ Do not post the vulnerability details on social media
- ❌ Do not disclose the vulnerability before we have time to fix it

### ✅ Please DO

1. **Report through GitHub Security Advisory** (Recommended)
   - Go to: Settings → Security → Report a vulnerability
   - This creates a private discussion with the maintainers
   - We'll acknowledge your report within 24-48 hours

2. **Email Security Report** (Alternative)
   - Send detailed information to the project maintainers
   - Include: Description, Severity, Reproduction Steps, Impact Assessment

### 📝 What to Include

When reporting a vulnerability, please provide:

```markdown
## Vulnerability Report

**Type:** [e.g., Command Injection, Information Disclosure]
**Severity:** [Critical / High / Medium / Low]
**CVSS Score:** [if available]

### Description
Clear description of the vulnerability...

### Reproduction Steps
1. Step 1...
2. Step 2...
3. Step 3...

### Impact
What could an attacker do with this vulnerability?

### Proof of Concept
```python
# If safe to share without compromising security
```

### Expected Behavior
What should happen instead?

### Actual Behavior
What currently happens?

### Environment
- Python Version: [e.g., 3.8, 3.11]
- OS: [e.g., Linux, macOS, Windows]
- ICAP Server Version: 1.1.x

### Additional Context
Any other relevant information...
```

## 🔍 Security Considerations

### Known Limitations

1. **EICAR Test File**
   - The EICAR string is encoded in hex and split into parts at runtime
   - This is for zero-trust environments but not cryptographically secure
   - Never use for real malware distribution

2. **Communication Protocol**
   - ICAP communication is unencrypted (RFC 3507 standard)
   - Implement TLS/encryption at your network layer if needed
   - Use only in trusted networks or with VPN

3. **ClamAV Integration**
   - Relies on ClamAV's security stance
   - Keep ClamAV updated for latest virus definitions
   - Docker image auto-updates by default (can be disabled)

4. **Python Standard Library**
   - Uses only Python standard library for compatibility
   - Regularly update Python version for security patches

### Security Best Practices

When using this project:

- **Update Regularly:** Keep all components (Python, ClamAV, Docker) updated
- **Network Isolation:** Run in isolated networks or with firewall rules
- **Principle of Least Privilege:** Run containers with minimal required permissions
- **Input Validation:** Don't trust file content; always validate with antivirus
- **Logging:** Monitor logs for suspicious activity
- **TLS/Encryption:** Add encryption layer for network communication
- **Secret Management:** Never commit credentials or secrets

## 🔧 Security Measures in Place

### Code Security

- ✅ String encoding (Hex for EICAR test string)
- ✅ Input validation in ICAP request parsing
- ✅ Exception handling to prevent information leakage
- ✅ No execution of untrusted code (ast.parse instead of exec)
- ✅ No external dependencies (reduces attack surface)

### Process Security

- ✅ GitHub Actions with workflow validation
- ✅ Python syntax checking in CI/CD
- ✅ Version verification at release time
- ✅ Release notes requirement
- ✅ Protected main branch

### Deployment Security

- ✅ Alpine Linux base image (minimal attack surface)
- ✅ ClamAV in isolated Docker container
- ✅ Non-root user option available
- ✅ Official ClamAV image (regularly updated)

## 🔄 Vulnerability Response Timeline

We aim to follow this timeline for security issues:

| Phase | Timeframe | Action |
|-------|-----------|--------|
| **Report Received** | 0h | Acknowledge receipt |
| **Initial Assessment** | 24-48h | Determine severity |
| **Fix Development** | 3-7 days | Create patch |
| **Testing** | 2-3 days | Comprehensive testing |
| **Release** | 7-14 days | Release security update |
| **Disclosure** | 7-14 days | Public announcement |

**Note:** Timelines may vary based on complexity. Critical issues get priority.

## 🔐 Dependency Security

### Current Dependencies

- **Python Standard Library Only** (test script)
- **Docker Official Images Only** (ClamAV, Alpine)
- **GitHub Actions** (security verified actions only)

### No External Python Packages

This project intentionally avoids external Python dependencies to:
- Reduce attack surface
- Minimize dependency vulnerabilities
- Ensure reproducibility
- Simplify deployment

## 📚 Additional Resources

- **ICAP Protocol (RFC 3507):** https://tools.ietf.org/html/rfc3507
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **ClamAV Security:** https://www.clamav.net/
- **Python Security:** https://python.readthedocs.io/en/latest/library/security_warnings.html

## 🙏 Credits

Thank you to everyone who responsibly reports security vulnerabilities and helps us maintain a secure project.

---

**Last Updated:** February 8, 2026  
**Current Version:** 1.1.x  
**Security Policy Version:** 1.0
