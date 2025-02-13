import os
import re
from flask import current_app

def preprocess_text(text):
    text = re.sub(r'\s+', '', text)
    return text.upper()

def generate_key_order(key):
    key = key.upper()
    sorted_key = sorted(key)
    key_order = {char: i+1 for i, char in enumerate(sorted_key)}
    numbered_key = [key_order[char] for char in key]

    return numbered_key

def create_table(key, text):
    try:
        text = preprocess_text(text)
        key_order = generate_key_order(key)
        
        num_cols = len(key)
        num_rows = len(text) // num_cols
        remainder = len(text) % num_cols
        if remainder:
            num_rows += 1
        
        table = [["" for _ in range(num_cols)] for _ in range(num_rows + 2)]  # +2 for key rows
        
        # Insert key and numbering
        for i, char in enumerate(key):
            table[0][i] = char
            table[1][i] = str(key_order[i])
        
        # Fill table column-wise based on key numbering
        sorted_indices = sorted(range(num_cols), key=lambda i: key_order[i])
        index = 0
        for col in sorted_indices:
            for row in range(2, num_rows + 2):
                if row == num_rows + 1 and col >= remainder:
                    break
                if index < len(text):
                    table[row][col] = text[index]
                    index += 1
        
        return table
    except Exception as e:
        current_app.logger.error(f"Error creating decryption table: {e}")
        raise

def fill_table(table):
    filled_table = ""
    for row in table[2:]:  # Skip key rows
        filled_table += "".join(row)
    return filled_table


def replace_symbols(text):
    replacements = {
        'CLN': ':', 'SEMICLN': ';', 'XX': '.', 
        'CMM': ',', 'QUOTE': '"', 'APOSTROPHE': "'", 
        'BRACKETON': '(', 'BRACKETOFF': ')', 'OBLIQUE': '/', 
        'HYPHEN': '-'
    }
    for symbol, replacement in replacements.items():
        text = text.replace(symbol, replacement)

    return text

myscript_dir = os.path.dirname(os.path.abspath(__file__))
dictionary_path = os.path.join(myscript_dir, "dictionary.txt")

def load_dictionary(file_path):
    """Load dictionary from a file and return a set of words."""
    with open(file_path, "r", encoding="utf-8") as file:
        return set(word.strip() for word in file)

loaded_dictionary = load_dictionary(dictionary_path)

def add_spaces(extracted_text):
    words_found = []
    i = 0

    while i < len(extracted_text):
        match = None
        for j in range(len(extracted_text), i, -1):
            word = extracted_text[i:j]
            if word in loaded_dictionary:
                match = word
                i = j
                break

        if match:
            words_found.append(match)
        else:
            words_found.append(extracted_text[i])
            i += 1
    
    return " ".join(words_found)


def format_text(text):
    # Remove spaces before punctuation marks
    text = re.sub(r'\s+([.,;:/@)])', r'\1', text)
    # Remove spaces after '(' and '/'
    text = re.sub(r'([(/])\s+', r'\1', text)
    # Remove spaces between consecutive digits
    text = re.sub(r'(\d)\s+(?=\d)', r'\1', text)
    return text



def decrypt_text(text, key):
    try:
        preprocessed_text = preprocess_text(text)
        table = create_table(key, preprocessed_text)
        extracted_text = fill_table(table)
        symbol_replaced_text = replace_symbols(extracted_text)
        decrypted_text = add_spaces(symbol_replaced_text)
        formatted_decrypted_text = format_text(decrypted_text)
        
        return formatted_decrypted_text
    except ValueError as e:
        current_app.logger.error(f"Error during decryption: {e}")
        raise



'''
file = "/Users/blackbalo/downloads/balo.docx"
key = "blackcountry"

section = copy_section(file)
print(section)

preprocessed_text = preprocess_text(section)
print(preprocessed_text)

table = create_table(key, preprocessed_text)
print(table)

decrypted_text = decrypt_text(key, file)
print(decrypted_text)

'''