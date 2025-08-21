from PySide6.QtCore import QThread, Signal
from PIL import Image, ImageEnhance
import os
try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

class CompressionWorker(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished = Signal(str)
    
    def __init__(self, files, settings):
        super().__init__()
        self.files = files
        self.settings = settings
        
    def run(self):
        total = len(self.files)
        success_count = 0
        for i, file_path in enumerate(self.files):
            try:
                self.status.emit(f"Processing: {os.path.basename(file_path)}")
                self.process_image(file_path)
                success_count += 1
            except Exception as e:
                self.status.emit(f"Error processing {os.path.basename(file_path)}: {str(e)}")
            self.progress.emit(int((i + 1) / total * 100))
        self.finished.emit(f"Completed! {success_count}/{total} images processed successfully.")
    
    def process_image(self, file_path):
        img = Image.open(file_path)
        if self.settings.get('remove_background', False) and REMBG_AVAILABLE:
            try:
                import io
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                result_bytes = remove(img_bytes.getvalue())
                img = Image.open(io.BytesIO(result_bytes))
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
            except Exception as e:
                self.status.emit(f"Background removal failed for {os.path.basename(file_path)}: {str(e)}")
        if self.settings['format'].lower() == 'jpeg' and img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        if self.settings['resize_enabled']:
            if self.settings['maintain_aspect']:
                img.thumbnail((self.settings['width'], self.settings['height']), Image.LANCZOS)
            else:
                img = img.resize((self.settings['width'], self.settings['height']), Image.LANCZOS)
        if self.settings['enhance_enabled']:
            if self.settings['brightness'] != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(self.settings['brightness'])
            if self.settings['contrast'] != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(self.settings['contrast'])
            if self.settings['sharpness'] != 1.0:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(self.settings['sharpness'])
        save_kwargs = {}
        fmt = self.settings['format'].upper()
        if fmt == 'JPEG':
            save_kwargs['quality'] = self.settings['quality']
            save_kwargs['optimize'] = True
            save_kwargs['progressive'] = True
        elif fmt == 'PNG':
            save_kwargs['optimize'] = True
            if not self.settings['lossy']:
                save_kwargs['compress_level'] = 6
        elif fmt == 'WEBP':
            save_kwargs['quality'] = self.settings['quality']
            save_kwargs['method'] = 6
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        if self.settings['add_suffix']:
            out_name = f"{base_name}_compressed.{self.settings['format'].lower()}"
        else:
            out_name = f"{base_name}.{self.settings['format'].lower()}"
        out_path = os.path.join(self.settings['output_dir'], out_name)
        img.save(out_path, fmt, **save_kwargs)
