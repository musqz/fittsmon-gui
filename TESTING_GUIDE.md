# Testing Guide: Enter/Leave Mode Protection

## Quick Start Testing

### Test 1: Basic Enter Mode Setup
**Objective:** Verify that Enter mode can be set and is tracked

**Steps:**
1. Launch the GUI: `python3 fittsmon-gui.py`
2. Select zone: **TopLeft**
3. Select event: **Enter**
4. Enter command: `notify-send "Entering corner"` or any test command
5. Press Tab or Enter to trigger save

**Expected Results:**
- ✓ Command is saved
- ✓ Status shows "Saved" in green
- ✓ Indicator displays: "🔒 ENTER mode active on TopLeft"
- ✓ Indicator color is red (#D32F2F)

---

### Test 2: Block Other Actions During Enter Mode
**Objective:** Verify that other actions are blocked when Enter mode is active

**Prerequisites:** Test 1 must have completed successfully

**Steps:**
1. With TopLeft zone and Enter mode still active
2. Change event to: **WheelUp**
3. Try to enter command: `amixer set Master 5%+`

**Expected Results:**
- ✓ Command entry remains empty
- ✓ Entry reverts/doesn't accept the command
- ✓ Status shows red error: "Action blocked: enter/leave mode active"
- ✓ Warning box shows: "ACTION BLOCKED: ENTER mode active! Can't set WheelUp..."
- ✓ Other zone actions should work fine (test by switching to TopRight)

---

### Test 3: Block Conflicting Enter/Leave Modes
**Objective:** Verify that Leave can't be set while Enter is active on the same zone

**Prerequisites:** Test 1 must have completed successfully

**Steps:**
1. With TopLeft zone and Enter mode still active
2. Change event to: **Leave**
3. Try to enter command: `notify-send "Leaving corner"`

**Expected Results:**
- ✓ Command entry remains empty
- ✓ Status shows red error: "Action blocked: enter/leave mode active"
- ✓ Warning box shows: "CONFLICT: ENTER mode active! Can't set LEAVE..."
- ✓ Suggestion: "Clear ENTER first or use a different zone"

---

### Test 4: Different Zones Are Independent
**Objective:** Verify that Enter/Leave modes on different zones don't conflict

**Steps:**
1. Keep Enter mode on TopLeft (from previous tests)
2. Switch to zone: **TopRight**
3. Change event to: **Enter**
4. Enter command: `notify-send "Right corner"`

**Expected Results:**
- ✓ Command is accepted and saved
- ✓ No conflicts or warnings
- ✓ Both zones now have Enter mode active (but tracked per-zone)

---

### Test 5: Clear Enter Mode and Test Other Actions
**Objective:** Verify that clearing Enter mode re-enables other actions

**Steps:**
1. Make sure TopLeft has Enter mode active
2. Select zone: **TopLeft**
3. Select event: **Enter**
4. Clear the command (delete all text) and press Tab

**Expected Results:**
- ✓ Command is saved (empty)
- ✓ Indicator changes to: "No enter/leave mode active"
- ✓ Indicator color changes to orange (#FF9800)
- ✓ Console shows: "[ENTER/LEAVE] ENTER mode deactivated"
- ✓ Now you can set WheelUp, LeftButton, etc. on TopLeft

---

### Test 6: Config Persistence
**Objective:** Verify that Enter/Leave mode state persists across GUI restarts

**Steps:**
1. Set Enter mode on TopLeft with command: `notify-send test`
2. Close the GUI completely
3. Reopen the GUI: `python3 fittsmon-gui.py`

**Expected Results:**
- ✓ Indicator immediately shows: "🔒 ENTER mode active on TopLeft"
- ✓ State is preserved from config file
- ✓ Other actions on TopLeft are still blocked
- ✓ Console shows: "[ENTER/LEAVE] Loaded: ENTER mode active..."

---

### Test 7: Leave Mode
**Objective:** Verify that Leave mode works identically to Enter mode

**Steps:**
1. Clear any existing Enter/Leave modes
2. Select zone: **BottomRight**
3. Select event: **Leave**
4. Enter command: `notify-send "Left corner"`

**Expected Results:**
- ✓ Command is saved
- ✓ Indicator shows: "🔒 LEAVE mode active on BottomRight"
- ✓ Try to set WheelDown → blocked with warning
- ✓ Try to set Enter on same zone → blocked with warning
- ✓ Other zones work normally

---

### Test 8: Multiple Zones with Multiple Modes
**Objective:** Verify complex scenario with multiple active modes

**Steps:**
1. Set Enter on TopLeft
2. Set Leave on BottomRight
3. Set WheelUp on TopRight (should work - no conflict)
4. Try to set WheelDown on TopLeft (should be blocked)
5. Try to set LeftButton on BottomRight (should be blocked)

**Expected Results:**
- ✓ Each zone is tracked independently
- ✓ TopRight is unrestricted (no Enter/Leave on it)
- ✓ Attempted conflicts on TopLeft and BottomRight are blocked
- ✓ Proper warnings shown for each conflict

---

## Advanced Testing

### Test 9: Wheel Event Conflicts (Still Works)
**Objective:** Verify that wheel event conflict detection still works

**Steps:**
1. Clear all Enter/Leave modes
2. Select zone: **Left**, event: **WheelUp**
3. Enter command: `amixer set Master 5%+`
4. Switch to event: **WheelUpOnce**
5. Try to enter command: `amixer set Master 3%+`

**Expected Results:**
- ✓ Warning shows: "WheelUpOnce already set! Can't use both..."
- ✓ Wheel conflict handling unaffected by Enter/Leave feature
- ✓ "Clear Conflict" button works

---

### Test 10: Config File Format
**Objective:** Verify config file is saved correctly

**Steps:**
1. Set Enter on TopLeft, Leave on BottomLeft
2. Save config
3. Open config file: `cat ~/.config/fittsmon/fittsmonrc`

**Expected Results:**
```ini
[TopLeft]
Enter=notify-send test
Leave=
...

[BottomLeft]
Enter=
Leave=notify-send leaving
...
```

---

## Troubleshooting Tests

### Test 11: Rapid Command Changes
**Objective:** Verify robustness with rapid changes

**Steps:**
1. Set Enter on TopLeft
2. Rapidly switch between zones
3. Try to quickly change events
4. Rapidly type/delete in command field

**Expected Results:**
- ✓ No crashes
- ✓ State remains consistent
- ✓ Blocks are applied correctly
- ✓ No ghost conflicts

---

### Test 12: Conflicting Config (Manual Edit)
**Objective:** Verify GUI handles manually edited config with both Enter and Leave

**Steps:**
1. Close GUI
2. Manually edit config file to have both Enter and Leave on same zone
3. Restart GUI

**Expected Results:**
- ✓ GUI loads without error
- ✓ Shows one mode (probably the first found - Enter)
- ✓ User can clear one and resume normal operation
- ✓ No crashes

---

## Acceptance Criteria Validation

| Criterion | Test Case | Status |
|-----------|-----------|--------|
| When `leave` is active, only `leave` actions accepted | Test 7, 8 | ✓ |
| When `enter` is active, only `enter` actions accepted | Test 2, 3, 8 | ✓ |
| Other actions disabled/warning shown | Test 2, 3, 5, 8 | ✓ |
| State persists across restarts | Test 6 | ✓ |
| Multiple zones independent | Test 4, 8 | ✓ |
| Existing features unaffected | Test 9 | ✓ |

---

## Test Execution Checklist

- [ ] All 12 tests executed successfully
- [ ] No errors in console
- [ ] Indicator displays correctly
- [ ] Warnings are clear and actionable
- [ ] Config file saves/loads correctly
- [ ] State persists across restarts
- [ ] No interference with existing features
- [ ] Wheel conflicts still work
- [ ] Multiple zones work independently
- [ ] Edge cases handled gracefully

---

## Example Command for Testing

```bash
# Launch GUI for testing
python3 fittsmon-gui.py

# Monitor console output for debugging
# Look for [ENTER/LEAVE] prefix messages:
# [ENTER/LEAVE] ENTER mode activated for HDMI-1/TopLeft
# [ENTER/LEAVE] ACTION BLOCKED: trying WheelUp during ENTER

# Check config after testing
cat ~/.config/fittsmon/fittsmonrc
```

---

## Notes

- Tests should be run in the order listed (some depend on previous setup)
- Use different test commands to visually verify actions (e.g., `notify-send`)
- The GUI will reject problematic commands without saving
- Config file is auto-saved after each successful change
- Console logging uses `[ENTER/LEAVE]` prefix for easy filtering

