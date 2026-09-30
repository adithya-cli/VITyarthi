"""
Password Manager Project for VITarthi
Made by: S. Adithya Narayanan
Date: 27-09-26
REG no - 26BEC10082

A simple password manager that encrypts your passwords and keeps them safe.
"""

import os
import json
import hashlib
import secrets
import string
import getpass
import requests
from encryption import make_key, encrypt_data, decrypt_data


class PasswordManager:
    def __init__(self):
        self.vault_file = "vault.enc"
        self.key = None
        self.passwords = {}
    
    # creates a new vault file
    def create_new_vault(self, master_pass):
        print("Creating new vault...")
        
        # create random bytes once and save them with this vault
        vault_random_bytes = os.urandom(16)
        
        self.key = make_key(master_pass, vault_random_bytes)
        self.passwords = {}
        
        self.save_vault(vault_random_bytes)
        print("Vault created successfully!")
    
    # opens an existing vault
    def open_vault(self, master_pass):
        if not os.path.exists(self.vault_file):
            print("Error: no vault file found!")
            return False
            
        try:
            f = open(self.vault_file, 'rb')
            vault_random_bytes = f.read(16)
            encrypted_stuff = f.read()
            f.close()
            
            self.key = make_key(master_pass, vault_random_bytes)
            
            decrypted = decrypt_data(encrypted_stuff, self.key)
            json_text = decrypted.decode()
            self.passwords = json.loads(json_text)
            
            print("Vault unlocked!")
            return True
            
        except:
            print("Error: wrong password or corrupted vault file")
            return False
    
    # saves the vault to disk
    def save_vault(self, vault_random_bytes):
        json_text = json.dumps(self.passwords, indent=2)
        json_data = json_text.encode()
        
        encrypted = encrypt_data(json_data, self.key)
        
        f = open(self.vault_file, 'wb')
        f.write(vault_random_bytes)
        f.write(encrypted)
        f.close()
    
    # add a password to the vault
    def add_new_password(self, service, username, password):
        self.passwords[service] = {
            "username": username,
            "password": password
        }
        
        f = open(self.vault_file, 'rb')
        vault_random_bytes = f.read(16)
        f.close()
        
        self.save_vault(vault_random_bytes)
        print(f"Password for {service} saved!")
    
    # gets a password from the vault
    def get_password(self, service):
        if service in self.passwords:
            entry = self.passwords[service]
            username = entry['username']
            password = entry['password']
            return username, password
        else:
            return None, None
    
    # lists all the services we have passwords for
    def show_all_services(self):
        if len(self.passwords) == 0:
            print("No passwords stored yet")
            return
        
        print("\nYour stored services:")
        print("---------------------")
        for service in self.passwords:
            username = self.passwords[service]['username']
            print(f"  - {service} ({username})")
        print("---------------------")
    
    # removes a password
    def delete_password(self, service):
        if service in self.passwords:
            del self.passwords[service]
            
            f = open(self.vault_file, 'rb')
            vault_random_bytes = f.read(16)
            f.close()
            
            self.save_vault(vault_random_bytes)
            print(f"Deleted password for {service}")
        else:
            print(f"No password found for {service}")
    
    # generates a random password
    def generate_strong_password(self, length=16, symbols=True):
        characters = string.ascii_letters + string.digits
        if symbols:
            characters = characters + string.punctuation
        
        password = ''
        for i in range(length):
            next_character = secrets.choice(characters)
            password = password + next_character
        
        return password
    
    # checks if a password has been in a data breach using the haveibeenpwned API
    def check_if_breached(self, password):
        password_bytes = password.encode()
        hash_result = hashlib.sha1(password_bytes)
        password_hash = hash_result.hexdigest()
        password_hash = password_hash.upper()
        
        first_five = password_hash[:5]
        remaining_hash = password_hash[5:]
        
        url = f"https://api.pwnedpasswords.com/range/{first_five}"
        
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                lines = response.text.split('\n')
                for line in lines:
                    parts = line.split(':')
                    if len(parts) == 2:
                        hash_part = parts[0].strip()
                        count_text = parts[1].strip()
                        count = int(count_text)
                        
                        if hash_part == remaining_hash:
                            return True, count
                
                return False, 0
            else:
                print("Could not check breach status (API error)")
                return None, 0
                
        except:
            print("Could not check breach status (network error)")
            return None, 0


