# Project Statement

## Problem Statement

People struggle to maintain unique, strong passwords for every online service they use. Reusing passwords means one breach can compromise multiple accounts, while writing them down in plain text (notes, spreadsheets, unencrypted files) leaves credentials exposed if someone gains access to the storage location.

Most users also lack an easy way to:
- Generate truly random passwords
- Check if their existing passwords have already appeared in known data breaches
- Store credentials securely without relying on cloud services or complex setup

This project addresses these problems by providing a **local, encrypted password vault** with master-password access, secure random password generation, and privacy-preserving breach checks.

---

## Scope of the Project

**In scope:**
- Single-user local password vault with encrypted storage (`vault.enc`)
- Master password-based authentication using PBKDF2 key derivation
- CRUD operations: add, retrieve, list, and delete credentials
- Secure random password generation (configurable length and character sets)
- Privacy-preserving breach checking via HaveIBeenPwned API (k-anonymity model)
- Command-line interface (CLI) for all operations
- Cross-platform Python implementation (Windows, macOS, Linux)

**Out of scope:**
- Graphical user interface (GUI)
- Browser integration or autofill
- Cloud sync or multi-device support
- Multi-user access or shared vaults
- Password recovery or account reset mechanisms
- Mobile app versions
- Two-factor authentication (2FA) storage

---

## Target Users

**Primary user:**
- Individual who wants to manage their own credentials from a terminal on a trusted device
- Comfortable with command-line tools
- Values local storage over cloud-based solutions
- Has basic Python environment setup skills

**Use cases:**
- Developers managing API keys, database credentials, and service accounts
- Privacy-conscious users who prefer local data storage
- Anyone learning about password security and cryptography
- Users who need offline credential access (internet only required for breach checks)

---

## High-Level Features

### 1. Encrypted Local Vault
- Credentials stored as encrypted JSON in a local file (`vault.enc`)
- **PBKDF2-SHA256** key derivation from master password + random salt
- **Fernet (symmetric encryption)** for authenticated encryption
- Tamper detection: rejects modified or corrupted vault files

### 2. Master Password Authentication
- Single master password unlocks the entire vault
- Password hidden during input (using `getpass`)
- First-run setup creates new vault with user-chosen master password
- Existing vault requires correct master password to decrypt

### 3. Credential Management (CRUD)
- **Add**: Store service name, username, and password
- **Retrieve**: Look up credentials by service name
- **List**: View all stored service names
- **Delete**: Remove credentials by service name

### 4. Random Password Generation
- Generates cryptographically secure random passwords using Python's `secrets` module
- Configurable length (default: 16 characters)
- Optional symbol inclusion (letters, digits, punctuation)
- Can be saved directly to vault or copied separately

### 5. Breach Detection
- Checks if a password appears in the **HaveIBeenPwned Pwned Passwords** database
- Uses **k-anonymity model**: only sends first 5 characters of SHA-1 hash
- Returns breach count if found, or confirms password is not in known breaches
- Graceful failure handling for network issues

### 6. Command-Line Interface
- Simple numbered menu system
- Clear prompts and error messages
- Hidden password input for security
- Runs entirely in terminal (no GUI dependencies)

### 7. Offline Operation
- All credential operations work without internet
- Only breach checking requires network access
- Vault remains functional even if breach API is unavailable
