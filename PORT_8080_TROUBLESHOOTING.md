# Port 8080 Already in Use - Troubleshooting Guide

## Problem

When starting the AddAttachment application, you see this error:

```
❌ Port 8080 is already in use!
OSError: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8080): 
only one usage of each socket address (protocol/network address/port) is normally permitted
```

## What This Means

Port 8080 is already being used by another process (usually a previous instance of AddAttachment that didn't close properly).

## Quick Solutions

### Solution 1: Wait (Easiest)
Simply wait 30-60 seconds and try again. Windows will automatically release the port.

### Solution 2: Close Previous Instance
1. Open **Task Manager** (Ctrl+Shift+Esc)
2. Look for **python.exe** processes
3. Right-click and select **End Task**
4. Try running AddAttachment again

### Solution 3: Find and Kill the Process

#### Using PowerShell:
```powershell
# Find what's using port 8080
Get-NetTCPConnection -LocalPort 8080

# Kill the process (replace PID with the OwningProcess number from above)
Stop-Process -Id PID -Force
```

#### Using Command Prompt:
```cmd
# Find what's using port 8080
netstat -ano | findstr :8080

# The last column is the PID (Process ID)
# Kill that process (replace 1234 with actual PID)
taskkill /PID 1234 /F
```

### Solution 4: Restart Computer
If nothing else works, restart your computer. This will forcefully release all ports.

## Prevention

### Best Practices

1. **Always close gracefully**: 
   - Don't force-close the application with Task Manager unless necessary
   - Use Ctrl+C or close the window normally
   
2. **Wait before restarting**:
   - After closing AddAttachment, wait 10-15 seconds before restarting
   - This gives Windows time to release the port

3. **Check for running instances**:
   - Before starting AddAttachment, check Task Manager for python.exe
   - Only one instance should run at a time

## Why This Happens

### Common Causes

1. **Ungraceful shutdown**: Application was force-closed or crashed
2. **Multiple instances**: Trying to run two copies at once
3. **Port not released**: Windows hasn't released the port yet (TIME_WAIT state)
4. **Other software**: Another application is using port 8080

### Technical Details

When a TCP server closes, the port enters a TIME_WAIT state for 30-120 seconds to ensure all packets are properly handled. This is normal TCP behavior.

The AddAttachment application now:
- ✅ Uses SO_REUSEADDR to allow faster port reuse
- ✅ Provides clear error messages with solutions
- ✅ Shows helpful commands to find the blocking process

## Advanced Troubleshooting

### Check Port Status

**PowerShell:**
```powershell
Get-NetTCPConnection -LocalPort 8080 | Format-Table -AutoSize
```

Output will show:
- `LocalAddress`: Where the server is listening
- `State`: LISTEN, ESTABLISHED, TIME_WAIT, etc.
- `OwningProcess`: The PID of the process using the port

### Find Process Details

```powershell
# Get process info from PID
Get-Process -Id PID | Format-List *

# Or get just the name
(Get-Process -Id PID).ProcessName
```

### Change the Port (Alternative)

If port 8080 is consistently blocked, you can change it:

1. Edit `conf.yaml`:
```yaml
DATA_CAPTURE:
  WS:
    IP: "0.0.0.0"
    PORT: 8081  # Changed from 8080
```

2. **Important**: Also update Unity's WebSocket connection to use port 8081

## Error Messages Explained

### "Address already in use"
Port 8080 is occupied by another process.

### "Permission denied"
You don't have permission to use that port (usually happens with ports < 1024).

### "Connection refused"
The server isn't running, or Unity is trying to connect to wrong address/port.

### "Connection reset"
Unity disconnected unexpectedly (check Unity console for errors).

## Live Log Messages

The improved GUI now shows helpful messages:

```
✓ WebSocket server starting on 0.0.0.0:8080
✓ Server ready - waiting for Unity connection...
```

If there's an error:
```
❌ Port 8080 is already in use!
⚠ Solution:
  1. Close any other AddAttachment instances
  2. Wait 30-60 seconds for the port to be released
  3. Check Task Manager for 'python.exe' processes
  4. Or try closing and reopening the application
```

## Quick Reference Commands

| Task | Command |
|------|---------|
| Check port 8080 | `Get-NetTCPConnection -LocalPort 8080` |
| Find all python processes | `Get-Process python*` |
| Kill process by PID | `Stop-Process -Id PID -Force` |
| Kill all python processes | `Get-Process python* \| Stop-Process -Force` |
| Check who's using a port | `netstat -ano \| findstr :8080` |

## Summary

**Most Common Solution**: Wait 30-60 seconds between runs or close python.exe in Task Manager.

**The application is working correctly** - the error just means something is still using the port from a previous session.

## Need Help?

If you continue to have port issues:
1. Check the live log in the GUI for specific error messages
2. Run `Get-NetTCPConnection -LocalPort 8080` to see what's using it
3. Try changing to a different port in `conf.yaml`
4. Restart your computer to clear all ports

---

**Remember**: This is a normal networking issue, not a bug in the application. The enhanced error messages now guide you to the solution!
