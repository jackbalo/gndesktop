import re
import math

def preprocess_text(text):
    # First remove any whitespace and convert to uppercase
    text = re.sub(r'\s+', '', text.upper())
    
    # Remove the date-time stamp pattern that appears at the end
    text = re.sub(r'\d{6}Z/[A-Z]{3}/\d{2}$', '', text)
    
    return text

def start_prepare_text(text):
    # Define punctuation replacements
    replacements = {
        ':': 'CLN', ';': 'SEMICLN', ',': 'CMM', '?': 'QUES',
        '"': 'QUOTE', "“":'QUOTE', "”":'QUOTE', "‘":'QUOTE',
        "'": 'APOSTROPHE', "’":"APOSTROPHE",'!': 'EXCLAMATION',
        '/':'OBLIQUE', '(.)':'XX', '-':'HYPHEN', "–":"HYPHEN", "—":"HYPHEN", "—":"HYPHEN"
    }
    
    spelled_out_replacements = {
        r'\bcolon\b': 'CLN', r'\bsemicolon\b': 'SEMICLN', 
        r'\bcomma\b': 'CMM', r'\bparen\b': 'BRACKETON', 
        r'\bunparen\b': 'BRACKETOFF'
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


def prepare_text(text):
    # Define punctuation replacements
    text = start_prepare_text(text)

    replacements = {
        '(': 'BRACKETON', ')': 'BRACKETOFF', '.': 'XX'
    }
    
    spelled_out_replacements = {
        r'\bcolon\b': 'CLN', r'\bsemicolon\b': 'SEMICLN', 
        r'\bcomma\b': 'CMM', r'\bparen\b': 'BRACKETON', 
        r'\bunparen\b': 'BRACKETOFF'
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
        raise ValueError("Key must be exactly 12 letters long and contain only alphabets.")
    
    key = key.upper()
    table = [list(key)]
    sorted_key = sorted(key)
    key_rank = {char: i + 1 for i, char in enumerate(sorted_key)}
    
    # Create numbered key based on ranks
    numbered_key = [key_rank[char] for char in key]
    table.append(numbered_key)
    
    return table

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

    # Group into sets of five, five groups per line
    grouped_text = ["".join(extracted_text[i:i+5]) for i in range(0, len(extracted_text), 5)]
    lines = ["     ".join(grouped_text[i:i+5]) for i in range(0, len(grouped_text), 5)]
    formatted_text = "\n".join(lines)
    
    num_groups = len(grouped_text) # Count the number of word groups
    
    return f"GR: {num_groups}\n{formatted_text}", num_groups

def encrypt_text(text, key):
    try:
        processed_text = preprocess_text(text)
        prepared_text = prepare_text(processed_text)
        table = create_encryption_table(key)
        filled_table = fill_encryption_table(table, prepared_text)
        extracted_text, num_groups = extract_encoded_text(filled_table)
        return extracted_text  # Return only the encoded text
    except ValueError as e:
        raise
    except Exception as e:
        raise




'''
Test
text = 'REST’D(.)The Egyptians called their country Kemet, meaning black land. The name refers to the rich black mud without which the people could not have survived.'

key = "blackcountry"

now = encrypt_text(text, key)
print(prepare_text(text))
print(now)
'''