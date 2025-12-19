# AddAttachment - User Guide

## 🎯 Quick Start

1. **Double-click** `AddAttachment_Main.exe`
2. **Fill in the form** with participant information
3. **Click** "Save & close"
4. The program will connect to Unity and start the experiment

That's it! ✨

---

## 📋 Step-by-Step Instructions

### Step 1: Start the Program

- **Locate** the file `AddAttachment_Main.exe`
- **Double-click** to open it
- A form window will appear

### Step 2: Fill in Participant Information

Complete all fields in the form:

1. **Naam** (Name): Enter participant's name
2. **ID**: Enter participant ID number
3. **Contingentie**: Select 20 or 80
4. **Leeftijd** (Age): Enter age (9-13 years)
5. **Geslacht** (Gender): Select M or V
6. **Block**: Select 1 or 2
7. **Support Frequentie**: Choose:
   - **Frequent** = More support during experiment
   - **Infrequent** = Less support during experiment
8. **Trial nummer**: Leave at 0 (unless restarting from specific trial)

### Step 3: Choose Starting Figure

After clicking "Save & close", a second dialog appears:

**Which figure to start with?**
- **'mama figuur'** = Brown hair, green shirt 👩‍🦰
- **'alternative'** = Blonde hair, white shirt 👱‍♀️

Type your choice and press OK.

### Step 4: Automatic Connection

The program will now:
- ✅ Create a data folder for this session
- ✅ Connect to Unity via WebSocket
- ✅ Send all participant information
- ✅ Start the experiment

---

## ⚙️ Configuration

### Changing Unity Connection

If Unity is running on a different computer:

1. **Open** `conf.yaml` with Notepad
2. **Change** the IP address:
   ```yaml
   DATA_CAPTURE:
     WS:
       IP: "192.168.1.100"  # Change this to Unity computer's IP
       PORT: "8080"
   ```
3. **Save** the file
4. **Restart** AddAttachment_Main.exe

---

## 📂 Data Storage

All experiment data is automatically saved in the `data` folder:

```
data/
└── 2025_10_17__14_30/      ← Session folder (date + time)
    ├── player_config.json   ← Participant settings
    ├── websocket/           ← Communication logs
    │   └── websocket.csv
    ├── eeg/                 ← EEG data (if used)
    ├── gsr/                 ← GSR data (if used)
    └── ...
```

Each session creates a new folder with timestamp.

---

## 🔍 Field Descriptions

### **Contingentie** (Contingency)
- **20**: 20% success rate condition
- **80**: 80% success rate condition

### **Support Frequentie** (Support Frequency)
- **Frequent**: Support figure appears often
- **Infrequent**: Support figure appears rarely

### **Block**
- **1**: First experimental block
- **2**: Second experimental block

### **Trial nummer** (Trial Number)
- Normally **0** (start from beginning)
- Only change if you need to restart from a specific trial (e.g., after technical issue)

---

## ❓ Troubleshooting

### Problem: Program won't start

**Solutions:**
- ✅ Make sure `conf.yaml` is in the same folder as the .exe
- ✅ Right-click the .exe → "Run as administrator"
- ✅ Check if antivirus is blocking the program

### Problem: "Cannot connect to Unity"

**Solutions:**
- ✅ Make sure Unity is running
- ✅ Check that Unity's WebSocket server is active (port 8080)
- ✅ Verify IP address in `conf.yaml` is correct
- ✅ Check firewall settings

### Problem: GUI fields won't accept input

**Solutions:**
- ✅ Click inside the field first
- ✅ Make sure you're entering valid data (e.g., age 9-13)
- ✅ Try restarting the program

### Problem: Age field turns red

**Cause:** Age must be between 9 and 13 years

**Solution:** Enter a valid age (9, 10, 11, 12, or 13)

### Problem: "Some values not entered?"

**Cause:** One or more required fields are empty

**Solution:** 
- Check all fields are filled in
- For **Trial nummer**, you can enter **0** (this is valid)

---

## 📊 After the Experiment

### Collecting Data

1. Navigate to the `data` folder
2. Find the session folder (named with date and time)
3. Copy the entire folder to your data storage location
4. The folder contains all experiment data

### Data Files

- **player_config.json**: Participant settings
- **websocket.csv**: All Unity communication logs
- **eeg/** folder: EEG recordings (if applicable)
- **gsr/** folder: GSR recordings (if applicable)

---

## ⚠️ Important Notes

### Before Starting an Experiment:

- [ ] Unity is running
- [ ] WebSocket server is active in Unity
- [ ] conf.yaml is properly configured
- [ ] All equipment is connected (EEG, GSR if used)

### During the Experiment:

- Do NOT close the program window
- Do NOT disconnect network cables
- Monitor the data folder to ensure data is being saved

### After the Experiment:

- Wait for confirmation that data is saved
- Back up the data folder immediately
- Close the program

---

## 🆘 Need Help?

If you encounter problems:

1. **Check** this guide's Troubleshooting section
2. **Verify** conf.yaml settings
3. **Restart** the program
4. **Check** Unity connection
5. **Contact** technical support with:
   - Description of the problem
   - Error messages (if any)
   - Last successful step

---

## 📝 Version Information

**Program:** AddAttachment
**Version:** 1.0
**Last Updated:** October 2025
**Python Version:** 3.10
**Platform:** Windows 10/11

---

## 📖 Quick Reference Card

| Field | Valid Values | Example |
|-------|-------------|---------|
| Naam | Any text | "Jan Jansen" |
| ID | Any number | 42 |
| Contingentie | 20 or 80 | 80 |
| Leeftijd | 9-13 | 12 |
| Geslacht | M or V | M |
| Block | 1 or 2 | 1 |
| Support Frequentie | frequent or infrequent | frequent |
| Trial nummer | 0-25 | 0 |

---

**Remember:** Always double-check participant information before starting! ✓
