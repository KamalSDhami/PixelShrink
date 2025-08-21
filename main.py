import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Check and install dependencies first
try:
    from check_dependencies import check_and_install
    check_and_install()
except Exception as e:
    print(f"Warning: Could not check dependencies: {e}")

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Pixel Shrink")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Image Tools")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
