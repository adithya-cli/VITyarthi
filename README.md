# 🔐 Secure Password Manager

A CLI-based password manager with encryption and breach checking capabilities.

## Features

**Master password protection** - Single password unlocks your entire vault  
**Breach checking** - Integrates with HaveIBeenPwned API to check compromised passwords  
**Strong password generator** - Creates cryptographically secure random passwords  
**Secure storage** - Encrypted vault file and works offline
**Easy to use** - Simple CLI interface for all operations  

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the password manager:

```bash
python password_manager.py
```

### First Time Setup

When you run it for the first time, you'll be prompted to create a master password. This password encrypts your entire vault, so:

- **Choose a strong master password**
- **Don't forget it** (there's no recovery option)
- **Don't reuse it anywhere else**

### Main Menu Options

1. **Add new password** - Store credentials for a service
2. **Get password** - Retrieve stored credentials
3. **List all services** - View all stored service names
4. **Delete password** - Remove a password entry
5. **Generate strong password** - Create random secure passwords
6. **Check password breach status** - Verify if a password has been compromised
7. **Exit** - Lock and exit the vault

## How It Works

### Encryption
- Uses **PBKDF2** with 100,000 iterations to derive encryption key from master password
- Random 16-byte salt for each vault (prevents rainbow table attacks)
- **Fernet** symmetric encryption (AES-128 in CBC mode with HMAC)

### Breach Checking
- Uses HaveIBeenPwned's k-anonymity API
- Only sends first 5 characters of password hash
- Your actual password **never** leaves your machine

## Security Notes

**Important Security Considerations:**

1. **Master password is critical** - If lost, your passwords are unrecoverable
2. **Keep vault.enc safe** - This file contains all your passwords (encrypted)
3. **Don't share vault.enc** - Even encrypted, it's sensitive data
4. **Backup vault.enc** - Store encrypted backup in safe location

## Example Usage

### Adding a password
```
Service name: Gmail
Username/Email: adithya@xyz.com
Generate password? (y/n): y
Password length: 20
Generated password: aB9$mK2#pL7&qR3@wX5
✓ Password for 'Gmail' saved!
```

### Checking a breach
```
Enter password to check: password123
Checking breach status...
WARNING: This password has been breached 9,545,824 times!
   Do NOT use this password!
```

## Requirements

- Python
- cryptography module
- requests module

## Future Enhancements (Possible in later versions)

- GUI version with tkinter or PyQt
- Export/import functionality
- Search functionality for large vaults
- Password strength analyzer
- Password expiry reminder
