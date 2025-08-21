from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout, QComboBox, QSpinBox, QCheckBox, QLineEdit, QProgressBar, QGroupBox, QSlider, QListWidgetItem, QMessageBox, QTabWidget, QGridLayout, QSplitter, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import os
from pathlib import Path
from PIL import Image
from .drag_drop_widget import DragDropWidget
from workers.compression_worker import CompressionWorker

# Check rembg availability
try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 Pixel Shrink - Dark Edition")
        self.setGeometry(100, 100, 900, 700)
        self.worker = None
        
        # Check rembg availability dynamically
        self.check_rembg_availability()
        
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1a1a2e, stop:1 #16213e);
                color: #eee;
            }
            QWidget {
                font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
                font-size: 11pt;
                color: #eee;
                background-color: transparent;
            }
            QGroupBox {
                font-weight: 600;
                border: 2px solid #0f3460;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 20px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #16213e, stop:1 #0f3460);
                color: #eee;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 5px 12px;
                background-color: #e94560;
                color: white;
                font-weight: 700;
                border-radius: 8px;
                font-size: 11pt;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e94560, stop:1 #c73650);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 11pt;
                min-height: 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f056c7, stop:1 #e94560);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #c73650, stop:1 #a52a40);
            }
            QPushButton:disabled {
                background-color: #555;
                color: #999;
            }
            QTabWidget::pane {
                border: 2px solid #0f3460;
                border-radius: 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #16213e, stop:1 #0f3460);
                margin-top: -1px;
                padding: 10px;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #16213e, stop:1 #0f3460);
                border: 2px solid #0f3460;
                border-bottom: none;
                border-radius: 10px 10px 0 0;
                padding: 12px 20px;
                margin-right: 3px;
                font-weight: 600;
                color: #bbb;
                min-width: 80px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e94560, stop:1 #c73650);
                border-bottom: 3px solid #f056c7;
                color: white;
                font-weight: 700;
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #0f3460, stop:1 #533483);
                color: #f056c7;
            }
            QSlider::groove:horizontal {
                border: 1px solid #0f3460;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1a1a2e, stop:1 #16213e);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f056c7, stop:1 #e94560);
                border: 2px solid white;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -8px 0;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e94560, stop:1 #c73650);
            }
            QComboBox {
                border: 2px solid #0f3460;
                border-radius: 8px;
                padding: 8px 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #16213e, stop:1 #0f3460);
                color: #eee;
                min-width: 140px;
                font-weight: 500;
            }
            QComboBox:hover {
                border-color: #e94560;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #f056c7;
                margin-right: 10px;
            }
            QSpinBox, QLineEdit {
                border: 2px solid #0f3460;
                border-radius: 8px;
                padding: 8px 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #16213e, stop:1 #0f3460);
                color: #eee;
                font-weight: 500;
            }
            QSpinBox:focus, QLineEdit:focus {
                border-color: #e94560;
                outline: none;
            }
            QSlider::sub-page:horizontal {
                background: #3498db;
                border-radius: 3px;
            }
            QCheckBox {
                spacing: 12px;
                color: #eee;
                font-weight: 500;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #0f3460;
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #16213e, stop:1 #0f3460);
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e94560, stop:1 #c73650);
                border-color: #e94560;
                image: none;
            }
            QCheckBox::indicator:hover {
                border-color: #f056c7;
            }
            QProgressBar {
                border: 2px solid #0f3460;
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1a1a2e, stop:1 #16213e);
                text-align: center;
                font-weight: 700;
                color: white;
                min-height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #f056c7, stop:1 #e94560);
                border-radius: 8px;
                margin: 2px;
            }
            QLabel {
                color: #ecf0f1;
            }
            QTextEdit {
                background-color: #34495e;
                border: 1px solid #4a6741;
                border-radius: 4px;
                color: #ecf0f1;
                padding: 8px;
            }
        """)
        self.setup_ui()
        
    def check_rembg_availability(self):
        """Dynamically check if rembg is available"""
        global REMBG_AVAILABLE
        try:
            import importlib.util
            REMBG_AVAILABLE = importlib.util.find_spec('rembg') is not None
        except:
            REMBG_AVAILABLE = False
        return REMBG_AVAILABLE

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🎨 Pixel Shrink Pro")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("""
            color: #f056c7; 
            margin: 25px; 
            padding: 25px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #16213e, stop:1 #0f3460);
            border-radius: 15px;
            border: 3px solid #e94560;
            font-weight: 800;
        """)
        main_layout.addWidget(title)
        
        # Create splitter for main content
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - File list
        left_panel = self.create_file_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Settings
        right_panel = self.create_settings_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 500])
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Status bar
        self.status = QLabel("✨ Ready to compress images. Drag and drop files or use 'Add Images'.")
        self.status.setStyleSheet("""
            padding: 15px 25px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #16213e, stop:1 #0f3460); 
            border: 2px solid #e94560; 
            border-radius: 12px;
            font-size: 12pt;
            color: white;
            font-weight: 600;
        """)
        main_layout.addWidget(self.status)
        
    def create_file_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # File list group
        file_group = QGroupBox("Images to Process")
        file_layout = QVBoxLayout(file_group)
        
        # Instructions
        instructions = QLabel("📁 Drag and drop images here\n🖼️ or use the buttons below")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("""
            color: #bdc3c7; 
            font-style: italic; 
            padding: 30px;
            font-size: 12pt;
            line-height: 1.6;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                stop:0 #34495e, stop:1 #2c3e50);
            border-radius: 8px;
            border: 2px dashed #4a6741;
        """)
        file_layout.addWidget(instructions)
        
        # File list
        self.listWidget = DragDropWidget(self)
        self.listWidget.files_dropped.connect(self.on_files_dropped)  # Connect the signal
        file_layout.addWidget(self.listWidget)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.addBtn = QPushButton("📁 Add Images")
        self.addBtn.clicked.connect(self.add_images)
        self.addBtn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #17a2b8, stop:1 #117a8b);
                font-size: 10pt;
                padding: 10px 15px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #117a8b, stop:1 #0c5460);
            }
        """)
        btn_layout.addWidget(self.addBtn)
        
        self.addFolderBtn = QPushButton("📂 Add Folder")
        self.addFolderBtn.clicked.connect(self.add_folder)
        self.addFolderBtn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #fd7e14, stop:1 #e8590c);
                font-size: 10pt;
                padding: 10px 15px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e8590c, stop:1 #d43c00);
            }
        """)
        btn_layout.addWidget(self.addFolderBtn)
        
        self.removeBtn = QPushButton("🗑️ Remove Selected")
        self.removeBtn.clicked.connect(self.remove_selected)
        self.removeBtn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #dc3545, stop:1 #c82333);
                font-size: 10pt;
                padding: 10px 15px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #c82333, stop:1 #a71e2a);
            }
        """)
        btn_layout.addWidget(self.removeBtn)
        
        self.clearBtn = QPushButton("🧹 Clear All")
        self.clearBtn.clicked.connect(self.clear_all)
        self.clearBtn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #6c757d, stop:1 #5a6268);
                font-size: 10pt;
                padding: 10px 15px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #5a6268, stop:1 #495057);
            }
        """)
        btn_layout.addWidget(self.clearBtn)
        
        file_layout.addLayout(btn_layout)
        layout.addWidget(file_group)
        
        return panel
        
    def create_settings_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Create tabs for different settings
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Compression tab
        compression_tab = self.create_compression_tab()
        tabs.addTab(compression_tab, "🗜️ Compression")
        
        # Resize tab
        resize_tab = self.create_resize_tab()
        tabs.addTab(resize_tab, "📏 Resize")
        
        # Enhancement tab
        enhancement_tab = self.create_enhancement_tab()
        tabs.addTab(enhancement_tab, "✨ Enhance")
        
        # Output tab
        output_tab = self.create_output_tab()
        tabs.addTab(output_tab, "💾 Output")
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        self.previewBtn = QPushButton("👁️ Preview Changes")
        self.previewBtn.clicked.connect(self.preview_changes)
        self.previewBtn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #6f42c1, stop:1 #5a2d91);
                padding: 12px 20px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #5a2d91, stop:1 #4c1a78);
            }
        """)
        action_layout.addWidget(self.previewBtn)
        
        action_layout.addStretch()
        
        self.compressBtn = QPushButton("🚀 Start Compression")
        self.compressBtn.clicked.connect(self.compress_images)
        self.compressBtn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #28a745, stop:1 #1e7e34);
                font-size: 14pt;
                padding: 15px 30px;
                font-weight: 700;
                border-radius: 8px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e7e34, stop:1 #155724);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #155724, stop:1 #0d4016);
            }
        """)
        action_layout.addWidget(self.compressBtn)
        
        layout.addLayout(action_layout)
        
        return panel

    def create_compression_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Compression type
        comp_group = QGroupBox("Compression Type")
        comp_layout = QGridLayout(comp_group)
        
        self.compType = QComboBox()
        self.compType.addItems(["Lossy", "Lossless"])
        self.compType.currentTextChanged.connect(self.on_compression_type_changed)
        comp_layout.addWidget(QLabel("Type:"), 0, 0)
        comp_layout.addWidget(self.compType, 0, 1)
        
        # Quality slider
        self.qualityLabel = QLabel("Quality: 75")
        comp_layout.addWidget(self.qualityLabel, 1, 0)
        
        self.qualitySlider = QSlider(Qt.Horizontal)
        self.qualitySlider.setRange(1, 100)
        self.qualitySlider.setValue(75)
        self.qualitySlider.valueChanged.connect(self.on_quality_changed)
        comp_layout.addWidget(self.qualitySlider, 1, 1)
        
        layout.addWidget(comp_group)
        
        # Format selection
        fmt_group = QGroupBox("Output Format")
        fmt_layout = QGridLayout(fmt_group)
        
        self.formatBox = QComboBox()
        self.formatBox.addItems(["JPEG", "PNG", "WebP"])
        self.formatBox.currentTextChanged.connect(self.on_format_changed)
        fmt_layout.addWidget(QLabel("Format:"), 0, 0)
        fmt_layout.addWidget(self.formatBox, 0, 1)
        
        layout.addWidget(fmt_group)
        layout.addStretch()
        
        return tab
        
    def create_resize_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Resize options
        resize_group = QGroupBox("Resize Settings")
        resize_layout = QGridLayout(resize_group)
        
        self.resizeCheck = QCheckBox("Enable Resizing")
        self.resizeCheck.toggled.connect(self.on_resize_toggled)
        resize_layout.addWidget(self.resizeCheck, 0, 0, 1, 2)
        
        self.maintainAspectCheck = QCheckBox("Maintain Aspect Ratio")
        self.maintainAspectCheck.setChecked(True)
        resize_layout.addWidget(self.maintainAspectCheck, 1, 0, 1, 2)
        
        resize_layout.addWidget(QLabel("Width:"), 2, 0)
        self.widthSpin = QSpinBox()
        self.widthSpin.setRange(1, 10000)
        self.widthSpin.setValue(800)
        self.widthSpin.setSuffix(" px")
        resize_layout.addWidget(self.widthSpin, 2, 1)
        
        resize_layout.addWidget(QLabel("Height:"), 3, 0)
        self.heightSpin = QSpinBox()
        self.heightSpin.setRange(1, 10000)
        self.heightSpin.setValue(600)
        self.heightSpin.setSuffix(" px")
        resize_layout.addWidget(self.heightSpin, 3, 1)
        
        # Preset sizes
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Quick Presets:"))
        
        presets = [
            ("📺 HD", 1280, 720),
            ("🖥️ FHD", 1920, 1080),
            ("📱 4K", 3840, 2160),
            ("⬜ Square", 1000, 1000)
        ]
        
        for name, w, h in presets:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, width=w, height=h: self.set_preset_size(width, height))
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #6f42c1, stop:1 #5a2d91);
                    font-size: 9pt;
                    padding: 6px 12px;
                    border-radius: 4px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #5a2d91, stop:1 #4c1a78);
                }
            """)
            preset_layout.addWidget(btn)
        
        resize_layout.addLayout(preset_layout, 4, 0, 1, 2)
        
        self.on_resize_toggled(False)  # Initially disable resize controls
        
        layout.addWidget(resize_group)
        layout.addStretch()
        
        return tab
        
    def create_enhancement_tab(self):
        try:
            from rembg import remove
            REMBG_AVAILABLE = True
        except ImportError:
            REMBG_AVAILABLE = False
            
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Background removal option
        bg_group = QGroupBox("Background Removal")
        bg_layout = QGridLayout(bg_group)
        
        self.removeBgCheck = QCheckBox("Remove Background")
        if not REMBG_AVAILABLE:
            self.removeBgCheck.setEnabled(False)
            self.removeBgCheck.setToolTip("Install 'rembg' package to enable background removal")
        bg_layout.addWidget(self.removeBgCheck, 0, 0, 1, 2)
        
        if not REMBG_AVAILABLE:
            warning_label = QLabel("🔧 Background removal requires 'rembg' package")
            warning_label.setStyleSheet("""
                padding: 15px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2d1b3d, stop:1 #1a0e2e);
                border: 2px solid #f056c7;
                border-radius: 12px;
                color: #f056c7;
                font-size: 11pt;
                font-weight: 600;
                margin: 5px 0px;
            """)
            bg_layout.addWidget(warning_label, 1, 0, 1, 1)
            
            # Add install button
            install_btn = QPushButton("� Install rembg")
            install_btn.clicked.connect(self.install_rembg)
            install_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #f056c7, stop:1 #e94560);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-size: 11pt;
                    font-weight: bold;
                    margin: 5px 0px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #ff69b4, stop:1 #ff1493);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #d147a3, stop:1 #c9184a);
                }
            """)
            bg_layout.addWidget(install_btn, 1, 1, 1, 1)
        else:
            info_label = QLabel("✨ Uses AI to automatically remove image backgrounds")
            info_label.setStyleSheet("""
                padding: 15px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #0f3460, stop:1 #16213e);
                border: 2px solid #4CAF50;
                border-radius: 12px;
                color: #4CAF50;
                font-size: 11pt;
                font-weight: 600;
                margin: 5px 0px;
            """)
            bg_layout.addWidget(info_label, 1, 0, 1, 2)
        
        layout.addWidget(bg_group)
        
        # Enhancement options
        enhance_group = QGroupBox("Image Enhancement")
        enhance_layout = QGridLayout(enhance_group)
        
        self.enhanceCheck = QCheckBox("Enable Enhancement")
        self.enhanceCheck.toggled.connect(self.on_enhance_toggled)
        enhance_layout.addWidget(self.enhanceCheck, 0, 0, 1, 3)
        
        # Brightness
        enhance_layout.addWidget(QLabel("Brightness:"), 1, 0)
        self.brightnessSlider = QSlider(Qt.Horizontal)
        self.brightnessSlider.setRange(50, 150)
        self.brightnessSlider.setValue(100)
        self.brightnessSlider.valueChanged.connect(self.on_brightness_changed)
        enhance_layout.addWidget(self.brightnessSlider, 1, 1)
        self.brightnessLabel = QLabel("1.0")
        enhance_layout.addWidget(self.brightnessLabel, 1, 2)
        
        # Contrast
        enhance_layout.addWidget(QLabel("Contrast:"), 2, 0)
        self.contrastSlider = QSlider(Qt.Horizontal)
        self.contrastSlider.setRange(50, 150)
        self.contrastSlider.setValue(100)
        self.contrastSlider.valueChanged.connect(self.on_contrast_changed)
        enhance_layout.addWidget(self.contrastSlider, 2, 1)
        self.contrastLabel = QLabel("1.0")
        enhance_layout.addWidget(self.contrastLabel, 2, 2)
        
        # Sharpness
        enhance_layout.addWidget(QLabel("Sharpness:"), 3, 0)
        self.sharpnessSlider = QSlider(Qt.Horizontal)
        self.sharpnessSlider.setRange(50, 150)
        self.sharpnessSlider.setValue(100)
        self.sharpnessSlider.valueChanged.connect(self.on_sharpness_changed)
        enhance_layout.addWidget(self.sharpnessSlider, 3, 1)
        self.sharpnessLabel = QLabel("1.0")
        enhance_layout.addWidget(self.sharpnessLabel, 3, 2)
        
        self.on_enhance_toggled(False)  # Initially disable enhancement controls
        
        layout.addWidget(enhance_group)
        layout.addStretch()
        
        return tab
        
    def create_output_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Output settings
        output_group = QGroupBox("Output Settings")
        output_layout = QGridLayout(output_group)
        
        output_layout.addWidget(QLabel("Output Folder:"), 0, 0)
        self.outFolder = QLineEdit()
        self.outFolder.setPlaceholderText("Leave empty to use same folder as input")
        output_layout.addWidget(self.outFolder, 0, 1)
        
        self.browseBtn = QPushButton("📁 Browse")
        self.browseBtn.clicked.connect(self.browse_folder)
        output_layout.addWidget(self.browseBtn, 0, 2)
        
        # File naming options
        self.addSuffixCheck = QCheckBox("Add '_compressed' suffix to filenames")
        self.addSuffixCheck.setChecked(True)
        output_layout.addWidget(self.addSuffixCheck, 1, 0, 1, 3)
        
        self.overwriteCheck = QCheckBox("Overwrite existing files")
        output_layout.addWidget(self.overwriteCheck, 2, 0, 1, 3)
        
        layout.addWidget(output_group)
        
        # Statistics
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout(stats_group)
        
        self.statsText = QTextEdit()
        self.statsText.setMaximumHeight(100)
        self.statsText.setReadOnly(True)
        self.statsText.setText("No images processed yet.")
        stats_layout.addWidget(self.statsText)
        
        layout.addWidget(stats_group)
        layout.addStretch()
        
        return tab

    # Event handlers and utility methods
    def add_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "", 
            "Images (*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.tif);;All Files (*)"
        )
        added_count = 0
        for f in files:
            if not any(self.listWidget.item(i).data(Qt.UserRole) == f for i in range(self.listWidget.count())):
                size = os.path.getsize(f)
                size_str = DragDropWidget.format_file_size(size)
                item = QListWidgetItem(f"📷 {os.path.basename(f)} ({size_str})")
                item.setData(Qt.UserRole, f)
                self.listWidget.addItem(item)
                added_count += 1
        
        if added_count > 0:
            self.status.setText(f"✅ Added {added_count} image(s)")
        else:
            self.status.setText("ℹ️ No new images to add")
    
    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder with Images")
        if folder:
            added_count = 0
            supported_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.tif']
            
            # Recursively scan the folder
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in supported_extensions):
                        file_path = os.path.join(root, file)
                        if not any(self.listWidget.item(i).data(Qt.UserRole) == file_path for i in range(self.listWidget.count())):
                            size = os.path.getsize(file_path)
                            size_str = DragDropWidget.format_file_size(size)
                            # Show relative path from selected folder
                            relative_path = os.path.relpath(file_path, folder)
                            item = QListWidgetItem(f"📷 {relative_path} ({size_str})")
                            item.setData(Qt.UserRole, file_path)
                            self.listWidget.addItem(item)
                            added_count += 1
            
            if added_count > 0:
                self.status.setText(f"✅ Added {added_count} image(s) from folder (including subfolders)")
            else:
                self.status.setText("⚠️ No images found in selected folder and subfolders")

    def remove_selected(self):
        selected_items = self.listWidget.selectedItems()
        if selected_items:
            for item in selected_items:
                self.listWidget.takeItem(self.listWidget.row(item))
            self.status.setText(f"🗑️ Removed {len(selected_items)} selected image(s)")
        else:
            self.status.setText("ℹ️ No images selected to remove")
    
    def clear_all(self):
        count = self.listWidget.count()
        if count > 0:
            self.listWidget.clear()
            self.status.setText(f"🧹 Cleared all {count} images")
        else:
            self.status.setText("ℹ️ No images to clear")
    
    def on_files_dropped(self, count):
        """Handle files dropped signal from drag drop widget"""
        self.status.setText(f"✅ Added {count} image(s)")

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.outFolder.setText(folder)
    
    def preview_changes(self):
        if self.listWidget.count() == 0:
            QMessageBox.information(self, "Preview", "Please add images first.")
            return
        
        # Get first image for preview
        first_item = self.listWidget.item(0)
        file_path = first_item.data(Qt.UserRole)
        
        try:
            original_size = os.path.getsize(file_path)
            img = Image.open(file_path)
            original_dimensions = img.size
            
            # Simulate compression settings
            settings = self.get_compression_settings()
            temp_path = os.path.join(os.path.dirname(file_path), "temp_preview.jpg")
            
            # Apply settings to image
            if settings['resize_enabled']:
                if settings['maintain_aspect']:
                    img.thumbnail((settings['width'], settings['height']), Image.LANCZOS)
                else:
                    img = img.resize((settings['width'], settings['height']), Image.LANCZOS)
            
            # Save temporarily to estimate compression
            save_kwargs = {}
            if settings['format'].upper() == 'JPEG':
                save_kwargs['quality'] = settings['quality']
            img.save(temp_path, 'JPEG', **save_kwargs)
            
            compressed_size = os.path.getsize(temp_path)
            os.remove(temp_path)  # Clean up
            
            # Show preview dialog
            reduction = (1 - compressed_size / original_size) * 100
            message = f"""Preview for: {os.path.basename(file_path)}

