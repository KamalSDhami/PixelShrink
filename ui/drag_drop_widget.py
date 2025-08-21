from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
import os

class DragDropWidget(QListWidget):
    files_dropped = Signal(int)  # Signal to emit when files are dropped
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setAlternatingRowColors(True)
        self.drag_active = False
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #3498db;
                border-radius: 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #34495e, stop:1 #2c3e50);
                padding: 10px;
                font-size: 10pt;
                color: #ecf0f1;
            }
            QListWidget::item {
                padding: 12px 16px;
                border-bottom: 1px solid #4a6741;
                border-radius: 6px;
                margin: 2px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #3498db, stop:1 #2980b9);
                border: 2px solid #3498db;
                color: #ffffff;
                font-weight: 600;
            }
            QListWidget::item:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #4a6741, stop:1 #34495e);
                border: 1px solid #3498db;
                color: #ecf0f1;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drag_active = True
            self.setStyleSheet(self.styleSheet() + """
                QListWidget {
                    border: 3px solid #27ae60;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #2ecc71, stop:1 #27ae60);
                }
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.drag_active = False
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #3498db;
                border-radius: 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #34495e, stop:1 #2c3e50);
                padding: 10px;
                font-size: 10pt;
                color: #ecf0f1;
            }
            QListWidget::item {
                padding: 12px 16px;
                border-bottom: 1px solid #4a6741;
                border-radius: 6px;
                margin: 2px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #3498db, stop:1 #2980b9);
                border: 2px solid #3498db;
                color: #ffffff;
                font-weight: 600;
            }
            QListWidget::item:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #4a6741, stop:1 #34495e);
                border: 1px solid #3498db;
                color: #ecf0f1;
            }
        """)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files_added = 0
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path) and self.is_image(path):
                # Check if file is already in the list
                if not any(self.item(i).data(Qt.UserRole) == path for i in range(self.count())):
                    item = QListWidgetItem(f"📷 {os.path.basename(path)} ({self.format_file_size(os.path.getsize(path))})")
                    item.setData(Qt.UserRole, path)
                    self.addItem(item)
                    files_added += 1
        
        # Reset drag styling
        self.drag_active = False
        self.dragLeaveEvent(None)
        
        if files_added > 0:
            self.files_dropped.emit(files_added)  # Emit signal instead of accessing parent
        
        event.acceptProposedAction()

    @staticmethod
    def is_image(path):
        return any(path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif'])

    @staticmethod
    def format_file_size(size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
