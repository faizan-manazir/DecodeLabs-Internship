# 🔐 DecodeLabs Cyber Security Internship

A collection of practical cybersecurity projects completed during the **DecodeLabs Cyber Security Industrial Training Program**. This repository documents hands-on work across password security, cryptography, Windows host security assessment, vulnerability identification, security hardening concepts, and technical documentation.

---

## 📌 Internship Project Progress

| Task | Project | Focus | Status |
|---|---|---|---|
| **Task 1** | 🔐 Password Security Analyzer | Password strength analysis & security assessment | ✅ Completed |
| **Task 2** | 🔐 CipherVault — Multi-Technique Encryption & Decryption Lab | Classical & modern cryptography | ✅ Completed |
| **Task 3** | 🛡️ System Vulnerability Checklist Audit | Windows host security & blue-team assessment | ✅ Completed |

---

# 🔐 Task 1 — Password Security Analyzer

**Official Project:** Password Strength Checker  
**Advanced Project Title:** Password Security Analyzer

A Python-based password analysis application that evaluates password characteristics, detects predictable patterns, estimates entropy and guess time, assigns a security score, and provides recommendations for stronger passwords.

### 🔎 Core Analysis

- Password length analysis
- Uppercase, lowercase, number and special-character detection
- Password strength classification
- Security score from 0–100
- Common-password detection
- Common-password variation detection
- Repeated-character detection
- Sequential-pattern detection
- Keyboard-pattern detection
- Entropy estimation
- Illustrative password guess-time estimation
- Personalized security recommendations

### 🖥️ Interfaces

- Modern graphical interface using CustomTkinter
- Command-line interface using hidden password input
- Password visibility controls
- Live character counter
- Animated security score
- Character-composition visualization
- Detailed security checklist

### 🧪 Testing

The project includes unit testing for password characteristics, common passwords, repeated/sequential patterns, strength classification, and score boundaries.

### 🛠️ Technologies

- Python 3
- CustomTkinter
- Regular Expressions (`re`)
- Mathematics (`math`)
- `getpass`
- `unittest`

[➡️ Open Task 1](Task-01-Password-Strength-Checker/)

---

# 🔐 Task 2 — CipherVault

**Project:** CipherVault — Multi-Technique Encryption & Decryption Lab

An interactive **Python/Flask cryptography application** combining classical ciphers, key-based transformations, and modern authenticated encryption in one cybersecurity-focused workspace.

### ✨ Main Features

- Encrypt/decrypt workspace
- Dynamic algorithm and key selection
- Input validation and operation feedback
- Copy and clear functionality
- How It Works learning section
- Live Transformation Lab
- Cipher Comparison Lab
- Encryption statistics
- Password-strength feedback for password-based techniques
- Security Guide
- Direct source-code link

### 🧩 Supported Techniques

| Technique | Category | Key Required | Security Context |
|---|---|---:|---|
| Caesar Cipher | Classical | Yes | Educational |
| Vigenère Cipher | Classical | Yes | Educational |
| Atbash Cipher | Classical | No | Educational |
| Rail Fence Cipher | Classical | Yes | Educational |
| XOR Cipher | Key-Based | Yes | Educational / Demonstration |
| Fernet | Modern | Yes | Authenticated Encryption |
| AES-256-GCM | Modern | Yes | Authenticated Encryption |

The project intentionally distinguishes educational ciphers from modern authenticated encryption. **Base64 is not presented as encryption** because it is an encoding mechanism rather than a confidentiality mechanism.

### 🔬 Transformation & Comparison Labs

CipherVault can visualize algorithm-specific transformations such as character shifts, Vigenère key alignment, Atbash mapping, XOR byte operations, Rail Fence paths, and high-level modern-encryption pipelines. The Comparison Lab allows multiple techniques to be evaluated side by side.

### 🧰 Technology Stack

- Python
- Flask
- `cryptography`
- HTML5
- CSS3
- Vanilla JavaScript
- Pytest

[➡️ Open Task 2](Task-02-CipherVault-Encryption-and-Decryption-Tool/)

---

# 🛡️ Task 3 — System Vulnerability Checklist Audit

**Official Project:** System Vulnerability Checklist  
**Assessment Type:** Windows Host Security Audit  
**Platform:** DecodeLabs Cyber Security Industrial Training Program

A practical **blue-team endpoint security assessment** performed on a Windows 10 Pro system using PowerShell and built-in Windows security utilities.

### 🎯 Assessment Areas

The audit covered four major security domains:

1. **Identity & Authentication**
2. **Software & Patch Management**
3. **Human & Physical Security**
4. **Network & Endpoint Hygiene**

