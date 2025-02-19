from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QScrollArea, QFileDialog, QDialog, QGroupBox, QGridLayout
from encryption_app.encrypt import encrypt_text
from encryption_app.decrypt import decrypt_text
from encryption_app.file_helpers import allowed_doc_file, copy_section, replace_section, create_document, duplicate_document, delete_file
import os
import shutil
from encryption_app.pages_web_index import IndexPage

class ResultPage(QWidget):
    def __init__(self, main_window, title, content, file_path):
        super().__init__()
        self.main_window = main_window
        self.title = title
        self.content = content
        self.file_path = file_path
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        result_label = QLabel(self.title)
        result_text = QTextEdit()
        result_text.setPlainText(self.content)
        result_text.setReadOnly(True)
        
        download_button = QPushButton("Download Document")
        download_button.clicked.connect(self.download_file)
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.main_window.show_index_page)
        
        layout.addWidget(result_label)
        layout.addWidget(result_text)
        layout.addWidget(download_button)
        layout.addWidget(back_button)
        
        self.setLayout(layout)
    
    def download_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Word Documents (*.docx);;All Files (*)", options=options)
        if file_name:
            shutil.copy(self.file_path, file_name)
            QMessageBox.information(self, "Download Complete", "File has been saved successfully.", QMessageBox.Ok, QMessageBox.Ok)

IndexPage = IndexPage

class EncryptionPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.uploaded_file_path = None
        self.duplicate_file_path = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Group box for file upload
        file_group = QGroupBox()
        file_layout = QVBoxLayout()
        self.upload_button = QPushButton("Upload Plaintext Document")
        self.upload_button.clicked.connect(self.upload_file)
        file_layout.addWidget(self.upload_button)
        file_group.setLayout(file_layout)
        
        # Group box for encryption inputs
        input_group = QGroupBox()
        input_layout = QGridLayout()
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Copy and Paste PlainText Message in here or Upload Document above!!")
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter encryption key")
        input_layout.addWidget(QLabel("Plaintext Message:"), 0, 0)
        input_layout.addWidget(self.text_input, 0, 1)
        input_layout.addWidget(QLabel("Key:"), 1, 0)
        input_layout.addWidget(self.key_input, 1, 1)
        input_group.setLayout(input_layout)
        
        # Group box for encryption actions
        action_group = QGroupBox()
        action_layout = QVBoxLayout()
        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_text)
        self.go_to_decryption_button = QPushButton("Go to Decryption")
        self.go_to_decryption_button.clicked.connect(self.main_window.show_decryption_page)
        action_layout.addWidget(self.encrypt_button)
        action_layout.addWidget(self.go_to_decryption_button)
        action_group.setLayout(action_layout)
        
        layout.addWidget(file_group)
        layout.addWidget(input_group)
        layout.addWidget(action_group)
        
        self.encrypted_output = QTextEdit()  # Add this line
        self.encrypted_output.setReadOnly(True)
        #layout.addWidget(self.encrypted_output)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll_area.setWidget(container)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        
        # Set background color for the main layout
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;  /* Darker background color */
            }
            QGroupBox {
                background-color: #34495e;  /* Slightly lighter background for group boxes */
                border: 1px solid #2c3e50;
                border-radius: 5px;
                margin-top: 10px;
            }
            QLabel {
                color: white;
            }
            QLineEdit, QTextEdit {
                background-color: #ecf0f1;
                color: black;
                border: 1px solid #34495e;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 1px solid #2980b9;
                border-radius: 5px;
                padding: 10px 20px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
    
    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Word Documents (*.docx);;All Files (*)")
        if file_name and allowed_doc_file(file_name):
            self.uploaded_file_path = file_name
            self.duplicate_file_path = duplicate_document(file_name)
            plaintext = copy_section(self.duplicate_file_path)
            self.text_input.setPlainText(plaintext)
    
    def encrypt_text(self):
        key = self.key_input.text()
        text = self.text_input.toPlainText()
        if not key or not text:
            QMessageBox.warning(self, "Input Error", "Please provide both key and text.", QMessageBox.Ok, QMessageBox.Ok)
            return
        try:
            encrypted_text = encrypt_text(text, key)  # Only one value is returned
            self.encrypted_output.setPlainText(encrypted_text)
            if self.duplicate_file_path:
                replace_section(self.duplicate_file_path, encrypted_text)
                delete_file(self.duplicate_file_path, 600)
            self.main_window.show_output_page("Encrypted Message", encrypted_text, self.duplicate_file_path)
        except Exception as e:
            QMessageBox.critical(self, "Encryption Error", str(e), QMessageBox.Ok, QMessageBox.Ok)
    
    def download_file(self):
        if self.duplicate_file_path:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Word Documents (*.docx);;All Files (*)", options=options)
            if file_name:
                shutil.copy(self.duplicate_file_path, file_name)
                QMessageBox.information(self, "Download Complete", "File has been saved successfully.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Download Error", "No file to download. Please encrypt a document first.", QMessageBox.Ok, QMessageBox.Ok)

class DecryptionPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.uploaded_file_path = None
        self.duplicate_file_path = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Group box for file upload
        file_group = QGroupBox()
        file_layout = QVBoxLayout()
        self.upload_button = QPushButton("Upload Encrypted Document")
        self.upload_button.clicked.connect(self.upload_file)
        file_layout.addWidget(self.upload_button)
        file_group.setLayout(file_layout)
        
        # Group box for decryption inputs
        input_group = QGroupBox()
        input_layout = QGridLayout()
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Copy and Paste Encrypted Message Text in here or Upload Document above!!")
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter decryption key")
        input_layout.addWidget(QLabel("Encrypted Text:"), 0, 0)
        input_layout.addWidget(self.text_input, 0, 1)
        input_layout.addWidget(QLabel("Key:"), 1, 0)
        input_layout.addWidget(self.key_input, 1, 1)
        input_group.setLayout(input_layout)
        
        # Group box for decryption actions
        action_group = QGroupBox()
        action_layout = QVBoxLayout()
        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_text)
        self.go_to_encryption_button = QPushButton("Go to Encryption")
        self.go_to_encryption_button.clicked.connect(self.main_window.show_encryption_page)
        action_layout.addWidget(self.decrypt_button)
        action_layout.addWidget(self.go_to_encryption_button)
        action_group.setLayout(action_layout)
        
        layout.addWidget(file_group)
        layout.addWidget(input_group)
        layout.addWidget(action_group)
        
        self.decrypted_output = QTextEdit()  # Add this line
        self.decrypted_output.setReadOnly(True)
        #layout.addWidget(self.decrypted_output)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll_area.setWidget(container)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        
        # Set background color for the main layout
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;  /* Darker background color */
            }
            QGroupBox {
                background-color: #34495e;  /* Slightly lighter background for group boxes */
                border: 1px solid #2c3e50;
                border-radius: 5px;
                margin-top: 10px;
            }
            QLabel {
                color: white;
            }
            QLineEdit, QTextEdit {
                background-color: #ecf0f1;
                color: black;
                border: 1px solid #34495e;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 1px solid #2980b9;
                border-radius: 5px;
                padding: 10px 20px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
    
    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Word Documents (*.docx);;All Files (*)")
        if file_name and allowed_doc_file(file_name):
            self.uploaded_file_path = file_name
            self.duplicate_file_path = duplicate_document(file_name)
            encrypted_text = copy_section(self.duplicate_file_path)
            self.text_input.setPlainText(encrypted_text)
    
    def decrypt_text(self):
        key = self.key_input.text()
        text = self.text_input.toPlainText()
        if not key or not text:
            QMessageBox.warning(self, "Input Error", "Please provide both key and text.", QMessageBox.Ok, QMessageBox.Ok)
            return
        try:
            decrypted_text = decrypt_text(text, key)
            self.decrypted_output.setPlainText(decrypted_text)
            if self.duplicate_file_path:
                replace_section(self.duplicate_file_path, decrypted_text)
                delete_file(self.duplicate_file_path, 600)
            self.main_window.show_output_page("Decrypted Message", decrypted_text, self.duplicate_file_path)
        except Exception as e:
            QMessageBox.critical(self, "Decryption Error", str(e), QMessageBox.Ok, QMessageBox.Ok)
    
    def download_file(self):
        if self.duplicate_file_path:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Word Documents (*.docx);;All Files (*)", options=options)
            if file_name:
                shutil.copy(self.duplicate_file_path, file_name)
                QMessageBox.information(self, "Download Complete", "File has been saved successfully.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Download Error", "No file to download. Please decrypt a document first.", QMessageBox.Ok, QMessageBox.Ok)
