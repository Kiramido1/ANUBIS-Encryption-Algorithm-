# ANUBIS Encryption Algorithm (Simplified)

**Description**  
ANUBIS is a custom symmetric encryption algorithm built in Python. It encrypts English text by converting it to Egyptian Hieroglyphs, mapping them to Unicode, applying key-dependent permutation, modular transformation, and circular bit shifts, and outputs a hexadecimal string. Decryption reverses all steps using the same key.

**Features**
- Symmetric encryption with a user-defined key
- Multi-layered encryption: Unicode, permutation, modular math, and bit manipulation
- Hexadecimal output for storage or transmission
- Simple Python implementation for educational purposes

**Usage**
1. Run the script:  
python anubis.py

Choose an option:

Encrypt

Decrypt

Enter your text and key

Receive ciphertext (hex) or decrypted plaintext

Example

Encrypt: hello
Key: secret
Output (hex): 191D13A21F000C92...


Developer:
Mohamed Ahmed Fekry
Omar Tarek El-Shafie

Note
This is a simplified educational implementation. Not intended for production use or sensitive data encryption.
