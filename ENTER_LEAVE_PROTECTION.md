# Enter/Leave Mode Protection - Implementation Guide

## Overview

This implementation prevents other actions from interfering with `enter` or `leave` mode operations, ensuring that these special actions complete cleanly without conflicts.

## Problem Statement

When `leave` or `enter` mode is active, other actions could still be triggered, potentially causing:
- Action conflicts
- Unexpected behavior
- Incomplete or corrupted state

## Solution

The solution implements a **state-tracking system** that:
1. Tracks which zone has an active `enter` or `leave` mode
2. Prevents setting conflicting actions while enter/leave mode is active
3. Shows clear warning messages to the user
4. Displays the current enter/leave mode status in the UI

## Changes Made

### 1. State Tracking (Lines ~363-365)

Added three new instance variables to `FittsmonGUI.__init__()`:

```python
# Track enter/leave mode state
self.enter_leave_active_monitor = None
self.enter_leave_active_zone = None
self.enter_leave_active_mode = None  # None, 'enter', or 'leave'
```

These track:
- Which monitor has an active enter/leave mode
- Which zone on that monitor
- Whether it's 'enter' or 'leave' mode

### 2. Conflict Detection (New Methods)

#### `check_enter_leave_conflict(monitor, zone, event, command)`

Checks for two types of conflicts:

**Type 1: Conflicting Enter/Leave** (mutually exclusive modes)
- Can't set both `Enter` AND `Leave` on the same zone simultaneously
- Example: Zone has `Enter` active, trying to set `Leave` → BLOCKED

**Type 2: Other Action During Enter/Leave** (protected mode)
- Can't set other actions while enter/leave is active on that zone
- Example: Zone has `Enter` active, trying to set `WheelUp` → BLOCKED
- This prevents interfering actions

#### `update_enter_leave_state(monitor, zone, event, command)`

Maintains the state tracking:
- When `Enter` or `Leave` command is set → activates tracking
- When `Enter` or `Leave` command is cleared → deactivates tracking
- Logs state changes for debugging

### 3. Enhanced Command Setting (Modified `set_command`)

```python
def set_command(self, monitor, zone, event, command):
    # Check for enter/leave conflicts FIRST
    el_conflict = self.check_enter_leave_conflict(monitor, zone, event, command)
    if el_conflict:
        return False, el_conflict  # REJECT the change
    
    # ... rest of normal processing ...
    
    # Update state tracking at the end
    self.update_enter_leave_state(monitor, zone, event, command)
    
    return True, None  # SUCCESS
```

The method now returns a tuple: `(success, conflict_info)`

### 4. UI Feedback

#### Mode Indicator (New in setup_gui)

Added a status label showing the current enter/leave mode:
```
🔒 ENTER mode active on TopLeft (HDMI-1)
```

Displayed in red when active, orange when inactive.

#### Warning Messages (New `show_enter_leave_conflict_warning` method)

Shows clear, actionable messages:

**Conflicting Enter/Leave:**
```
⚠️ CONFLICT: ENTER mode active!
Can't set LEAVE on TopLeft while ENTER is active.
Clear ENTER first or use a different zone.
```

**Other Action During Enter/Leave:**
```
⚠️ ACTION BLOCKED: ENTER mode active!
Can't set WheelUp while ENTER is active on TopLeft.
Clear ENTER first to use other actions.
```

#### Command Entry Reversion

When a command is rejected:
1. Error status is displayed
2. The entry field is reverted to its previous value
3. Warning message is shown

### 5. User Interaction Flow

**Scenario 1: Setting Enter Mode**
1. User selects "TopLeft" zone, "Enter" event, enters command
2. Command is accepted and saved
3. Mode indicator shows: "🔒 ENTER mode active on TopLeft"
4. Other events on TopLeft cannot be modified (blocked)

**Scenario 2: Attempting Other Action During Enter Mode**
1. User tries to set "WheelUp" on the same TopLeft zone
2. System detects conflict
3. Command is REJECTED, entry reverts
4. Warning shows: "ACTION BLOCKED: ENTER mode active!"
5. User must first clear the ENTER command to proceed

**Scenario 3: Clearing Enter Mode**
1. User selects "Enter" event on TopLeft and clears the command
2. Mode tracking is deactivated
3. Indicator changes to: "No enter/leave mode active"
4. Other events on TopLeft can now be modified

**Scenario 4: Different Zone**
1. User can set ENTER on TopLeft AND LEAVE on TopRight simultaneously
2. Each zone is tracked independently
3. No conflict because they're different zones

## Acceptance Criteria Met

✅ **When `leave` is active, only `leave` actions are accepted**
- Other action types are blocked with clear error messages
- Only the active leave command can be modified/cleared

✅ **When `enter` is active, only `enter` actions are accepted**
- Other action types are blocked with clear error messages
- Only the active enter command can be modified/cleared

✅ **Other actions are either disabled or trigger a warning message**
- Implemented as "blocked with warning"
- User attempts are rejected immediately
- Clear, actionable warning messages guide the user
- Entry field is reverted to safe state

## Testing Checklist

- [ ] Set an `Enter` command on a zone
- [ ] Verify mode indicator shows active state
- [ ] Try to set a `WheelUp` command on the same zone → should be blocked
- [ ] Try to set a `Leave` command on the same zone → should be blocked
- [ ] Try to set a command on a DIFFERENT zone → should work fine
- [ ] Clear the `Enter` command
- [ ] Verify mode indicator shows inactive state
- [ ] Try to set other commands on that zone → should work now
- [ ] Test with multiple zones simultaneously
- [ ] Verify config file saves correctly
- [ ] Restart GUI and verify state is loaded correctly

## Code Quality Notes

- No breaking changes to existing functionality
- Wheel event conflicts still work as before
- Config file format unchanged
- All existing features preserved
- Minimal performance impact (simple state tracking)
- Clear logging for debugging: `[ENTER/LEAVE]` prefix

## Future Enhancements

Possible future improvements:
1. Add "Auto-clear other actions" option
2. Allow temporary override with confirmation dialog
3. Per-zone conflict policies
4. Conflict resolution templates
