# Quick Start Guide - AddAttachment Application

## For Researchers Using the Executable

### Starting the Application

1. **Double-click** `AddAttachment_Main.exe` in the `dist\AddAttachment_Main` folder
2. The application window will open with two panels

### Using the Interface

#### Left Panel: Participant Information
Fill in all the required fields:

1. **Naam speler** - Child's name
2. **Identificatie** - Participant ID
3. **Leeftijd (9-13)** - Age (must be between 9 and 13)
   - You'll see a ✓ checkmark when valid
   - You'll see ❌ if age is out of range

4. **Geslacht** - Gender
   - Select M (Mannelijk) or V (Vrouwelijk)

5. **Contingentie** - Select 20% or 80%

6. **Trial Block** - Select Block 1 or Block 2

7. **Support Frequentie** - Select Frequent or Infrequent

8. **Trial nummer** (Optional)
   - Default is 0 (starts from beginning)
   - Can be set to 0-25 to start from a specific trial

9. Click **💾 Save & Continue**

#### Right Panel: Live Activity Log
This shows you what's happening in real-time:

**What to look for:**
- ✓ **Green checkmarks** = Everything is working correctly
- 🔌 **"Unity connected"** = Unity game has connected successfully
- 📡 **"Listening for messages"** = System is ready and waiting for data
- ❌ **Red errors** = Something needs attention

**Common messages you'll see:**

| Time | Message | Meaning |
|------|---------|---------|
| [10:23:15] | GUI started | Application is running |
| [10:23:45] | ✓ Configuration loaded | Settings loaded successfully |
| [10:23:46] | ✓ Player session created | Participant data processed |
| [10:23:46] | ✓ Data directory created | Files ready for saving data |
| [10:23:47] | ✓ Selected: Mama figure | Support figure chosen |
| [10:23:48] | 🌐 Starting WebSocket server | Server starting |
| [10:23:48] | ✓ Waiting for Unity to connect | Ready for Unity |
| [10:23:50] | 🔌 Unity connected | **Unity is connected!** |
| [10:23:50] | ✓ All initialization data sent | Data sent to Unity |
| [10:23:50] | 📡 Listening for messages | Ready for experiment |

### After Filling the Form

1. Click **Save & Continue**
2. A small dialog will appear asking for **"Starting Support Figure"**
3. Type either:
   - `mama figuur` (for brown hair, green shirt character)
   - `alternative` (for blonde hair, white shirt character)
4. Press OK

### What Happens Next

Watch the **Live Activity Log** (right panel) to see:

1. ✓ Configuration and files being created
2. 🌐 WebSocket server starting
3. ⏳ **"Waiting for Unity to connect"** - At this point:
   - **Start Unity** if not already running
   - Unity should connect automatically
4. 🔌 **"Unity connected"** - Success! You'll see:
   - Connection IP address
   - Messages being sent to Unity
   - "All initialization data sent"
5. 📡 **"Listening for messages"** - System is now active
6. 📨 Messages from Unity will appear here

### Status Bar (Bottom)

The bottom bar shows the current status:
- **Ready** - Waiting for input
- **Validating input...** - Checking your data
- **✓ Validation successful!** - All good, proceeding
- **Error: Missing required fields** - Something needs to be filled in

### Troubleshooting

#### "Unity connected" doesn't appear
- Make sure Unity is running
- Check that Unity is trying to connect to the server
- Verify network settings (usually localhost:8080)

#### Red error messages
- Read the error message carefully
- Common issues:
  - Missing required fields
  - Age out of range (must be 9-13)
  - Trial number out of range (must be 0-25)

#### Need to restart
- Close the application
- Double-click `AddAttachment_Main.exe` again
- All previous data is saved in the `data` folder

### Tips

1. **Keep the log visible** - It helps you understand what's happening
2. **Wait for "Unity connected"** before starting the experiment
3. **Check for green ✓ checkmarks** - They mean success
4. **Use Clear Log button** if the log gets too long (bottom right of log panel)
5. **Data is automatically saved** in the `data` folder with timestamp

### Data Location

All collected data is saved in:
```
Python\python\data\YYYY_MM_DD__HH_MM\
```

Each session gets its own folder with timestamp.

---

## For Developers/Technicians

### Running from Python

If you need to run from source instead of the executable:

```bash
cd c:\AddaGit\Python\python
python addattachment.py
```

### Building New Executable

If changes were made and you need to rebuild:

```bash
cd c:\AddaGit\Python\python
.\build_executable.bat
```

Wait 2-5 minutes for the build to complete.

### Reverting to Old GUI

Edit `addattachment.py`:

Change:
```python
from utils.GUI_improved import ImprovedGUI
gui = ImprovedGUI()
```

To:
```python
from utils.GUI import GUI
gui = GUI()
```

### Log Colors Reference

- **Black** - Normal information
- **Green** - Success messages
- **Orange** - Warnings
- **Red** - Errors
- **Gray** - Debug information

---

## Need Help?

Common issues and solutions:

### Application won't start
- Make sure all files from the `dist\AddAttachment_Main` folder are present
- Try running as Administrator
- Check if antivirus is blocking it

### Unity won't connect
- Ensure Unity is configured to connect to localhost:8080
- Check firewall settings
- Look for red error messages in the log

### Data not saving
- Check `data` folder exists
- Verify write permissions
- Look for error messages in the log

### Form won't submit
- Check all required fields are filled
- Verify age is 9-13
- Check trial number is 0-25
- Look at inline error messages (red text)

---

**Remember**: The **Live Activity Log** is your friend! It shows you exactly what's happening, making it easy to spot and fix any issues.