Original:
- Size: {DragDropWidget.format_file_size(original_size)}
- Dimensions: {original_dimensions[0]} × {original_dimensions[1]}

After compression:
- Estimated size: {DragDropWidget.format_file_size(compressed_size)}
- New dimensions: {img.size[0]} × {img.size[1]}
- Size reduction: {reduction:.1f}%"""
            
            QMessageBox.information(self, "Preview Results", message)
            
        except Exception as e:
            QMessageBox.warning(self, "Preview Error", f"Could not preview: {str(e)}")
    
    # Settings change handlers
    def on_compression_type_changed(self, comp_type):
        is_lossy = comp_type == "Lossy"
        self.qualitySlider.setEnabled(is_lossy)
        self.qualityLabel.setEnabled(is_lossy)
        if not is_lossy:
            self.qualitySlider.setValue(100)
    
    def on_quality_changed(self, value):
        self.qualityLabel.setText(f"Quality: {value}")
    
    def on_format_changed(self, fmt):
        # PNG doesn't support quality settings in the same way
        is_quality_supported = fmt in ["JPEG", "WebP"]
        self.qualitySlider.setEnabled(is_quality_supported and self.compType.currentText() == "Lossy")
    
    def on_resize_toggled(self, enabled):
        self.maintainAspectCheck.setEnabled(enabled)
        self.widthSpin.setEnabled(enabled)
        self.heightSpin.setEnabled(enabled)
    
    def on_enhance_toggled(self, enabled):
        self.brightnessSlider.setEnabled(enabled)
        self.contrastSlider.setEnabled(enabled)
        self.sharpnessSlider.setEnabled(enabled)
        self.brightnessLabel.setEnabled(enabled)
        self.contrastLabel.setEnabled(enabled)
        self.sharpnessLabel.setEnabled(enabled)
    
    def on_brightness_changed(self, value):
        self.brightnessLabel.setText(f"{value/100:.1f}")
    
    def on_contrast_changed(self, value):
        self.contrastLabel.setText(f"{value/100:.1f}")
    
    def on_sharpness_changed(self, value):
        self.sharpnessLabel.setText(f"{value/100:.1f}")
    
    def set_preset_size(self, width, height):
        self.widthSpin.setValue(width)
        self.heightSpin.setValue(height)
        self.resizeCheck.setChecked(True)
        self.on_resize_toggled(True)
    
    def get_compression_settings(self):
        return {
            'format': self.formatBox.currentText().lower(),
            'lossy': self.compType.currentText() == "Lossy",
            'quality': self.qualitySlider.value(),
            'resize_enabled': self.resizeCheck.isChecked(),
            'width': self.widthSpin.value(),
            'height': self.heightSpin.value(),
            'maintain_aspect': self.maintainAspectCheck.isChecked(),
            'enhance_enabled': self.enhanceCheck.isChecked(),
            'brightness': self.brightnessSlider.value() / 100.0,
            'contrast': self.contrastSlider.value() / 100.0,
            'sharpness': self.sharpnessSlider.value() / 100.0,
            'remove_background': self.removeBgCheck.isChecked(),
            'output_dir': self.outFolder.text() or os.getcwd(),
            'add_suffix': self.addSuffixCheck.isChecked()
        }

    def compress_images(self):
        count = self.listWidget.count()
        if count == 0:
            QMessageBox.information(self, "No Images", "Please add images to compress first.")
            return
        
        # Get list of file paths
        files = []
        for i in range(count):
            files.append(self.listWidget.item(i).data(Qt.UserRole))
        
        # Get settings
        settings = self.get_compression_settings()
        
        # Create output directory if it doesn't exist
        os.makedirs(settings['output_dir'], exist_ok=True)
        
        # Disable UI during compression
        self.compressBtn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Start compression in background thread
        self.worker = CompressionWorker(files, settings)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status.setText)
        self.worker.finished.connect(self.on_compression_finished)
        self.worker.start()
    
    def on_compression_finished(self, message):
        self.progress_bar.setVisible(False)
        self.compressBtn.setEnabled(True)
        self.status.setText(message)
        
        # Update statistics
        total_original_size = 0
        total_compressed_size = 0
        output_dir = self.get_compression_settings()['output_dir']
        
        for i in range(self.listWidget.count()):
            original_path = self.listWidget.item(i).data(Qt.UserRole)
            total_original_size += os.path.getsize(original_path)
            
            # Find corresponding compressed file
            base_name = os.path.splitext(os.path.basename(original_path))[0]
            fmt = self.formatBox.currentText().lower()
            if self.addSuffixCheck.isChecked():
                compressed_name = f"{base_name}_compressed.{fmt}"
            else:
                compressed_name = f"{base_name}.{fmt}"
            
            compressed_path = os.path.join(output_dir, compressed_name)
            if os.path.exists(compressed_path):
                total_compressed_size += os.path.getsize(compressed_path)
        
        if total_original_size > 0:
            reduction = (1 - total_compressed_size / total_original_size) * 100
            stats_text = f"""Compression Complete!

Original total size: {DragDropWidget.format_file_size(total_original_size)}
Compressed total size: {DragDropWidget.format_file_size(total_compressed_size)}
Total reduction: {reduction:.1f}%
Files processed: {self.listWidget.count()}"""
            self.statsText.setText(stats_text)
        
        QMessageBox.information(self, "Compression Complete", message)
        
        self.worker = None
    
    def install_rembg(self):
        """Install rembg package"""
        try:
            import subprocess
            import sys
            self.status.setText("📦 Installing rembg package...")
            
            # Install rembg
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'rembg'])
            
            # Refresh availability
            if self.check_rembg_availability():
                self.status.setText("✅ rembg package installed successfully! Please restart the application.")
                QMessageBox.information(self, "Success", "rembg package installed successfully!\nPlease restart the application to use background removal.")
            else:
                self.status.setText("❌ Failed to install rembg package")
                QMessageBox.warning(self, "Error", "Failed to install rembg package. Please try again or install manually.")
                
        except Exception as e:
            self.status.setText(f"❌ Error installing rembg: {str(e)}")
            QMessageBox.warning(self, "Error", f"Error installing rembg package:\n{str(e)}")
