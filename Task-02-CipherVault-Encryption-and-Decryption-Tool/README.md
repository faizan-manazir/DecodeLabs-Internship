# 🔐 CipherVault

> A polished multi-technique encryption, decryption, encoding, and cryptography-learning toolkit built with Flask and Python.

CipherVault was designed as an educational cybersecurity application that lets users **compare multiple reversible techniques in one interface**, encrypt or decrypt text, understand how each method works, and distinguish historical ciphers from modern authenticated encryption.

> **Design decision:** Base64 is intentionally excluded from CipherVault's encryption techniques because it is an encoding format, not encryption. The Security Guide explains this distinction.

## ✨ Highlights

- 8 supported techniques
- Classical, key-based, modern, and encoding categories
- Encrypt/decrypt or encode/decode from one workspace
- Dedicated **How It Works** tab for every technique
- Algorithm steps, key requirements, examples, and security context
- AES-256-GCM authenticated encryption
- Fernet authenticated encryption
- Password-derived keys using **scrypt**
- Fresh random salts and nonces for modern encryption
- Versioned ciphertext packages for modern formats
- Input validation and safe generic server errors
- Privacy-conscious local operation history (metadata only)
- Copy, swap, clear, download, search, keyboard shortcuts
- Responsive desktop, tablet, and mobile GUI
- Automated unit and edge-case tests

---



## 🔗 Direct Source Code Link

CipherVault includes a highly visible **SOURCE CODE ↗** button in the application navigation.

Clicking it opens the project's repository directly in a new browser tab.

Before publishing the project, replace the placeholder repository URL in:

- `templates/index.html`
- `templates/learn.html`

Current placeholder:

```text
https://github.com/YOUR-USERNAME/CipherVault
```


## 🚀 Enhanced Features

### ⚖ Cipher Comparison Lab
Run the same input through multiple selected techniques and compare:

- Ciphertext output
- Output length
- Algorithm category
- Educational security context
- Individual key/password fields for every selected key-based technique
- Validation before the comparison is submitted

### 📖 Visual Algorithm Demonstrations
The **How It Works** tab now includes a visual representation for every technique, including:

- Caesar alphabet shifts
- Vigenère keyword alignment
- Atbash alphabet mirroring
- Rail Fence zig-zag layout
- XOR byte transformation
- Fernet key derivation flow
- AES-GCM encryption flow

### 🔑 Password Strength Meter
For modern password-based techniques, CipherVault checks:

- Length of at least 12 characters
- Lowercase letters
- Uppercase letters
- Numbers
- Special characters

This is an educational strength indicator, not a formal password-security guarantee.

### 📊 Encryption Statistics
After an operation, CipherVault displays:

- Input character count
- Output character count
- Percentage size change
- Browser-observed request time

### 🛡 Security Guide
A dedicated security comparison table helps users distinguish educational ciphers, encoding, and modern authenticated encryption.

---

## 🔬 Live Transformation Lab

After each encryption or decryption operation, CipherVault displays an interactive explanation of the current input:

- Caesar: character positions, shifts, calculations, and output
- Vigenère: aligned key characters and modular arithmetic
- Atbash: mirrored alphabet positions
- XOR: byte-level binary XOR operations
- Rail Fence: zig-zag rail placement
- Fernet and AES-256-GCM: technically accurate encryption pipelines rather than misleading character substitutions

The detailed visualization is limited to the first 60 characters for readability.

## 🧭 Supported Techniques

| Technique | Category | Key | Primary Use |
|---|---|---|---|
| Caesar Cipher | Classical | Numeric shift | Learn alphabet shifting |
| Vigenère Cipher | Classical | Keyword | Learn polyalphabetic substitution |
| Atbash Cipher | Classical | None | Learn fixed substitution |
| Rail Fence | Classical | Number of rails | Learn transposition |
| XOR | Key-Based | Secret key | Learn reversible byte transformation |
| Fernet | Modern | Password | Authenticated symmetric encryption |
| AES-256-GCM | Modern | Password | Confidentiality + tamper detection |

> ⚠️ Classical ciphers and repeating-key XOR are included for education and should not protect real sensitive data.

---

# 🧠 How Each Technique Works

## 1. Caesar Cipher

**Idea:** Shift each ASCII English letter by a fixed number.

**Encryption**
1. Read the numeric shift.
2. Convert each A–Z/a–z letter to its alphabet position.
3. Add the shift.
4. Wrap around using modulo 26.

**Decryption**
1. Use the same shift.
2. Move each letter backward by that shift.

**Example**

`HELLO` + shift `3` → `KHOOR`

---

## 2. Vigenère Cipher

**Idea:** Use a keyword to generate a different alphabet shift for each letter.

