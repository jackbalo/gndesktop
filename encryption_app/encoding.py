import re
import math

def prepare_text(text):
    # Define punctuation replacements
    replacements = {
        ':': 'CLN', ';': 'SEMICLN', '.': 'XX', ',': 'CMM', 
        '"': 'QUOTE...UNQUOTE', "'": 'APOSTROPHE', 
        '(': 'BRACKETON', ')': 'BRACKETOFF', '/':'OBLIQUE', '-':'HYPHEN'
    }
    
    spelled_out_replacements = {
        r'\bcolon\b': 'CLN', r'\bsemicolon\b': 'SEMICLN', 
        r'\bcomma\b': 'CMM', r'\bquote unquote\b': 'QUOTE...UNQUOTE', 
        r'\bparen\b': 'BRACKETON', r'\bunparen\b': 'BRACKETOFF'
    }
    
    # Convert text to uppercase and remove spaces
    text = re.sub(r'\s+', '', text)
    text = text.upper()
    
    # Replace punctuation symbols
    for symbol, replacement in replacements.items():
        text = text.replace(symbol, replacement)
    
    # Replace spelled-out punctuation (whole words only)
    for word, replacement in spelled_out_replacements.items():
        text = re.sub(word, replacement, text, flags=re.IGNORECASE)

    return text


def create_encryption_table(key):
    if len(key) != 12 or not key.isalpha():
        return None, "Key must be exactly 12 letters long and contain only alphabets."
    
    key = key.upper()
    table = [list(key)]
    sorted_key = sorted(key)
    key_rank = {char: i + 1 for i, char in enumerate(sorted_key)}
    
    # Create numbered key based on ranks
    numbered_key = [key_rank[char] for char in key]
    table.append(numbered_key)
    
    return table, None


def fill_encryption_table(table, text):
    num_chars = len(text)
    table = list(table)
    # Calculate required extra 'X' padding
    remainder = num_chars % 5
    if remainder > 0:
        text += 'X' * (5 - remainder)  # Pad with up to 4 'X' to make it a multiple of 5

    num_rows = math.ceil(len(text) / 12)  # Calculate required rows
    filled_rows = [list(text[i:i + 12]) for i in range(0, len(text), 12)]  # Fill table rows


    table.extend(filled_rows)  # Add filled rows to the table

    return table


def extract_encoded_text(table):
    if not table or len(table) < 2:
        raise ValueError("Invalid table format. Ensure encryption table is properly created.")
    key_numbers = table[1]  # Second row contains key numbering
    text_columns = table[2:]  # Exclude key and numbering rows

    if key_numbers is None:
        raise ValueError("Key numbering row is missing or invalid.")
    
    # Sort columns based on key numbering order
    sorted_columns = sorted(enumerate(key_numbers), key=lambda x: x[1])

    # Extract text column-wise based on sorted key order
    extracted_text = []
    for col_index, _ in sorted_columns:
        for row in text_columns:
            if col_index < len(row):  # Ensure we don't go out of bounds
                extracted_text.append(row[col_index])

    # Group into sets of five
    grouped_text = ["".join(extracted_text[i:i+5]) for i in range(0, len(extracted_text), 5)]
    num_groups = len(grouped_text)  # Count the number of word groups
    
    return " ".join(grouped_text), num_groups  # Return the encoded text and the count of word groups


def encrypt_text(text, key):
    try:
        prepared_text = prepare_text(text)

        table, error = create_encryption_table(key)
        if error:
            return error
        
        filled_table = fill_encryption_table(table, prepared_text)
        extracted_text, num_groups = extract_encoded_text(filled_table)
        return extracted_text, num_groups  # Return both the encoded text and the count of word groups
    except ValueError as e:
        return str(e)
