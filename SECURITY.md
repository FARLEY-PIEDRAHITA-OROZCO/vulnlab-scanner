# Security Policy - VulnLab Scanner

## Reporting Security Vulnerabilities

If you discover a security vulnerability in **VulnLab Scanner**, please follow these steps:

### 🔒 Responsible Disclosure
- **DO NOT** open a public GitHub issue for security vulnerabilities.
- Send details to: **security@vulnlab.com** (or create a private security advisory).
- We will respond within **48 hours**.

### What to Include
1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)
5. Your contact information

### Scope
This policy applies to:
- Vulnerabilities in VulnLab Scanner code
- Vulnerabilities in dependencies (we monitor via Dependabot)
- Configuration issues in the project

### Out of Scope
- Vulnerabilities in target applications scanned by VulnLab Scanner
- Social engineering attacks
- Physical security issues

## Security Best Practices for Users

### When Using VulnLab Scanner
- ✅ Only scan applications you **own** or have **explicit permission** to test
- ✅ Use in a controlled environment (staging, not production)
- ✅ Keep VulnLab Scanner updated (`pip install --upgrade vulnlab-scanner`)
- ✅ Review generated reports carefully before sharing
- ❌ Do NOT use for malicious purposes
- ❌ Do NOT scan third-party sites without authorization

### Configuration
- Store `.env` files securely and never commit them to version control
- Use strong passwords for authentication testing
- Limit rate of requests to avoid DoS (use `RATE_LIMIT` config)
- Review `DEFAULT_BRUTE_FORCE_PASSWORDS` before use

## Dependency Management
- We use **Dependabot** to automatically update dependencies
- Security updates are prioritized and released as patch versions
- Users should update promptly when security fixes are released

## Contact
- Security Email: security@vulnlab.com
- Maintainer: @FARLEY-PIEDRAHITA-OROZCO
- Project: https://github.com/FARLEY-PIEDRAHITA-OROZCO/vulnlab-scanner

## Acknowledgments
We thank all security researchers who responsibly disclose vulnerabilities to us.
