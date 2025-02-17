from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QScrollArea, QFileDialog, QDialog
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
        
        self.text_label = QLabel("Text:")
        self.text_input = QTextEdit()
        
        self.key_label = QLabel("Key:")
        self.key_input = QLineEdit()
        
        self.encrypted_label = QLabel("Encrypted Text:")
        self.encrypted_output = QTextEdit()
        self.encrypted_output.setReadOnly(True)
        
        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_text)
        
        self.upload_button = QPushButton("Upload Document")
        self.upload_button.clicked.connect(self.upload_file)
        
        self.download_button = QPushButton("Download Encrypted Document")
        self.download_button.clicked.connect(self.download_file)
        
        self.go_to_decryption_button = QPushButton("Go to Decryption")
        self.go_to_decryption_button.clicked.connect(self.main_window.show_decryption_page)
        
        layout.addWidget(self.text_label)
        layout.addWidget(self.text_input, stretch=3)  # Make text input larger
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input, stretch=1)  # Make key input smaller
        layout.addWidget(self.upload_button)
        layout.addWidget(self.encrypt_button)
        '''layout.addWidget(self.encrypted_label)
        layout.addWidget(self.encrypted_output)
        layout.addWidget(self.download_button)
        layout.addWidget(self.go_to_decryption_button)
        '''
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll_area.setWidget(container)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
    
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
            self.main_window.show_output_page("Encrypted Text", encrypted_text, self.duplicate_file_path)
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
        
        self.text_label = QLabel("Encrypted Text:")
        self.text_input = QTextEdit()
        
        self.key_label = QLabel("Key:")
        self.key_input = QLineEdit()
        
        self.decrypted_label = QLabel("Decrypted Text:")
        self.decrypted_output = QTextEdit()
        self.decrypted_output.setReadOnly(True)
        
        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_text)
        
        self.upload_button = QPushButton("Upload Document")
        self.upload_button.clicked.connect(self.upload_file)
        
        self.download_button = QPushButton("Download Decrypted Document")
        self.download_button.clicked.connect(self.download_file)
        
        self.go_to_encryption_button = QPushButton("Go to Encryption")
        self.go_to_encryption_button.clicked.connect(self.main_window.show_encryption_page)
        
        layout.addWidget(self.text_label)
        layout.addWidget(self.text_input, stretch=3)  # Make text input larger
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input, stretch=1)  # Make key input smaller
        layout.addWidget(self.upload_button)
        layout.addWidget(self.decrypt_button)
        '''layout.addWidget(self.decrypted_label)
        layout.addWidget(self.decrypted_output)
        layout.addWidget(self.download_button)
        layout.addWidget(self.go_to_encryption_button)
        '''
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll_area.setWidget(container)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
    
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
            self.main_window.show_output_page("Decrypted Text", decrypted_text, self.duplicate_file_path)
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
