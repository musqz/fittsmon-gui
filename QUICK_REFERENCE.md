# Quick Reference: Enter/Leave Mode Protection

## What Changed?

Added a **protection system** that prevents other actions from interfering with `enter` and `leave` modes.

## How It Works

### 🔒 Three State Variables
```python
enter_leave_active_monitor = "HDMI-1"      # Which monitor
enter_leave_active_zone = "TopLeft"         # Which zone
enter_leave_active_mode = "enter"           # 'enter', 'leave', or None
```

### 🛑 Two Types of Blocking

**1. Conflicting Modes**
- Can't set both `Enter` AND `Leave` on same zone
- Example: Zone has `Enter` → Can't set `Leave`

**2. Other Actions During Mode**
- Can't set other actions while enter/leave is active
- Example: Zone has `Enter` → Can't set `WheelUp`

### ✨ User Interface Changes

**New Status Indicator:**
```
🔒 ENTER mode active on TopLeft (HDMI-1)    [RED - Active]
No enter/leave mode active                   [ORANGE - Inactive]
```

**New Warning Messages:**
```
⚠️ ACTION BLOCKED: ENTER mode active!
Can't set WheelUp while ENTER is active on TopLeft.
Clear ENTER first to use other actions.
```

## Usage Example

### Setting Up Enter Mode
1. Zone: **TopLeft**
2. Event: **Enter**
3. Command: `notify-send "Entering corner"`
4. ✅ Saved, mode is active

### Trying to Add Other Action
1. Try to set **WheelUp** on TopLeft
2. ❌ BLOCKED: "ACTION BLOCKED: ENTER mode active!"
3. 💡 Solution: Switch to different zone or clear Enter first

### Clearing Enter Mode
1. Zone: **TopLeft**, Event: **Enter**
2. Clear command (delete all text)
3. ✅ Mode deactivates
4. Other actions on TopLeft now work

## Key Features

| Feature | Status | Notes |
|---------|--------|-------|
| Zone-specific tracking | ✅ | Each zone independent |
| Multiple zones supported | ✅ | Can have Enter on TopLeft + Leave on BottomRight |
| State persistence | ✅ | Survives GUI restart |
| Clear error messages | ✅ | User knows exactly what's blocked |
| Auto-revert on rejection | ✅ | Entry field reverts to safe value |
| Backward compatible | ✅ | Old configs work unchanged |

## Testing Checklist

- [ ] Set Enter command → Indicator shows active
- [ ] Try WheelUp → Gets blocked
- [ ] Switch zone → Works normally
- [ ] Clear Enter → Indicator shows inactive
- [ ] Restart GUI → State persists
- [ ] Wheel conflicts still work → Unaffected

## Files to Review

1. **IMPLEMENTATION_SUMMARY.md** - Complete overview
2. **ENTER_LEAVE_PROTECTION.md** - Detailed architecture
3. **STATE_DIAGRAM.md** - Visual state machine
4. **TESTING_GUIDE.md** - 12 test cases

## Console Logging

Watch for `[ENTER/LEAVE]` prefix:
```
[ENTER/LEAVE] Loaded: ENTER mode active on TopLeft
[ENTER/LEAVE] ENTER mode activated for HDMI-1/TopLeft
[ENTER/LEAVE] ENTER mode deactivated
```

## Common Issues

**Q: Why is WheelUp blocked when I have Enter set?**
A: This is intentional protection. Enter/Leave modes are special and must complete without interference. Clear the Enter command first.

**Q: Can I have both Enter and Leave on same zone?**
A: No. They're mutually exclusive for safety. Use different zones if you need both.

**Q: Does this affect wheel event conflicts?**
A: No. Wheel conflict detection (WheelUp vs WheelUpOnce) still works independently.

**Q: What if I manually edit the config file?**
A: The GUI will load and handle it correctly. If both Enter and Leave are set, the first one found is used.

## Code Changes Summary

- **5 new methods** for tracking and conflict detection
- **4 modified methods** to integrate new checks
- **3 new state variables** to track active modes
- **1 new UI label** for mode indicator
- **~200 lines** of code (well-commented)
- **Zero breaking changes** - fully backward compatible

## How It Integrates

```
User modifies command entry
        ↓
on_command_changed() triggered
        ↓
set_command() checks for conflicts
        ↓
check_enter_leave_conflict() returns conflict or None
        ↓
If conflict: reject + show warning + revert entry
If no conflict: save command + update state + update UI
        ↓
update_enter_leave_indicator() shows current status
```

## Performance

- ✅ No background threads
- ✅ No constant monitoring
- ✅ Single string check per command change
- ✅ Minimal memory footprint (3 simple variables)

## Acceptance Criteria Met

✅ **When `leave` is active, only `leave` actions accepted**
✅ **When `enter` is active, only `enter` actions accepted**  
✅ **Other actions are either disabled or trigger warning message**

All requirements fulfilled! 🎉
