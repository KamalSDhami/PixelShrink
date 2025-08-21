# PixelShrink 🖼️✨

A modern, feature-rich image compression tool built with Python and PySide6. PixelShrink provides an intuitive drag-and-drop interface for batch image processing with multiple compression options and AI-powered background removal.

![PixelShrink Interface](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green?logo=qt&logoColor=white)
![PIL](https://img.shields.io/badge/PIL-Image%20Processing-orange)

## 🌟 Features

### Core Functionality
- **Batch Image Compression**: Process multiple images simultaneously
- **Multiple Formats**: Support for JPEG, PNG, BMP, TIFF, and WebP
- **Quality Control**: Adjustable compression levels with real-time preview
- **Smart Resizing**: Maintain aspect ratio with custom width/height options
- **Drag & Drop**: Intuitive file management with visual feedback

### Advanced Features
- **🤖 AI Background Removal**: Powered by `rembg` for automatic background removal
- **🎨 Image Enhancement**: Sharpen, blur, and contrast adjustments
- **📁 Folder Processing**: Batch process entire directories
- **💾 Format Conversion**: Convert between different image formats
- **🎯 Smart Output**: Organized output with size reduction statistics

### User Interface
- **Modern Dark Theme**: Sleek purple/pink gradient design
- **Real-time Progress**: Live progress bars and status updates
- **Responsive Layout**: Tabbed interface for organized workflow
- **Error Handling**: Comprehensive error messages and recovery

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/PixelShrink.git
   cd PixelShrink
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Dependencies
The application will automatically check and install missing dependencies:
- `PySide6` - Modern Qt-based GUI framework
- `Pillow` - Python Imaging Library for image processing
- `rembg` - AI background removal (optional, installed on-demand)

## 📋 Requirements

```txt
PySide6>=6.5.0
Pillow>=9.0.0
rembg>=2.0.0
```

## 🎯 Usage

### Basic Compression
1. Launch PixelShrink
2. Drag and drop images or click "Add Images"
3. Adjust quality settings (1-100)
4. Choose output format if needed
5. Click "Compress Images"

### Advanced Features

#### Background Removal
1. Navigate to the "Background Removal" tab
2. Enable "Remove Background" option
3. If `rembg` isn't installed, click the install button
4. Process images with AI-powered background removal

#### Batch Folder Processing
1. Click "Add Folder" to process entire directories
2. All supported image formats will be automatically detected
3. Maintain folder structure in output

#### Image Enhancement
- **Sharpen**: Enhance image details and clarity
- **Blur**: Apply gaussian blur effect
- **Contrast**: Adjust image contrast levels
- **Resize**: Custom width/height with aspect ratio preservation

### Output Management
- Processed images are saved to an `output` folder
- Original folder structure is preserved for batch operations
- Compression statistics are displayed in real-time

## 🏗️ Project Structure

```
PixelShrink/
├── main.py                 # Application entry point with dependency checking
├── requirements.txt        # Python dependencies
├── check_dependencies.py   # Automatic dependency installer
├── ui/
│   ├── __init__.py
│   ├── main_window.py      # Main application window and UI logic
│   └── drag_drop_widget.py # Custom drag-and-drop file widget
├── workers/
│   ├── __init__.py
│   └── compression_worker.py # Background thread for image processing
└── utils/
    ├── __init__.py
    └── image_utils.py      # Shared image processing utilities
```

## ⚙️ Configuration

### Supported Formats
- **Input**: JPEG, JPG, PNG, BMP, TIFF, TIF, WebP
- **Output**: JPEG, PNG, BMP, TIFF, WebP

### Quality Settings
- **JPEG**: 1-100 (recommended: 80-95)
- **PNG**: Lossless compression with optimization
- **WebP**: 1-100 with superior compression ratios

## 🔧 Development

### Setting up Development Environment
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Architecture
- **Modular Design**: Separated UI, workers, and utilities
- **Thread Safety**: Background processing with QThread
- **Error Handling**: Comprehensive exception management
- **Dependency Management**: Auto-installation with package mapping

## 🎨 Customization

### Themes
The application features a modern dark theme with:
- Purple/pink gradient accent colors
- Smooth hover transitions
- Professional typography
- Responsive component styling

### Adding New Features
1. UI components go in `ui/`
2. Background processing in `workers/`
3. Shared utilities in `utils/`
4. Follow the existing modular pattern

## 🐛 Troubleshooting

### Common Issues

#### "rembg not found" Error
```bash
# Manual installation
pip install rembg
```
Or use the built-in installer in the application.

#### Large File Processing
- For very large images, increase system memory
- Consider resizing before processing
- Process in smaller batches

#### Permission Errors
- Ensure write permissions to output directory
- Run as administrator if needed (Windows)

### Debug Mode
Enable verbose logging by modifying `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance

### Optimization Tips
- **Batch Processing**: Process multiple images together
- **Quality Settings**: Balance quality vs. file size
- **Format Selection**: Use WebP for best compression
- **Memory Management**: Close application between large batches

### Benchmarks
- **JPEG Compression**: Up to 70% size reduction
- **PNG Optimization**: 20-40% size reduction
- **Background Removal**: 2-5 seconds per image (GPU accelerated)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings for new functions
- Test on multiple operating systems
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PySide6** - Qt for Python GUI framework
- **Pillow** - Python Imaging Library
- **rembg** - Background removal AI models
- **Qt Company** - For the excellent Qt framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/PixelShrink/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/PixelShrink/discussions)
- **Email**: your.email@example.com

## 🔄 Version History

### v1.0.0
- Initial release with core compression features
- Modern dark theme UI
- Drag-and-drop functionality
- Basic image processing options

### v1.1.0 (Current)
- Added AI background removal
- Enhanced UI with purple/pink theme
- Improved batch processing
- Automatic dependency management
- Folder processing support

---

<div align="center">
  <p>Made with ❤️ and Python</p>
  <p>⭐ Star this repository if you find it helpful!</p>
</div>
