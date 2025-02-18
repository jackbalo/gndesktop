from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QSizePolicy
from PySide6.QtCore import Qt
import os

class IndexPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Load HTML template from file and render using QTextEdit
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
        index_html_path = os.path.join(base_path, 'index_desktop.html')
        try:
            with open(index_html_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                # Add inline CSS to set text color to silver and ensure full height
                html_content = f"<style>body {{ color: silver; height: 100vh; overflow: hidden; }}</style>{html_content}"
        except Exception as e:
            html_content = f"<html><body style='color: silver; height: 100vh; overflow: hidden;'><p>Error loading template: {e}</p></body></html>"
        self.text_edit.setHtml(html_content)
        
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
