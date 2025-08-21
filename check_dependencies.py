import subprocess
import sys
import importlib.util

# Package name -> import name mapping
REQUIRED = {
    'PySide6': 'PySide6',
    'Pillow': 'PIL',  # Pillow package imports as PIL
    'rembg': 'rembg',
    'onnxruntime': 'onnxruntime'
}

def is_installed(import_name):
    """Check if a package is installed by its import name"""
    return importlib.util.find_spec(import_name) is not None

def check_and_install():
    """Check for missing packages and install them"""
    print("🔍 Checking dependencies...")
    
    missing_packages = []
    for package_name, import_name in REQUIRED.items():
        if not is_installed(import_name):
            missing_packages.append(package_name)
            print(f"❌ {package_name} is not installed")
        else:
            print(f"✅ {package_name} is installed")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {missing_packages}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_packages])
            print("✅ All packages installed successfully!")
            
            # Verify installation
            print("\n🔍 Verifying installation...")
            all_verified = True
            for package_name in missing_packages:
                import_name = REQUIRED[package_name]
                if is_installed(import_name):
                    print(f"✅ {package_name} verified")
                else:
                    print(f"❌ {package_name} installation failed")
                    all_verified = False
            
            return all_verified
                    
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing packages: {e}")
            return False
    else:
        print("✅ All required packages are installed!")
    
    return True

if __name__ == '__main__':
    check_and_install()