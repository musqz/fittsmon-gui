![Menu preview](images/menu-800.jpg)
# FittsMon GUI

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Lightweight GUI for FittsMon — captures mouse events on configurable hot edges and triggers/visualizes actions.

## Usage

- Requirements: Python 3
- Run the GUI:

```bash
./fittsmon-gui.py
# or
python3 fittsmon-gui.py
```

- To install helper pieces (icons, desktop files), run:

```bash
./install.sh
```

## License & Contact

This project is released under the MIT License. See `LICENSE` for details.

Author: musqz — linuxbirdtweets@duck.com

## Prerequisites

- Python 3.8+ (or your distribution's default Python 3)
- GTK / PyGObject runtime. On Debian/Ubuntu you can install with:

```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0
# or on Fedora:
sudo dnf install python3-gobject gtk3
```

If you prefer, run from source; system packages are more reliable than `pip` for GTK bindings.

## Install and Run (copy-paste)

Run from source (no install):

```bash
chmod +x fittsmon-gui.py
./fittsmon-gui.py
# or
python3 fittsmon-gui.py
```

Install system-wide (copies files to `$PREFIX`, default `/usr/local`):

```bash
chmod +x install.sh
sudo ./install.sh
```

Uninstall:

```bash
sudo ./uninstall.sh
```

## Configuration

User configuration is saved to `~/.config/fittsmon/fittsmonrc`.
A minimal example (pseudo-INI) might look like:

```
[hotedges]
top-left = show-menu
top-right = none

[general]
timeout = 200
```

Adjust settings after running the GUI; actual keys depend on `fittsmon` daemon configuration.

## Troubleshooting

- If the GUI fails to start, ensure GTK bindings are installed (see Prerequisites).
- Permission errors when installing: use `sudo` for `install.sh`.
- If icons or desktop entries don't show, run `update-icon-caches` or `gtk-update-icon-cache` per your distro.

## Screenshots

There is a sample screenshot in `images/menu-800.jpg` showing the menu UI.

## Contact

Report issues or questions via GitHub issues, or email linuxbirdtweets@duck.com.