def show_menu():
    print("\n" + "="*40)
    print("Password Manager")
    print("="*40)
    print("1. Add a new password")
    print("2. Get a password")
    print("3. List all services")
    print("4. Delete a password")
    print("5. Generate random password")
    print("6. Check if password is breached")
    print("7. Exit")
    print("="*40)


def main():
    manager = PasswordManager()
    
    print("\nWelcome to Password Manager!")
    print()
    
    if os.path.exists("vault.enc"):
        print("Found existing vault")
        master = getpass.getpass("Enter your master password: ")
        
        if not manager.open_vault(master):
            print("Exiting...")
            return
    else:
        print("No vault found. Let's create a new one.")
        print("Don't forget this password. There is no recovery option.")
        
        while True:
            master = getpass.getpass("Create a master password: ")
            confirm = getpass.getpass("Confirm master password: ")
            
            if master == confirm:
                manager.create_new_vault(master)
                break
            else:
                print("Passwords don't match. Try again.")
    
    while True:
        show_menu()
        choice = input("\nWhat do you want to do? (1-7): ")
        
        if choice == "1":
            print("\n--- Add new password ---")
            service = input("Enter service name (e.g. Gmail, Facebook): ")
            username = input("Enter username/email: ")
            
            generate_answer = input("Generate a password? (y/n): ")
            generate_answer = generate_answer.lower()
            if generate_answer == 'y':
                length_input = input("Enter password length (default 16): ")
                if length_input.isdigit():
                    length = int(length_input)
                else:
                    length = 16
                    
                password = manager.generate_strong_password(length)
                print(f"Generated password: {password}")
            else:
                password = getpass.getpass("Enter password: ")
            
            manager.add_new_password(service, username, password)
            
        elif choice == "2":
            print("\n--- Get password ---")
            service = input("Enter service name: ")
            saved_entry = manager.get_password(service)
            username = saved_entry[0]
            password = saved_entry[1]
            
            if password:
                print(f"\nService: {service}")
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print(f"No password found for {service}")
        
        elif choice == "3":
            manager.show_all_services()
        
        elif choice == "4":
            print("\n--- Delete password ---")
            service = input("Enter service name: ")
            confirm = input(f"Delete the password for {service}? (y/n): ")
            confirm = confirm.lower()
            if confirm == 'y':
                manager.delete_password(service)
        
        elif choice == "5":
            print("\n--- Generate password ---")
            length_input = input("Enter length (default 16): ")
            if length_input.isdigit():
                length = int(length_input)
            else:
                length = 16
            
            symbols_answer = input("Include symbols? (y/n): ")
            symbols_answer = symbols_answer.lower()
            if symbols_answer == 'n':
                use_symbols = False
            else:
                use_symbols = True
            
            password = manager.generate_strong_password(length, use_symbols)
            print(f"\nGenerated password: {password}")
        
        elif choice == "6":
            print("\n--- Check password breach ---")
            password = getpass.getpass("Enter password to check: ")
            print("Checking...")
            
            check_result = manager.check_if_breached(password)
            password_found = check_result[0]
            count = check_result[1]
            
            if password_found == True:
                print(f"\nWarning: this password has been breached!")
                print(f"It appeared {count:,} times in data breaches.")
                print("Do not use this password!")
            elif password_found == False:
                print("\nThis password was not found in the breach database.")
            
        elif choice == "7":
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Enter a number from 1-7")


if __name__ == "__main__":
    main()
