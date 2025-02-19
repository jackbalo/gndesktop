import os
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMenuBar, QFileDialog, QMessageBox, QToolBar, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import Qt  # Add this import
from encryption_app.pages_web_index import IndexPage  # New import for web index page
from encryption_app.pages import EncryptionPage, DecryptionPage, ResultPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 100, 800, 700)
        self.setMinimumSize(800, 500)

        
        # Enable window resizing using restore, maximize, and minimize buttons
        self.setWindowFlags(Qt.Window)
        
        # Set the window icon
        icon_path = os.path.join(os.path.dirname(__file__), 'static', 'comms.ico')
        self.setWindowIcon(QIcon(icon_path))
        
        self.central_widget = QStackedWidget()
        
        self.index_page = IndexPage()  # Use WebIndexPage instead of previous IndexPage
        self.encryption_page = EncryptionPage(self)
        self.decryption_page = DecryptionPage(self)
        self.result_page = None
        
        self.central_widget.addWidget(self.index_page)
        self.central_widget.addWidget(self.encryption_page)
        self.central_widget.addWidget(self.decryption_page)
        
        self.create_menu_bar()  # Ensure this method is called
        self.create_tool_bar()
        
        self.apply_stylesheet()
        self.setup_main_layout()  # Setup main layout with logo and central widget
    
    def create_menu_bar(self):
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        file_menu = self.menu_bar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = self.menu_bar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def create_tool_bar(self):
        self.tool_bar = QToolBar("Main Toolbar")
        
        home_action = QAction("Home", self)
        home_action.triggered.connect(self.show_index_page)
        self.tool_bar.addAction(home_action)
        
        encryption_action = QAction("Encryption", self)
        encryption_action.triggered.connect(self.show_encryption_page)
        self.tool_bar.addAction(encryption_action)
        
        decryption_action = QAction("Decryption", self)
        decryption_action.triggered.connect(self.show_decryption_page)
        self.tool_bar.addAction(decryption_action)
    
    def show_about_dialog(self):
        QMessageBox.about(self, "About GNCipher", "GNCipher is a desktop application for encryption and decryption.")
    
    def show_index_page(self):
        self.central_widget.setCurrentWidget(self.index_page)
        self.setWindowTitle("GNCipher")
        self.setMenuBar(self.menu_bar)
    
    def show_encryption_page(self):
        self.central_widget.setCurrentWidget(self.encryption_page)
        self.setWindowTitle("Encryption")
        self.setMenuBar(self.menu_bar)
    
    def show_decryption_page(self):
        self.central_widget.setCurrentWidget(self.decryption_page)
        self.setWindowTitle("Decryption")
        self.setMenuBar(self.menu_bar)
    
    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                content = file.read()
                self.encryption_page.text_input.setPlainText(content)
    
    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                content = self.encryption_page.text_input.toPlainText()
                file.write(content)
                
    def show_output_page(self, title, content, file_path):
        self.result_page = ResultPage(self, title, content, file_path)
        self.central_widget.addWidget(self.result_page)
        self.central_widget.setCurrentWidget(self.result_page)
        self.setWindowTitle(title)
        self.setMenuBar(self.menu_bar)
    
    def apply_stylesheet(self):
        stylesheet_path = os.path.join(os.path.dirname(__file__), 'static', 'styles.qss')
        with open(stylesheet_path, 'r') as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)
    
    def setup_main_layout(self):
        main_layout = QVBoxLayout()
        
        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'static', 'comms.png'))
        logo_label.setPixmap(logo_pixmap.scaled(50, 50))
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(logo_label)
        top_layout.addStretch()
        top_layout.addWidget(self.tool_bar)
        
        main_layout.addLayout(top_layout)
        main_layout.addSpacing(10)  # Reduce the vertical space
        main_layout.addWidget(self.central_widget)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
