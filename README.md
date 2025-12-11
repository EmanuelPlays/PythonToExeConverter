# 🚀 Py to EXE Converter

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyInstaller](https://img.shields.io/badge/PyInstaller-5.0+-orange.svg)](https://www.pyinstaller.org/)
[![Rich](https://img.shields.io/badge/Rich-13.0+-green.svg)](https://rich.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Transform your Python scripts into standalone executables with ease!** ✨

A powerful, interactive Python to EXE converter built on top of PyInstaller, featuring a beautiful console interface powered by the Rich library. No more memorizing command-line flags – just answer a few questions and get your executable ready!

## 🎯 What is this?

This tool simplifies the process of converting Python scripts into executable files (.exe on Windows, etc.) using PyInstaller. Instead of typing long command-line arguments, you interact with a user-friendly prompt system that guides you through all available options.

### 🔍 How it works
1. **Interactive Prompts**: Answer simple yes/no and text questions
2. **Smart Defaults**: Remembers your last settings for faster subsequent builds
3. **Rich Interface**: Beautiful, colorful console output with progress indicators
4. **Comprehensive Options**: Access to all major PyInstaller features
5. **Error Handling**: Clear feedback and help system built-in

## ✨ Features

- 🎨 **Beautiful Interface**: Rich-powered console with panels, tables, and live progress
- 📁 **Flexible Output**: Choose between single file or directory bundles
- 🖼️ **Custom Icons**: Add custom icons to your executables
- 🔒 **Windowed Apps**: Create GUI applications without console windows
- 📦 **Hidden Imports**: Automatically include hard-to-find dependencies
- 🚫 **Module Exclusion**: Exclude unnecessary modules to reduce size
- 📄 **Data Inclusion**: Bundle additional files and data
- 🗜️ **Compression**: UPX compression support for smaller executables
- 🔐 **Encryption**: Bytecode encryption for added security
- 📋 **Version Info**: Add detailed version information to executables
- 🛠️ **Developer Mode**: Advanced options for power users
- 💾 **Persistent Settings**: Remembers your preferences between runs

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/yourusername/py-to-exe-converter.git
   cd py-to-exe-converter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the converter**
   ```bash
   python main.py
   ```

That's it! Follow the interactive prompts to configure your build.

## 📖 Usage

### Basic Workflow

1. **Launch**: Run `python main.py`
2. **Select Script**: Enter the path to your Python file
3. **Configure**: Answer the prompts for your desired options
4. **Build**: Let PyInstaller do its magic
5. **Done**: Find your executable in the output directory

### Configuration Options

The tool supports all major PyInstaller options through an intuitive interface:

| Option | Description | <span title="Tooltip: Choose between a single executable file or a directory with multiple files">ℹ️</span> |
|--------|-------------|-----|
| **Output Mode** | Single file vs. directory bundle | <span title="Onefile: Creates a single .exe. Onedir: Creates a folder with executable and dependencies">?</span> |
| **Windowed** | Hide console window for GUI apps | <span title="Useful for applications with graphical interfaces">?</span> |
| **Icon** | Custom icon for the executable | <span title="Supports .ico, .png, .jpg formats">?</span> |
| **Name** | Custom executable name | <span title="Defaults to script name if left blank">?</span> |
| **Hidden Imports** | Additional modules to include | <span title="Comma-separated list of module names">?</span> |
| **Exclude Modules** | Modules to exclude from bundle | <span title="Reduces size by removing unnecessary code">?</span> |
| **Add Data** | Include additional files | <span title="Format: 'source;destination' - can include multiple">?</span> |
| **UPX Compression** | Compress executable size | <span title="Requires UPX to be installed separately">?</span> |
| **Version Info** | Add version metadata | <span title="Uses versioninfo.txt format">?</span> |
| **Encryption** | Encrypt Python bytecode | <span title="Adds security but increases startup time">?</span> |

### Advanced Options

- **Runtime Hooks**: Custom initialization code
- **Manifest Files**: Windows manifest customization
- **Code Signing**: macOS code signing support
- **Bootloader Options**: Advanced PyInstaller settings

## 🎮 Interactive Help

Type `help` at any prompt to see:
- Current configuration values
- Developer options status
- Quick reference guide

## 📋 Examples

### Basic GUI Application
```
Path to Python file: my_app.py
Executable name: MyApp
Output directory: dist
Build as single file? Yes
Windowed (no console)? Yes
Icon path: icon.png
... (other options as needed)
```

### Command-Line Tool with Dependencies
```
Path to Python file: cli_tool.py
Executable name: MyTool
Output directory: build
Build as single file? Yes
Windowed (no console)? No
Hidden imports: requests,beautifulsoup4
... (other options as needed)
```

## 🛠️ Developer Mode

Enable developer mode for advanced PyInstaller options:
- Custom spec file paths
- Work directory specification
- Alternative Python executable paths

## 📁 Project Structure

```
py-to-exe-converter/
├── main.py                 # Main converter script
├── requirements.txt        # Python dependencies
├── versioninfo.txt         # Version information template
├── icon.png               # Default icon
├── ReadME.md              # This file
├── test.py                # Test script
├── main.spec              # PyInstaller spec file
├── test.spec              # Test spec file
└── build/                 # Build artifacts (generated)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PyInstaller](https://www.pyinstaller.org/) - The underlying packaging technology
- [Rich](https://rich.readthedocs.io/) - Beautiful console output library
- [EmanuelPlays](https://github.com/EmanuelPlays) - Original creator

## 🆘 Troubleshooting

### Common Issues

**"Module not found" errors:**
- Use "Hidden Imports" to include missing modules
- Check your Python environment has all dependencies

**Large executable size:**
- Use "Exclude Modules" to remove unnecessary code
- Enable UPX compression
- Consider onefile vs onedir based on your needs

**Icon not showing:**
- Ensure icon file exists and is in a supported format (.ico recommended)
- Check file path is correct

**Build fails:**
- Ensure PyInstaller is properly installed
- Check Python version compatibility
- Try running with "Clean build" option

### Getting Help

- Check the [PyInstaller documentation](https://pyinstaller.readthedocs.io/)
- Open an issue on GitHub
- Type `help` during interactive mode for current configuration


**Made with ❤️ by EmanuelPlays**

