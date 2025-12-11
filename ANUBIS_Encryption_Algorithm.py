# -----------------------------------------
#   ANUBIS Encryption Algorithm (Simplified)
# -----------------------------------------

import binascii

# ------------------------------
# 1) Basic English → Hieroglyph map
# ------------------------------
english_to_hiero = {
    "a": "𓂝", "b": "𓃀", "c": "𓍿", "d": "𓂧",
    "e": "𓇋", "f": "𓆑", "g": "𓎼", "h": "𓎛",
    "i": "𓇋", "j": "𓆓", "k": "𓎡", "l": "𓃭",
    "m": "𓅓", "n": "𓈖", "o": "𓅱", "p": "𓊪",
    "q": "𓈎", "r": "𓂋", "s": "𓋴", "t": "𓏏",
    "u": "𓅱", "v": "𓆑", "w": "𓅱", "x": "𓐍",
    "y": "𓇌", "z": "𓊃"
}

# Reverse map (Hieroglyph → English)
hiero_to_english = {v: k for k, v in english_to_hiero.items()}

MAX_HIERO = 0x1342F   # Highest Egyptian Hieroglyph Unicode code point


# --------------------------------------------------
# Utility: Circular Right Shift for encryption
# --------------------------------------------------
def circular_right_shift(num, shift, bits=18):
    b = format(num, f'0{bits}b')
    shift %= bits
    return int(b[-shift:] + b[:-shift], 2)


# --------------------------------------------------
# Utility: Circular Left Shift for decryption
# --------------------------------------------------
def circular_left_shift(num, shift, bits=18):
    b = format(num, f'0{bits}b')
    shift %= bits
    return int(b[shift:] + b[:shift], 2)


# --------------------------------------------------
# Step 1: English → Hieroglyph
# --------------------------------------------------
def english_to_hieroglyphs(text):
    return "".join(english_to_hiero[c] for c in text.lower() if c in english_to_hiero)


# --------------------------------------------------
# Step 2: Hieroglyph → Unicode list
# --------------------------------------------------
def hieroglyphs_to_unicode(htext):
    return [ord(ch) for ch in htext]


# --------------------------------------------------
# Step 3: Key-dependent permutation
# --------------------------------------------------
def apply_permutation(unicode_list, key):
    key_nums = [ord(k) for k in key]
    sorted_key = sorted(list(set(key_nums)))
    rank = [sorted_key.index(k) for k in key_nums]  # position map

    # Ensure ranks do NOT repeat (if key has duplicate letters)
    # If duplicates exist, add index to make unique
    for i in range(len(rank)):
        rank[i] = rank[i] + i/1000

    ranked_positions = sorted(range(len(rank)), key=lambda x: rank[x])
    return [unicode_list[i] for i in ranked_positions]


# --------------------------------------------------
# Step 4: Modular Transformation
# --------------------------------------------------
def modular_transform(unicode_list, key):
    key_nums = [ord(k) for k in key]
    out = []

    for i, u in enumerate(unicode_list):
        k = key_nums[i % len(key_nums)]
        out.append((u + k) % MAX_HIERO)

    return out


# --------------------------------------------------
# Step 5: Circular Bit Shift (Right)
# --------------------------------------------------
def apply_bit_shift(enc_list, key):
    shift = sum(ord(c) for c in key) % 16  # small shift
    return [circular_right_shift(u, shift) for u in enc_list]


# --------------------------------------------------
# Step 6: Convert to Hex output
# --------------------------------------------------
def to_hex_string(enc_list):
    return "".join(f"{x:05X}" for x in enc_list)


# ------------------------------
#             ENCRYPT
# ------------------------------
def encrypt(text, key):
    h = english_to_hieroglyphs(text)
    u = hieroglyphs_to_unicode(h)
    p = apply_permutation(u, key)
    m = modular_transform(p, key)
    b = apply_bit_shift(m, key)
    return to_hex_string(b)


# ------------------------------
#  DECRYPT — reverse steps
# ------------------------------
def decrypt(hex_string, key):
    # Split hex into chunks of 5 digits
    unicode_list = [int(hex_string[i:i+5], 16) for i in range(0, len(hex_string), 5)]

    # Reverse Step 5 (Right shift → Left shift)
    shift = sum(ord(c) for c in key) % 16
    step5 = [circular_left_shift(u, shift) for u in unicode_list]

    # Reverse Step 4
    key_nums = [ord(k) for k in key]
    step4 = []
    for i, v in enumerate(step5):
        k = key_nums[i % len(key_nums)]
        step4.append((v - k) % MAX_HIERO)

    # Reverse Step 3 (undo permutation)
    key_nums = [ord(k) for k in key]
    sorted_key = sorted(list(set(key_nums)))
    rank = [sorted_key.index(k) for k in key_nums]
    for i in range(len(rank)):
        rank[i] = rank[i] + i/1000
    ranked_positions = sorted(range(len(rank)), key=lambda x: rank[x])

    # Undo:
    original = [None] * len(step4)
    for new_i, old_i in enumerate(ranked_positions):
        original[old_i] = step4[new_i]

    # Unicode → Hieroglyph
    hiero = "".join(chr(u) for u in original)

    # Hieroglyph → English
    return "".join(hiero_to_english.get(ch, "?") for ch in hiero)


# -----------------------------
# MAIN Program (Menu)
# -----------------------------
while True:
    print("\n===== ANUBIS Encryption System =====")
    print("1) Encrypt")
    print("2) Decrypt")
    print("3) Exit")
    choice = input("Choose: ")

    if choice == "1":
        msg = input("Enter message: ")
        key = input("Enter key: ")
        print("\nEncrypted Hex:")
        print(encrypt(msg, key))

    elif choice == "2":
        cipher = input("Enter hex string: ")
        key = input("Enter key: ")
        print("\nDecrypted Message:")
        print(decrypt(cipher, key))

    elif choice == "3":
        break

    else:
        print("Invalid choice!")