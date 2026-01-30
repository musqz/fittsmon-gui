# Enter/Leave Mode Protection - State Diagram

## State Tracking Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Global Application State                 │
│  (Tracks which zone has active enter/leave mode, if any)    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  enter_leave_active_monitor = "HDMI-1"                      │
│  enter_leave_active_zone    = "TopLeft"                     │
│  enter_leave_active_mode    = "enter"  (or "leave"/None)    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
           ↑
           │ tracks
           │
    ┌──────────────┐
    │  User Action │  (Setting/clearing a command)
    └──────────────┘
           │
           ↓
    ┌──────────────────────────────────┐
    │  check_enter_leave_conflict()    │
    │  (Detect conflicts)              │
    └──────────────────────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ↓             ↓
  YES           NO
 (Block)      (Allow)
    │             │
    │             ↓
    │      ┌─────────────────────┐
    │      │  Set Command        │
    │      │  Save to Config     │
    │      └─────────────────────┘
    │             │
    │             ↓
    │      ┌──────────────────────────────┐
    │      │  update_enter_leave_state()  │
    │      │  (Update tracking)           │
    │      └──────────────────────────────┘
    │             │
    └─────────────┤
                  │
                  ↓
    ┌──────────────────────────────────┐
    │  update_enter_leave_indicator()  │
    │  (Update UI display)             │
    └──────────────────────────────────┘
```

## Conflict Detection Logic

```
User tries to set: command on (monitor, zone, event)
                        │
                        ↓
        ┌───────────────────────────────┐
        │ Is this event Enter or Leave? │
        └───────────────────────────────┘
           │                        │
          YES                       NO (e.g., WheelUp, LeftButton)
           │                        │
           ↓                        ↓
    ┌──────────────┐        ┌──────────────────────┐
    │ Is command   │        │ Is enter/leave       │
    │ being set    │        │ active on this zone? │
    │ (not empty)? │        └──────────────────────┘
    └──────────────┘           │              │
         │        │           YES             NO
        YES      NO            │              │
         │       │             ↓              ↓
         ↓       │      ┌──────────────┐  ALLOW
    ┌────────┐  │      │ BLOCK:       │
    │ Is     │  │      │ Other action │
    │ it     │  │      │ not permitted│
    │ same   │  │      │ during       │
    │ mode   │  │      │ enter/leave  │
    │ being  │  │      └──────────────┘
    │ active?│  │
    └────────┘  │
        │    │  │
       NO   YES │
        │    │  │
        ↓    ↓  ↓
    ┌────┐ ├─ ALLOW ─┐
    │    │ │ (Modify)│
    │    │ └────────┘
    │    │
    │    ├─ ALLOW (Clear)
    │    │
    │    │
    │    └─ DEACTIVATE tracking
    │
    └─ BLOCK:
       Can't have both
       Enter AND Leave
       on same zone
```

## Example: Three Scenarios

### Scenario A: Clean Enter Mode Setup
```
Initial State:
  enter_leave_active_mode = None

Step 1: User sets Enter="notify-send entering"
  → Checks: Is this Enter/Leave? YES
  → Checks: Is mode being set? YES (command not empty)
  → Checks: Is same mode active? NO (mode is None)
  → ACTION: ALLOW
  → Update: enter_leave_active_mode = "enter"
  → Status: "🔒 ENTER mode active on TopLeft"

Current State:
  enter_leave_active_monitor = "HDMI-1"
  enter_leave_active_zone = "TopLeft"
  enter_leave_active_mode = "enter"
```

### Scenario B: Blocked Other Action
```
Current State:
  enter_leave_active_mode = "enter"
  enter_leave_active_zone = "TopLeft"

Step 2: User tries to set WheelUp="amixer..."
  → Checks: Is this Enter/Leave? NO (it's WheelUp)
  → Checks: Is enter/leave active on this zone? YES
  → ACTION: BLOCK
  → Warning: "ACTION BLOCKED: ENTER mode active!"
  → Revert command entry to previous value

Current State:
  [No change - command rejected]
```

### Scenario C: Clear Enter Mode
```
Current State:
  enter_leave_active_mode = "enter"

Step 3: User clears Enter command (empty)
  → Checks: Is this Enter/Leave? YES
  → Checks: Is command being set? NO (empty)
  → Checks: Is same mode active? YES
  → ACTION: DEACTIVATE tracking
  → Update: enter_leave_active_mode = None
  → Status: "No enter/leave mode active"

Final State:
  enter_leave_active_mode = None
  enter_leave_active_monitor = None
  enter_leave_active_zone = None
```

## Per-Zone Independence

```
Monitor: HDMI-1

Zone: TopLeft          Zone: TopCenter
├─ Enter: active       ├─ Enter: (none)
├─ Leave: (blocked)    ├─ Leave: active ← Independent!
├─ WheelUp: (blocked)  ├─ WheelUp: (blocked)
└─ Other: (blocked)    └─ Other: (blocked)

Zone: TopRight         Zone: Right
├─ Enter: (none)       ├─ Enter: (none)
├─ Leave: (none)       ├─ Leave: (none)
├─ WheelUp: ALLOWED    ├─ WheelUp: ALLOWED ← Can set freely
└─ Other: ALLOWED      └─ Other: ALLOWED
```

Each zone tracks its own enter/leave mode independently!

## UI Indicator Display

```
┌─────────────────────────────────────────────┐
│         fittsmon action manager             │
├─────────────────────────────────────────────┤
│  ✓ Ready                                    │
│                                             │
│  🔒 ENTER mode active on TopLeft (HDMI-1)  │ ← Shows when active
│                                             │   Red color
│  ─────────────────────────────────────────  │
│                                             │
│  Monitor: HDMI-1  ▼                         │
│                                             │
│  Select Zone:                               │
│     ↖️  ⬆️  ↗️                               │
│     ⬅️  ❌  ➡️                               │
│     ↙️  ⬇️  ↘️                               │
│                                             │
│  Event: Enter  ▼                            │
│                                             │
│  Command: notify-send entering             │
│                                             │
│  ⚠️  CONFLICT: LEAVE already active!        │ ← Shows when blocked
│      Can't set ENTER...                     │
│                                             │
└─────────────────────────────────────────────┘
```

## Configuration File State Persistence

```
Config File: ~/.config/fittsmon/fittsmonrc

[TopLeft]
Enter=notify-send entering
Leave=
WheelUp=
...

[TopCenter]
Enter=
Leave=notify-send leaving
WheelUp=
...

When GUI starts:
1. Load config file
2. Scan all zones for Enter/Leave commands
3. If ANY Enter/Leave command found, activate that zone's tracking
4. Display indicator
```

This ensures state persists across GUI restarts!
