# 🔐 Playfair Text Encryption App

A Flask-based encryption and decryption web application utilizing a **12-column table-based cipher** for secure message encoding.

---

## 🚀 Features

- **Encrypt Messages**: Secure text using a **12-letter key**.
- **Decrypt Messages**: Retrieve original text using the same key.
- **User-Friendly UI**: Clean web interface with **dark mode**.
- **Flask Backend**: Handles encryption and decryption securely.

---

## 🛠️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/jackbalo/playfair.git
cd playfair

2️⃣ Install Dependencies

Make sure you have Python 3+ installed, then run:

pip install -r requirements.txt

3️⃣ Run the Application

flask run

The application will be available at:
➡️ http://127.0.0.1:5000/


---

📂 Project Structure

📁 playfair-cipher-app/
│── 📄 app.py                # Main Flask application
│── 📄 config.py             # Configuration settings
│── 📂 encryption_app/
│   │── 📄 __init__.py       # Package initialization
│   │── 📄 routes.py         # Flask routes (handles encryption & decryption)
│   │── 📄 decoding.py       # Decryption logic
│   │── 📄 helpers.py        # Encryption utilities
│── 📂 templates/            # HTML templates
│   │── 📄 layout.html       # Base template
│   │── 📄 index.html        # Home page
│   │── 📄 encrypt.html      # Encryption page
│   │── 📄 decrypt.html      # Decryption page
│── 📂 static/               # Static assets (CSS & JS)
│   │── 📄 styles.css        # Styling
│   │── 📄 script.js         # Dark mode toggle
│── 📄 requirements.txt      # Required dependencies
│── 📄 README.md             # Project documentation


---

🔑 How It Works

🔒 Encryption

1️⃣ Enter your plaintext message.
2️⃣ Provide a 12-letter key (alphabets only).
3️⃣ The app arranges text column-wise and extracts it row-wise.
4️⃣ The encrypted text is grouped into sets of five characters.

🔓 Decryption

1️⃣ Enter the encrypted text.
2️⃣ Use the same key for decryption.
3️⃣ The app reconstructs the table and extracts the original message.


---

📜 Code Breakdown

🔹 app.py (Flask Entry Point)

Initializes the Flask app.

Loads configurations.

Registers the blueprint (routes.py).

Ensures no-cache policy for responses.


🔹 routes.py (Flask Routes)

Defines the index, encryption, and decryption routes.

Processes form inputs.

Calls encrypt_text() and decrypt_text() functions.


🔹 helpers.py (Encryption Utilities)

prepare_text(): Formats text, replacing special characters.

create_encryption_table(): Builds the table with key ranking.

fill_encryption_table(): Organizes text into the 12-column format.

extract_encoded_text(): Extracts the encrypted message in 5-character groups.


🔹 decoding.py (Decryption Logic)

preprocess_text(): Formats text before processing.

generate_key_order(): Numbers the key alphabetically.

create_table(): Reconstructs the 12-column table.

extract_text(): Retrieves the original message.



---

📜 Example Usage

Encryption

Input:

Message: HELLO WORLD
Key: PLAYFAIRCIPHER

Output:


Decryption

Input:

Message: 
Key: PLAYFAIRCIPHER

Output:

HELLO WORLD


---

🎨 User Interface

🔹 index.html

Home page with an overview of encryption and decryption.


🔹 encrypt.html

Form to enter plaintext and key.

Displays encrypted text.


🔹 decrypt.html

Form to enter encrypted text and key.

Displays decrypted text.


🔹 layout.html

Navigation bar for encryption/decryption.

Dark mode toggle.



---

🌟 Future Improvements

✅ User authentication for secure message storage.
✅ Implement alternative encryption algorithms.
✅ Deploy as a web service.


---

🤝 Contributing

Feel free to submit issues or open pull requests. 🚀


---

📜 License

This project is licensed under the MIT License.


---

🔥 Built with Flask | HTML | CSS | JavaScript

This README integrates all components of your project cohesively, making it easy for others to understand, install, and use. Let me know if you need modifications! 🚀

