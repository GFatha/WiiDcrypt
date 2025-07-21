# WiiU CDN Decryptor v2.0

A professional-grade tool for processing WiiU CDN files to prepare them for decryption.

![WiiU CDN Decryptor](https://img.shields.io/badge/version-2.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **📁 Folder Validation**: Automatically validates CDN folder structure
- **🔄 File Processing**: Renames extensionless files to .app format
- **📝 TMD Handling**: Intelligent TMD file processing and backup
- **📜 Certificate Management**: Handles title.cert template copying
- **📊 Progress Tracking**: Real-time progress feedback with detailed status
- **🎨 Modern Interface**: Professional UI with tooltips and keyboard shortcuts
- **📋 Comprehensive Logging**: Detailed operation logs for debugging and support
- **🛠️ Error Recovery**: Graceful error handling with user-friendly messages

## 🚀 Quick Start

### Requirements
- Python 3.7 or higher
- tkinter (usually included with Python)

### Installation
1. Clone or download this repository
2. Navigate to the project directory
3. Run the application:
   ```bash
   python app.py
   ```

### Usage
1. **Launch**: Run `python app.py` to start the application
2. **Select Folder**: Click "📁 Select CDN Folder" or press Enter
3. **Choose Directory**: Browse and select your WiiU CDN folder
4. **Processing**: Watch the progress dialog as files are processed
5. **Completion**: Review the completion message and choose next action

## ⌨️ Keyboard Shortcuts

- **Enter**: Start processing / Select highlighted option
- **F1**: Show About dialog
- **Escape**: Cancel/Exit with confirmation
- **Ctrl+Q**: Quick exit with confirmation

## 🔧 Configuration

The application uses centralized configuration in `wiiman/config.py`:
- Window dimensions and UI settings
- File extension patterns
- Color themes and styling
- Error messages and user prompts
- Logging configuration

## 📊 Logging

Comprehensive logging is automatically enabled:
- **Location**: `~/.wiidcrypt/logs/`
- **Format**: Daily log files (`wiidcrypt_YYYYMMDD.log`)
- **Content**: Detailed operation tracking, errors, and user actions
- **Access**: Help → Open Log Folder

## 🛠️ Troubleshooting

### Common Issues

**"Invalid Folder" Error**
- Ensure the folder contains WiiU CDN files (.app, .tmd, .tik)
- Check that files are not corrupted or zero-byte

**"Permission Denied" Error**
- Run as administrator on Windows
- Check file/folder permissions on Unix systems

**"Template Missing" Warning**
- Verify `template/title.cert` exists in the application directory
- Application will continue without template if missing

### Getting Support
1. Check the troubleshooting guide: Help → Troubleshooting
2. Review log files for detailed error information
3. Report issues with log file content for faster resolution

## 👥 Contributors

- **GFatha** - Lead Developer and Project Maintainer

## 🔄 Version History

### v2.0 (Current)
- Complete UI/UX overhaul with modern interface
- Comprehensive logging system
- Enhanced error handling and recovery
- Progress tracking with real-time feedback
- Professional troubleshooting and help system
- Improved code quality and maintainability

---

**Made with ❤️ for the WiiU homebrew community**
