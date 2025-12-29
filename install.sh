#!/usr/bin/env bash
set -euo pipefail

# If not root, re-run with sudo
if [ "${EUID:-$(id -u)}" -ne 0 ]; then
  exec sudo "$0" "$@"
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PREFIX=${PREFIX:-/usr/local}
BINDIR="$PREFIX/bin"
MANDIR="$PREFIX/share/man/man1"
DESKTOPDIR="$PREFIX/share/applications"
ICONDIR="$PREFIX/share/icons/hicolor"

# Create target directories
echo "Preparing install directories under $PREFIX"
mkdir -p "$BINDIR" "$MANDIR" "$DESKTOPDIR"
#!/usr/bin/env bash
set -euo pipefail

# If not root, re-run with sudo
if [ "${EUID:-$(id -u)}" -ne 0 ]; then
  exec sudo "$0" "$@"
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PREFIX=${PREFIX:-/usr/local}
BINDIR="$PREFIX/bin"
MANDIR="$PREFIX/share/man/man1"
DESKTOPDIR="$PREFIX/share/applications"
ICONDIR="$PREFIX/share/icons/hicolor"

echo "Preparing install directories under $PREFIX"
mkdir -p "$BINDIR" "$MANDIR" "$DESKTOPDIR"
mkdir -p "$ICONDIR/scalable/apps"
echo "Created: $BINDIR, $MANDIR, $DESKTOPDIR, $ICONDIR/scalable/apps"

# Install the GUI script
if [ -f "$SCRIPT_DIR/fittsmon-gui.py" ]; then
  echo "Installing fittsmon-gui to $BINDIR/fittsmon-gui"
  cp "$SCRIPT_DIR/fittsmon-gui.py" "$BINDIR/fittsmon-gui"
  chmod +x "$BINDIR/fittsmon-gui"
  echo "Installed script: $BINDIR/fittsmon-gui"
else
  echo "Warning: fittsmon-gui.py not found in $SCRIPT_DIR"
fi

# Install man page (gzip compressed)
if [ -f "$SCRIPT_DIR/fittsmon-gui.1" ]; then
  echo "Installing manpage to $MANDIR/fittsmon-gui.1.gz"
  gzip -c "$SCRIPT_DIR/fittsmon-gui.1" > "$MANDIR/fittsmon-gui.1.gz"
  echo "Installed manpage"
else
  echo "No manpage found to install"
fi

# Install .desktop file
echo "Writing desktop file to $DESKTOPDIR/fittsmon-gui.desktop"
cat > "$DESKTOPDIR/fittsmon-gui.desktop" <<EOF
[Desktop Entry]
Name=fittsmon-gui
Comment=Configure fittsmon screen corner hotspots
Exec=$BINDIR/fittsmon-gui
Terminal=false
Type=Application
Categories=Utility;
Icon=input-mouse
EOF
echo "Desktop file installed"

# Install icon (scalable svg if present)
if [ -f "$SCRIPT_DIR/icons/scalable/apps/fittsmon-gui.svg" ]; then
  echo "Installing icon to $ICONDIR/scalable/apps/fittsmon-gui.svg"
  cp "$SCRIPT_DIR/icons/scalable/apps/fittsmon-gui.svg" "$ICONDIR/scalable/apps/fittsmon-gui.svg"
  echo "Icon installed"
else
  echo "No icon found to install"
fi

echo "Updating system caches (if available)"
if command -v update-desktop-database >/dev/null 2>&1; then
  echo "Updating desktop database"
  update-desktop-database "$PREFIX/share/applications" || true
fi
if command -v mandb >/dev/null 2>&1; then
  echo "Updating man database"
  mandb || true
fi

# Update icon cache if available
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  echo "Updating icon cache for $ICONDIR"
  gtk-update-icon-cache -f -t "$ICONDIR" || true
fi

echo "Installation complete. Files installed to:"
echo "  Binary: $BINDIR/fittsmon-gui"
echo "  Desktop file: $DESKTOPDIR/fittsmon-gui.desktop"
echo "  Man page: $MANDIR/fittsmon-gui.1.gz"
echo "  Icon: $ICONDIR/scalable/apps/fittsmon-gui.svg"
echo "If you don't see the app in your application menu immediately, log out/in or run 'update-desktop-database' and 'gtk-update-icon-cache' as root."
