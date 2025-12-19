# Building AddAttachment Executable

This guide explains how to create a standalone executable (.exe) for the AddAttachment application that non-technical users can run without installing Python.

## 📋 Prerequisites

Before building the executable, make sure you have:

1. **Python 3.10** installed
2. **All dependencies** installed (see Installation section below)
3. **PyInstaller** installed

### Installation

If you have the `environment.yml` file, create the conda environment:

```bash
conda env create -f environment.yml
conda activate addAttachment
```

Or install dependencies manually:

```bash
pip install pyinstaller pyyaml websockets pylsl brainflow pyserial python-osc pywin32
```

## 🚀 Quick Build (Easiest Method)

### For Windows Users:

1. Open the `Python/python` folder
2. **Double-click** `build_executable.bat`
3. Wait for the build to complete (2-5 minutes)
4. Find your executable in the `dist` folder

That's it! ✅

## 🔧 Manual Build (Alternative)

If you prefer to build manually or need more control:

```bash
# Navigate to the python directory
cd c:\AddaGit\Python\python

# Clean previous builds
rmdir /s /q build dist

# Build the executable
pyinstaller AddAttachment_Main.spec --clean
```

## 📦 What Gets Built

After building, you'll find:

```
dist/
├── AddAttachment_Main.exe  ← Main executable (standalone)
└── conf.yaml               ← Configuration file (must be in same folder)
```

## 📤 Distribution to End Users

To distribute the application to non-technical users:

1. **Copy the entire `dist` folder** or at minimum:
   - `AddAttachment_Main.exe`
   - `conf.yaml` (must be in the same folder)

2. **Create a simple folder structure** for users:
   ```
   AddAttachment/
   ├── AddAttachment_Main.exe
   ├── conf.yaml
   └── data/  (will be created automatically)
   ```

3. **User Instructions:**
   - Double-click `AddAttachment_Main.exe`
   - Fill in the GUI form
   - Click "Save & close"
   - The application will connect to Unity via WebSocket

## ⚙️ Configuration (conf.yaml)

The `conf.yaml` file contains WebSocket connection settings:

```yaml
DATA_CAPTURE:
  WS:
    IP: "localhost"    # Unity server IP
    PORT: "8080"       # Unity server port
```

**Note:** If users need to connect to Unity on a different computer, they should edit `conf.yaml` to change the IP address.

## 🐛 Troubleshooting

### Build Fails with "Module not found"

**Solution:** Install missing dependencies:
```bash
pip install <missing-module>
```

Then rebuild.

### Executable won't start / Shows console errors

**Possible causes:**
1. `conf.yaml` is missing → Place it in the same folder as the .exe
2. Missing DLL files → Rebuild with `--clean` flag
3. Antivirus blocking → Add exception for the executable

### "Could not find Python DLL" error

**Solution:** Ensure you're building with the correct Python environment:
```bash
# Check Python version
python --version  # Should be 3.10.x

# Verify PyInstaller sees the right Python
pyinstaller --version
```

### Executable is very large (>100MB)

This is normal for PyInstaller executables because they bundle:
- Python interpreter
- All libraries (numpy, websockets, etc.)
- Your application code

Typical size: 50-150 MB depending on dependencies.

## 🔄 Rebuilding After Code Changes

Whenever you update the Python code:

1. Run `build_executable.bat` again
2. Or manually: `pyinstaller AddAttachment_Main.spec --clean`
3. Test the new executable before distributing

## 📝 Spec File Details

The `AddAttachment_Main.spec` file controls the build process:

- **Entry point:** `addattachment.py`
- **Included data:** `conf.yaml`, `utils/`, `Player/`, `websocket/`, etc.
- **Console mode:** Disabled (no black console window)
- **Single file:** Yes (all files bundled into one .exe)

## 🎯 Testing the Executable

Before distributing to users, test the executable:

1. ✅ Run on a clean Windows machine (without Python installed)
2. ✅ Verify GUI appears correctly
3. ✅ Fill in all fields and click "Save & close"
4. ✅ Check that WebSocket connects to Unity
5. ✅ Verify data is saved in the `data/` folder
6. ✅ Test the starting support figure dialog appears

## 📊 File Size Optimization (Optional)

To reduce executable size:

1. **Remove unused dependencies** from `environment.yml`
2. **Use UPX compression** (already enabled in spec file)
3. **Exclude unnecessary modules:**
   ```python
   # In .spec file, add to excludes:
   excludes=['matplotlib', 'scipy', 'pandas']  # if not used
   ```

## 🔐 Code Signing (Optional)

For professional distribution, consider code signing:

```bash
# After building, sign with your certificate:
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\AddAttachment_Main.exe
```

This prevents Windows SmartScreen warnings for users.

## ✅ Checklist Before Distribution

- [ ] Executable builds without errors
- [ ] Tested on clean machine without Python
- [ ] GUI displays correctly
- [ ] All fields work properly
- [ ] WebSocket connection works
- [ ] Data saves correctly
- [ ] conf.yaml is included
- [ ] User instructions are clear
- [ ] Version number is documented

## 📞 Support

If users encounter issues:
1. Check `conf.yaml` settings
2. Verify Unity is running and WebSocket server is active
3. Check firewall settings (port 8080 must be open)
4. Review log files in `data/` folder

---

**Built with:** PyInstaller
**Python Version:** 3.10
**Last Updated:** October 2025
