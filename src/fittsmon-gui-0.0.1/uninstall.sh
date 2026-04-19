#!/usr/bin/env bash
set -euo pipefail

# If not root, re-run with sudo
if [ "${EUID:-$(id -u)}" -ne 0 ]; then
  exec sudo "$0" "$@"
fi

PREFIX=${PREFIX:-/usr/local}
BINDIR="$PREFIX/bin"
MANDIR="$PREFIX/share/man/man1"
DESKTOPDIR="$PREFIX/share/applications"

echo "Removing fittsmon-gui from $PREFIX"

if [ -f "$BINDIR/fittsmon-gui" ]; then
  echo "Removing binary: $BINDIR/fittsmon-gui"
  rm -f "$BINDIR/fittsmon-gui"
else
  echo "Binary not found: $BINDIR/fittsmon-gui"
fi

if [ -f "$MANDIR/fittsmon-gui.1.gz" ]; then
  echo "Removing manpage: $MANDIR/fittsmon-gui.1.gz"
  rm -f "$MANDIR/fittsmon-gui.1.gz"
else
  echo "Manpage not found: $MANDIR/fittsmon-gui.1.gz"
fi

if [ -f "$DESKTOPDIR/fittsmon-gui.desktop" ]; then
  echo "Removing desktop file: $DESKTOPDIR/fittsmon-gui.desktop"
  rm -f "$DESKTOPDIR/fittsmon-gui.desktop"
else
  echo "Desktop file not found: $DESKTOPDIR/fittsmon-gui.desktop"
fi

echo "Refreshing system caches (if available)"
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$PREFIX/share/applications" || true
fi
if command -v mandb >/dev/null 2>&1; then
  mandb || true
fi

echo "Removal complete. Files removed from $PREFIX where present."
