# GUI Responsiveness Fix - Threading Solution

## Problem

After clicking "Start Experiment", the GUI window became unresponsive (frozen) even though the WebSocket server was working correctly and logging to the terminal.

**Symptoms:**
- ❌ GUI window shows "(Not Responding)" in title bar
- ❌ Can't interact with the window (scroll log, click buttons, close window)
- ✅ BUT messages are still logging correctly in the Python terminal
- ✅ Unity connects successfully
- ✅ Data is being received

## Root Cause

### The Threading Problem

The issue was caused by **blocking the main thread**:

```python
# OLD CODE - BLOCKS MAIN THREAD
asyncio.run(start_ws_server(...))  # This blocks!
```

**What was happening:**
1. Tkinter GUI runs on the **main thread**
2. When `asyncio.run()` is called, it **blocks the main thread**
3. While asyncio is running, the GUI event loop can't process:
   - Window redraws
   - Scroll events
   - Log updates
   - Button clicks
   - Window close events
4. GUI appears frozen but the WebSocket server is working fine

### Why Logging Worked in Terminal

The logging was working because:
- The logging handlers write directly to console (not requiring GUI updates)
- The `TextHandler` tries to update the GUI but those updates queue up
- Terminal output bypasses the GUI completely

## Solution

### Run WebSocket in Background Thread

```python
# NEW CODE - NON-BLOCKING
def run_websocket_server():
    """Run the websocket server in its own event loop"""
    asyncio.run(start_ws_server(...))

# Start in background thread (daemon=True means it dies when main program exits)
ws_thread = threading.Thread(target=run_websocket_server, daemon=True)
ws_thread.start()

# GUI continues running on main thread
gui.mainloop()  # This keeps the GUI responsive!
```

**Now:**
1. ✅ WebSocket server runs in **background thread**
2. ✅ GUI runs on **main thread** (where Tkinter requires it)
3. ✅ Both can run simultaneously without blocking each other
4. ✅ GUI stays responsive while WebSocket server handles Unity connection

## Technical Details

### Threading Architecture

```
┌─────────────────────────────────────────────┐
│ MAIN THREAD                                 │
│ ┌─────────────────────────────────────────┐ │
│ │ Tkinter GUI Event Loop                  │ │
│ │ - Updates window                        │ │
│ │ - Handles user input                    │ │
│ │ - Processes log updates                 │ │
│ │ - Redraws widgets                       │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ BACKGROUND THREAD (daemon)                  │
│ ┌─────────────────────────────────────────┐ │
│ │ Asyncio Event Loop                      │ │
│ │ - WebSocket server                      │ │
│ │ - Accepts Unity connections             │ │
│ │ - Sends/receives messages               │ │
│ │ - Logs via TextHandler                  │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Thread Safety

**Logging is thread-safe:**
- Python's logging module is thread-safe by default
- Multiple threads can log without conflicts
- `TextHandler.emit()` uses `text_widget.after()` which schedules GUI updates on the main thread
- This ensures GUI updates happen from the correct thread

**Why daemon=True:**
```python
threading.Thread(target=run_websocket_server, daemon=True)
```
- Daemon threads automatically terminate when main program exits
- Prevents hanging on exit
- No need for explicit cleanup

### Window Close Handling

Added proper cleanup when window is closed:

```python
def on_closing():
    """Handle window close event"""
    logging.info("Window closing...")
    gui.destroy()

gui.protocol("WM_DELETE_WINDOW", on_closing)
```

This ensures:
- ✅ Logs the closure
- ✅ Cleanly destroys the window
- ✅ Daemon thread automatically stops

## Before vs After

### Before (Blocking)

```
User clicks "Start Experiment"
  ↓
asyncio.run() called on main thread
  ↓
Main thread BLOCKED by WebSocket server
  ↓
GUI frozen (can't process events)
  ↓
User sees "(Not Responding)"
  ↓
Can't scroll, click, or close window
  ↓
BUT WebSocket works and logs to terminal ✓
```

### After (Non-Blocking)

```
User clicks "Start Experiment"
  ↓
WebSocket thread started in background
  ↓
Main thread continues immediately
  ↓
GUI stays responsive ✓
  ↓
User can:
  - Scroll through log ✓
  - See real-time updates ✓
  - Close window ✓
  ↓
WebSocket runs in parallel ✓
Unity connects ✓
All logging visible in GUI ✓
```

## Benefits

### For Users
1. ✅ **Responsive GUI** - Can scroll, interact, close window
2. ✅ **Real-time log updates** - See messages as they arrive
3. ✅ **Professional appearance** - No "(Not Responding)" messages
4. ✅ **Better UX** - Window behaves as expected

### For Developers
1. ✅ **Proper threading** - Follows Tkinter + asyncio best practices
2. ✅ **Clean architecture** - Separation of concerns
3. ✅ **Easy to debug** - GUI and WebSocket are independent
4. ✅ **Thread-safe logging** - Automatic via logging module

## Testing

To verify the fix works:

1. **Start the application**
2. **Fill in the form** and click "Start Experiment"
3. **Check responsiveness:**
   - ✅ Window title should NOT say "(Not Responding)"
   - ✅ You can scroll the log window
   - ✅ Log updates appear in real-time
   - ✅ You can close the window at any time
4. **Start Unity** and connect
5. **Verify:**
   - ✅ "Unity connected" appears in log
   - ✅ Messages appear as Unity sends them
   - ✅ Window remains responsive throughout

## Common Threading Patterns

### ❌ DON'T: Block Main Thread
```python
# This freezes the GUI
asyncio.run(server_function())
gui.mainloop()  # Never reached!
```

### ✅ DO: Use Background Thread
```python
# This keeps GUI responsive
thread = threading.Thread(target=lambda: asyncio.run(server_function()), daemon=True)
thread.start()
gui.mainloop()  # GUI runs on main thread
```

### ❌ DON'T: Update GUI from Background Thread
```python
# WRONG - Tkinter isn't thread-safe
def background_task():
    label.config(text="New text")  # Crashes!
```

### ✅ DO: Schedule GUI Updates
```python
# CORRECT - Schedule on main thread
def background_task():
    gui.after(0, lambda: label.config(text="New text"))
```

Our `TextHandler` already does this correctly:
```python
def emit(self, record):
    msg = self.format(record)
    def append():
        self.text_widget.insert(tk.END, msg)
    self.text_widget.after(0, append)  # ✓ Scheduled on main thread
```

## Performance

**Impact:**
- Minimal - thread creation overhead is negligible
- GUI updates are queued efficiently
- No noticeable lag or delay

**Resource Usage:**
- One additional thread (lightweight)
- Daemon thread automatically cleaned up
- No memory leaks

## Summary

### The Fix
Changed from **blocking** (single-threaded) to **non-blocking** (multi-threaded) architecture:

1. **WebSocket server** → Background daemon thread
2. **Tkinter GUI** → Main thread (required by Tkinter)
3. **Logging** → Thread-safe, works from both

### Result
✅ GUI stays responsive throughout entire session
✅ Real-time log updates visible
✅ Professional user experience
✅ Clean shutdown handling

---

**Key Takeaway**: When using Tkinter with asyncio or long-running operations, always run the blocking code in a background thread to keep the GUI responsive!