**Encryption**
1. Keep ASCII English letters from the keyword.
2. Repeat the keyword across the alphabetic characters of the message.
3. Convert each keyword letter to a shift from 0–25.
4. Shift each plaintext letter by its corresponding key value.

**Decryption**
1. Repeat the same keyword alignment.
2. Subtract the corresponding shift.

**Example**

`HELLO` + `KEY` → `RIJVS`

---

## 3. Atbash Cipher

**Idea:** Mirror the alphabet.

`A ↔ Z`, `B ↔ Y`, `C ↔ X`

**Working**
1. Replace each ASCII English letter with its opposite alphabet position.
2. Preserve case and non-letter characters.
3. Apply the same operation again to decrypt.

**Example**

`HELLO` → `SVOOL`

---

## 4. Rail Fence Cipher

**Idea:** Rearrange text using a zig-zag rail pattern.

**Encryption**
1. Choose the number of rails.
2. Write characters diagonally down and up across those rails.
3. Read the rails from top to bottom.

**Decryption**
1. Recreate the rail pattern.
2. Determine how many characters belong in each rail.
3. Reconstruct the original zig-zag order.

**Example**

With 3 rails:

`WEAREDISCOVEREDFLEEATONCE` → `WECRLTEERDSOEEFEAOCAIVDEN`

---

## 5. XOR Cipher

**Idea:** XOR each byte with a repeating key byte.

**Encryption**
1. Convert text and secret key to UTF-8 bytes.
2. Repeat the key across the message.
3. XOR each pair of bytes.

**Decryption**
2. XOR with the same key.
3. XOR reversibility restores the original bytes.

**Important:** Repeating-key XOR in this project is educational.

---

## 6. Fernet

**Idea:** Password-derived authenticated encryption.

**Encryption**
1. Generate a fresh random salt.
2. Use **scrypt** to derive a key from the password and salt.
3. Encrypt and authenticate the message with Fernet.
4. Package a version marker, salt, and token into URL-safe Base64.

**Decryption**
1. Decode the package.
2. Verify the format/version.
3. Recover the salt.
4. Derive the same key from the password.
5. Fernet verifies authenticity and decrypts the message.

A wrong password or modified ciphertext fails authentication.

---

## 7. AES-256-GCM

**Idea:** Modern authenticated encryption.

**Encryption**
1. Generate a fresh 16-byte salt.
2. Generate a fresh 12-byte GCM nonce.
3. Derive a 256-bit key from the password using **scrypt**.
4. Encrypt with AES-GCM.
5. Package a version marker + salt + nonce + authenticated ciphertext.
6. Encode the package with URL-safe Base64.

**Decryption**
1. Decode and validate the package.
2. Recover salt and nonce.
3. Derive the same key.
4. AES-GCM verifies integrity/authentication.
5. Return plaintext only if verification succeeds.

A wrong password or tampering causes decryption to fail.

---


## 1. Clone or extract the project

```bash
git clone <your-repository-url>
cd CipherVault
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment

Copy `.env.example` values into your deployment environment and set a strong `SECRET_KEY` for production.

## 5. Run

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 🧪 Testing

Run:

```bash
pytest -q
```

The test suite covers:

- Round-trip encryption/decryption
- Known-answer tests
- Wrong modern-encryption passwords
- Unicode preservation for ASCII-only classical processing
- Invalid Rail Fence keys

---

# 🔒 Security Notes

- Classical ciphers are educational.
- Repeating-key XOR is educational.
- Base64 is encoding, not encryption, and is intentionally not included as a CipherVault technique.
- Modern encryption uses established primitives from the `cryptography` library.
- Fernet and AES-GCM derive keys using scrypt and fresh random salts.
- AES-GCM uses a fresh nonce for every encryption.
- Modern ciphertext packages include format/version markers.
- Authentication failures do not reveal raw backend exception details.
- Browser history stores metadata only, not plaintext, ciphertext, keys, or passwords.
- If deployed remotely, submitted data is processed by the server. The UI should not be interpreted as a zero-knowledge or client-only encryption tool.

---

# 🎓 Project Context

CipherVault fulfills the core requirements of the DecodeLabs Project 2 brief by implementing reversible encryption/decryption logic, displaying encrypted and decrypted results, and expanding the basic exercise into a multi-technique educational toolkit. The project brief specifically allows a Caesar cipher or similar technique and encourages experimentation with user-selected keys and more complex ciphers. fileciteturn0file0L34-L48 fileciteturn0file0L87-L104

---

## Future Improvements

- Client-side WebCrypto mode for browser-only modern encryption
- Argon2id password derivation option
- File encryption mode
- Ciphertext format inspector
- Algorithm performance comparison
- Accessibility audit and high-contrast mode
- Docker deployment
- CI pipeline with automated tests

---

**CipherVault — Learn the logic. Compare the techniques. Understand the security.**