### 🔍 Assessment Methodology

```text
Baseline Assessment
        ↓
Methodical Inspection
        ↓
Risk Identification & Prioritization
        ↓
Remediation Planning
        ↓
Hardened-State Verification
```

### 🚨 Findings

The assessment documented **10 security findings**:

- **4 High-severity findings**
- **6 Medium-severity findings**

The findings covered password-policy weaknesses, account lockout configuration, local administrator privileges, operating-system and software lifecycle concerns, workstation-lock enforcement, AutoPlay configuration, and BitLocker status.

### 🛡️ Existing Security Controls Verified

The assessment also verified existing controls including:

- Built-in Administrator account disabled
- Guest account disabled
- Microsoft Defender enabled
- Real-time Protection enabled
- Behavior Monitoring enabled
- UAC enabled with Secure Desktop
- Windows Firewall enabled across Domain, Private and Public profiles
- Defender signatures updated
- Display timeout configured

### 🛠️ Assessment Tools

```powershell
Get-LocalUser
Get-LocalGroupMember
net accounts
Get-HotFix
Get-ComputerInfo
Get-MpComputerStatus
Get-ItemProperty
powercfg /query
Get-Disk
Get-NetFirewallProfile
Get-BitLockerVolume
manage-bde -status
```

### 📄 Deliverables

- One-page vulnerability report
- Evidence screenshots from the four assessment areas
- Documented findings and severity classification
- Remediation recommendations
- Verification requirements

[➡️ Open Task 3](Task-03-System-Vulnerability-Checklist/)

---

# 📊 Skills & Security Concepts Demonstrated

### 🔐 Security Assessment

- Vulnerability assessment
- Host security auditing
- Risk identification and prioritization
- Security-control verification
- Security documentation

### 🛡️ Blue-Team / Defensive Security

- Windows endpoint security
- Authentication and access control
- Password-policy analysis
- Account lockout assessment
- Local privilege assessment
- Microsoft Defender verification
- Windows Firewall verification
- Disk-encryption assessment
- Physical-security controls

### 🔑 Cryptography & Application Security

- Password security analysis
- Entropy estimation
- Classical cryptography
- Key-based transformations
- Authenticated encryption
- AES-256-GCM
- Fernet
- Secure coding concepts
- Input validation

### 💻 Technical Skills

- Python
- Flask
- PowerShell
- CustomTkinter
- HTML/CSS/JavaScript
- `cryptography`
- Pytest / unittest
- Git & GitHub
- Technical reporting

---

# 📂 Repository Structure

```text
DecodeLabs-Internship/
│
├── README.md
│
├── Task-01-Password-Strength-Checker/
│   ├── README.md
│   ├── password_analyzer.py
│   ├── guess_time_estimator.py
│   ├── password_checker_cli.py
│   ├── password_checker_gui.py
│   ├── requirements.txt
│   ├── data/
│   │   └── common_passwords.txt
│   └── screenshots/
│       ├── weak_password.png
│       ├── medium_password.png
│       ├── strong_password.png
│       ├── very_strong_password.png
│       └── cli.png
│
├── Task-02-CipherVault-Encryption-and-Decryption-Tool/
│   ├── README.md
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── algorithms/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── tests/
│   └── screenshots/
│
└── Task-03-System-Vulnerability-Checklist/
    ├── README.md
    ├── System_Vulnerability_Report.pdf
    └── evidence/
        ├── S1-01.png
        ├── S1-02.png
        ├── S1-03.png
        ├── S1-04.png
        ├── S2-01.png
        ├── S2-02.png
        ├── S2-03.png
        ├── S2-04.png
        ├── S2-05.png
        ├── S3-01.png
        ├── S3-02.png
        ├── S3-03.png
        ├── S3-04.png
        ├── S3-05.png
        ├── S3-06.png
        └── S3-07.png
```

---

# 🎓 Internship Outcomes

Across the three projects, the internship work progressed from **password-security analysis**, through **cryptographic application development**, to **host-level vulnerability assessment and defensive security verification**.

The repository therefore demonstrates both **development-oriented cybersecurity skills** and **practical blue-team/security-assessment skills**, supported by source code, screenshots, tests, and technical documentation.

---

# ⚠️ Disclaimer

All projects in this repository were developed for **educational and authorized cybersecurity training purposes** as part of the DecodeLabs Cyber Security Industrial Training Program.

Security testing, vulnerability assessment, and cryptographic experimentation should only be performed on systems, applications, and networks that you own or are explicitly authorized to assess.

---

### 🔐 Learn • Build • Analyze • Secure

**DecodeLabs Cyber Security Internship — Practical Projects Portfolio**