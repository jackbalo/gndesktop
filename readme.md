# 🔐 Playfair Text Encryption App

A PySide6-based desktop application for encryption and decryption utilizing a **12-column table-based cipher** for secure message encoding.

---

## 🚀 Features

- **Encrypt Messages**: Secure text using a **12-letter key**.
- **Decrypt Messages**: Retrieve original text using the same key.
- **User-Friendly UI**: Clean desktop interface with **dark mode**.
- **Document Handling**: Upload and download encrypted/decrypted documents.

---

## 🛠️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/jackbalo/gndesktop.git
cd playfair

2️⃣ Install Dependencies

Make sure you have Python 3+ installed, then run:

pip install -r requirements.txt

3️⃣ Run the Application

python app.py

The application will open as a desktop window.

---

📂 Project Structure

📁 gndesktop/
│── 📄 app.py                # Main application entry point
│── 📄 main_window.py        # Main window setup and navigation
│── 📂 encryption_app/
│   │── 📄 __init__.py       # Package initialization
│   │── 📄 pages.py          # UI pages for encryption, decryption, and results
│   │── 📄 encrypt.py        # Encryption logic
│   │── 📄 decrypt.py        # Decryption logic
│   │── 📄 file_helpers.py   # File handling utilities
│── 📂 static/               # Static assets (CSS & images)
│   │── 📄 styles.qss        # Styling
│   │── 📄 logo.png          # Application logo
│── 📄 requirements.txt      # Required dependencies
│── 📄 README.md             # Project documentation


---

🔑 How It Works

🔒 Encryption

1️⃣ Enter your plaintext message or upload a document.
2️⃣ Provide a 12-letter key (alphabets only).
3️⃣ The app arranges text column-wise and extracts it row-wise.
4️⃣ The encrypted text is displayed and can be downloaded.

🔓 Decryption

1️⃣ Enter the encrypted text or upload a document.
2️⃣ Use the same key for decryption.
3️⃣ The app reconstructs the table and extracts the original message.


---

📜 Code Breakdown

🔹 app.py (Application Entry Point)

Initializes the QApplication.

Creates and shows the main window.


🔹 main_window.py (Main Window)

Sets up the main window and navigation.

Handles menu and toolbar actions.

Manages page transitions.


🔹 pages.py (UI Pages)

Defines the encryption, decryption, and result pages.

Handles user inputs and displays results.


🔹 encrypt.py (Encryption Logic)

encrypt_text(): Encrypts the plaintext using the provided key.


🔹 decrypt.py (Decryption Logic)

decrypt_text(): Decrypts the encrypted text using the provided key.


🔹 file_helpers.py (File Handling Utilities)

allowed_doc_file(): Checks if the file is a valid document.

copy_section(): Copies text from a document.

replace_section(): Replaces text in a document.

create_document(): Creates a new document.

duplicate_document(): Duplicates a document.

delete_file(): Deletes a file after a specified delay.


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

🔹 Encryption Page

Form to enter plaintext and key.

Displays encrypted text and allows document download.


🔹 Decryption Page

Form to enter encrypted text and key.

Displays decrypted text and allows document download.


🔹 Result Page

Displays the result of encryption or decryption.

Allows downloading the result as a document.


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

🔥 Built with PySide6 | Python🚀

