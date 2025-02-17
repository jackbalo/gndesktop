from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings  # Updated import
from PySide6.QtCore import QUrl
import os

class IndexPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.webview = QWebEngineView()
        # Enable local file access for CSS/JS files in relative paths
        self.webview.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
        index_html_path = os.path.join(base_path, 'index_desktop.html')
        self.webview.load(QUrl.fromLocalFile(index_html_path))
        layout.addWidget(self.webview)
        self.setLayout(layout)
