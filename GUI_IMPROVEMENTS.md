# GUI Improvements - AddAttachment Application

## Overview
The AddAttachment GUI has been significantly improved with better layout, formatting, and a live activity log window for researchers to monitor the session in real-time.

## New Features

### 1. **Two-Panel Layout**
- **Left Panel**: Participant information input form
- **Right Panel**: Live activity log showing real-time events
- Both panels are resizable and the window can be expanded

### 2. **Live Activity Log**
- Real-time logging of all application events
- Color-coded messages:
  - **Black**: General information
  - **Green**: Success messages (marked with ✓)
  - **Orange**: Warnings (marked with ⚠)
  - **Red**: Errors (marked with ❌)
  - **Gray**: Debug information
- Timestamps for each log entry
- Auto-scrolling to show latest events
- Clear log button to reset the log window

### 3. **Improved Form Layout**
- Better visual organization with sections
- Clear labels with bold formatting for required fields
- Inline validation with immediate feedback:
  - **Age**: Must be 9-13 years old
  - **Trial Number**: Must be 0-25 (default: 0)
- Visual checkmarks (✓) when values are valid
- Error messages displayed inline with red color

### 4. **Status Bar**
- Bottom status bar showing current application state
- Color-coded status messages:
  - Ready state
  - Validation in progress
  - Success/Error states

### 5. **Enhanced Logging Throughout Application**
Researchers can now monitor:
- GUI startup and initialization
- Form validation progress
- Participant data being processed
- Directory creation and file operations
- Support figure selection
- WebSocket server status:
  - Server starting
  - Waiting for Unity connection
  - Unity connection established
  - Data being sent to/from Unity
  - Connection issues and errors

## Window Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ AddAttachment - Participant Data Entry                          │
├──────────────────────────────┬──────────────────────────────────┤
│  Participant Information     │  Live Activity Log               │
│  ────────────────────────    │  ─────────────────               │
│                              │                                  │
│  Naam speler: [         ]    │  [10:23:15] GUI started         │
│  Identificatie: [       ]    │  [10:23:15] Fill in info...     │
│  Leeftijd (9-13): [  ] ✓     │  [10:23:45] Validating...       │
│  ──────────────────────       │  [10:23:45] ✓ All validated    │
│  Geslacht: (•) M  ( ) V      │  [10:23:46] Creating dirs...    │
│  Contingentie: ( ) 20% (•) 80│  [10:23:46] ✓ Data dir created │
│  Trial Block: (•) 1  ( ) 2   │  [10:23:47] Selected mama...    │
│  Support Freq: (•) Freq      │  [10:23:48] Starting WS...      │
│  ──────────────────────       │  [10:23:48] Waiting Unity...   │
│  Trial nummer: [0]           │  [10:23:50] 🔌 Unity connected │
│    (optioneel, standaard=0)  │  [10:23:50] ✓ Sent message 1   │
│                              │  [10:23:50] 📡 Listening...     │
│  [  💾 Save & Continue  ]    │  [Clear Log]                    │
│                              │                                  │
├──────────────────────────────┴──────────────────────────────────┤
│ Ready | Fill in participant information to continue             │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Details

### New Files
- **`utils/GUI_improved.py`**: Enhanced GUI class with logging capabilities
  - `TextHandler`: Custom logging handler for Tkinter
  - `ImprovedGUI`: Main GUI class with two-panel layout

### Modified Files
- **`addattachment.py`**: 
  - Now uses `ImprovedGUI` instead of `GUI`
  - Enhanced logging messages throughout the flow
  - Better error messages with icons (✓, ❌, ⚠, 🔌, 📡, etc.)

- **`websocket/WebSocketServer.py`**:
  - Added connection status logging
  - Message send/receive logging
  - Better error messages with troubleshooting hints

### Color Scheme
The log uses semantic colors:
- Success: Green
- Errors: Red
- Warnings: Orange
- Info: Black
- Debug: Gray

### Icons Used in Log
- ✓ : Success/Completed
- ❌ : Error/Failed
- ⚠ : Warning
- 🔌 : Connection established
- 📡 : Communication/Listening
- 📤 : Sending data
- 📨 : Receiving data
- 📋 : Processing data
- 📁 : File/Directory operations
- 👤 : User interaction
- 💾 : Saving

## Usage

### For Researchers
1. **Fill in the form** on the left with participant information
2. **Monitor the log** on the right for real-time status
3. **Look for**:
   - Green ✓ checkmarks indicating successful operations
   - "Unity connected" message when Unity establishes connection
   - Any red ❌ errors that need attention
4. **Use Clear Log** button to reset the log if it gets too long

### Common Log Messages

#### Startup Phase
```
═══════════════════════════════════════════
  AddAttachment - Starting Application
═══════════════════════════════════════════
AddAttachment GUI started
Please fill in participant information
```

#### Validation Phase
```
─────────────────────────────────────────────
📋 Processing participant information...
✓ Configuration loaded
✓ Player session created: TestChild (ID: 001)
```

#### Directory Setup
```
📁 Creating data directories...
✓ Data directory: c:\AddaGit\Python\python\data\2025_01_20__14_30
✓ Player configuration saved
```

#### Support Figure Selection
```
─────────────────────────────────────────────
👤 Selecting starting support figure...
✓ Selected: Mama figure (brown hair, green shirt)
```

#### WebSocket Connection
```
─────────────────────────────────────────────
🌐 Starting WebSocket server...
   Listening on localhost:8080
   Waiting for Unity to connect...
✓ WebSocket server started successfully
✓ Server ready - waiting for Unity connection...
🔌 Unity connected from 127.0.0.1:52341
📤 Sending 2 initialization message(s) to Unity...
   ✓ Sent message 1: ['type', 'playerValues']
   ✓ Sent message 2: ['websocketMessage', 'support']
✓ All initialization data sent to Unity
─────────────────────────────────────────────
📡 Listening for messages from Unity...
📨 Received: {'trialNumber': 0, 'phase': 'init', ...}
```

## Benefits

### For Researchers
- **Transparency**: See exactly what's happening at each step
- **Debugging**: Quickly identify issues with clear error messages
- **Monitoring**: Track Unity connection status in real-time
- **Documentation**: Log serves as a record of the session

### For Development
- **Debugging**: Easier to trace issues with detailed logging
- **Testing**: Visual feedback during testing
- **Documentation**: Self-documenting through log messages

## Window Size
- **Default**: 900x700 pixels
- **Minimum**: 800x600 pixels
- **Resizable**: Yes, both width and height
- **Position**: Automatically centered on screen

## Future Enhancements (Optional)
- Export log to file
- Filter log by message type (info/warning/error)
- Search within log
- Session timer display
- Participant count for the day
- Quick access to data directory

## Backward Compatibility
The original `GUI.py` file is still available and unchanged. The application can be reverted to the old GUI by changing the import in `addattachment.py` from:
```python
from utils.GUI_improved import ImprovedGUI
```
back to:
```python
from utils.GUI import GUI
```
and changing:
```python
gui = ImprovedGUI()
```
back to:
```python
gui = GUI()
```
