"""
Secure Password Generator
Generates strong random passwords and copies to clipboard
"""
import secrets
import string
import pyperclip

def generate_password(length=16, use_symbols=True, use_numbers=True, use_uppercase=True, use_lowercase=True):
    """Generate a secure random password"""
    
    characters = ""
    
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    
    if not characters:
        characters = string.ascii_letters + string.digits
    
    # Generate password
    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    return password

def main():
    # Generate password
    password = generate_password(16)
    
    print(f"Generated Password: {password}")
    
    # Copy to clipboard
    try:
        pyperclip.copy(password)
        print("(Copied to clipboard)")
    except:
        print("(Could not copy to clipboard)")

if __name__ == "__main__":
    main()
