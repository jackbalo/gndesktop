from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QScrollArea


class IndexPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        text_container = QWidget()
        text_layout = QVBoxLayout()
        
        self.header = QLabel("<h1 style='text-align: center;'>Welcome to GNCipher</h1>")
        self.header.setStyleSheet("color: white; font-size: 20px;")
        
        self.description = QLabel(
            "<div style='text-align: justify;'>GNCipher encodes and decodes classified messages using Playfair cipher algorithm.<p>It ensures your messages remain confidential.</p></div>"
        )
        self.description.setStyleSheet("color: silver; font-size: 18px;")
        
        text_layout.addWidget(self.header)
        text_layout.addWidget(self.description)
        text_container.setLayout(text_layout)
        
        steps_card = QGroupBox()
        steps_layout = QVBoxLayout()
        
        self.encryption_steps = QLabel("<p><h2>Encryption Steps</h2></<p><ol><li>Enter your plaintext message in the text input field.</li><li>Provide a secure encryption key.</li><li>Click the 'Encrypt' button to generate the encrypted text.</li><li>Download the encrypted document if needed.</li></ol>")
        self.encryption_steps.setStyleSheet("color: silver; text-align: center; font-size: 18px;")
        
        self.decryption_steps = QLabel("<p><h2>Decryption Steps</h2></<p><ol><li>Enter the encrypted message in the text input field.</li><li>Provide the corresponding decryption key.</li><li>Click the 'Decrypt' button to reveal the original message.</li><li>Download the decrypted document if needed.</li></ol>")
        self.decryption_steps.setStyleSheet("color: silver; text-align: center; font-size: 18px;")
        
        steps_layout.addWidget(self.encryption_steps)
        steps_layout.addWidget(self.decryption_steps)
        steps_card.setLayout(steps_layout)
        steps_card.setStyleSheet("background-color: #2c3e50; border: 1px solid #white; border-radius: 2px; padding: 0 auto;")
        
        layout.addWidget(text_container)
        layout.addWidget(steps_card)
        
        self.footer = QLabel('&copy; 2025 GNCipher. All rights reserved. This app is open source. <a href="https://github.com/jackbalo/gndesktop.git" target="_blank" style="color: #3498db; text-decoration: none;">GitHub Repository</a>')
        self.footer.setStyleSheet("color: #999; text-align: center; margin-top: 20px; font-size: 12px;")
        
        layout.addWidget(self.footer)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll_area.setWidget(container)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;  /* Darker background color */
                border: 1px solid white;  /* White border for the container */
            }
            QGroupBox {
                background-color: #34495e;  /* Slightly lighter background for group boxes */
                border: 1px solid white;  /* White border for the group boxes */
                border-radius: 5px;
                margin-top: 10px;
            }
            QLabel {
                color: silver;
            }
        """)
