TARGET  = fittsmon-gui

# Installation layout — all overridable on the command line.
# DESTDIR is used by package managers to stage files before final install.
DESTDIR    =
PREFIX     = /usr/local
BINDIR     = $(PREFIX)/bin
MANDIR     = $(PREFIX)/share/man/man1
DATADIR    = $(PREFIX)/share/$(TARGET)
APPSDIR    = $(PREFIX)/share/applications
ICONDIR    = $(PREFIX)/share/icons/hicolor
LICENSEDIR = $(PREFIX)/share/licenses/$(TARGET)

SCRIPT   = fittsmon-gui.py
MAN_PAGE = fittsmon-gui.1
ICON_SVG = icons/scalable/apps/fittsmon-gui.svg

# -----------------------------------------------------------------------

all:
	@echo "Nothing to build. Run 'make install' to install."

install:
	install -Dm755 $(SCRIPT)   $(DESTDIR)$(BINDIR)/$(TARGET)
	install -Dm644 $(MAN_PAGE) $(DESTDIR)$(MANDIR)/$(MAN_PAGE)
	gzip -nf                   $(DESTDIR)$(MANDIR)/$(MAN_PAGE)
	install -Dm644 /dev/stdin  $(DESTDIR)$(APPSDIR)/$(TARGET).desktop <<EOF
[Desktop Entry]
Name=fittsmon-gui
Comment=Configure fittsmon screen corner hotspots
Exec=$(BINDIR)/$(TARGET)
Terminal=false
Type=Application
Categories=Utility;
Icon=$(TARGET)
EOF
	@if [ -f $(ICON_SVG) ]; then \
	  install -Dm644 $(ICON_SVG) \
	    $(DESTDIR)$(ICONDIR)/scalable/apps/$(TARGET).svg; \
	fi
	install -Dm644 LICENSE     $(DESTDIR)$(LICENSEDIR)/LICENSE
	@echo ""
	@echo "Installation complete."
	@echo "  Binary  : $(DESTDIR)$(BINDIR)/$(TARGET)"
	@echo "  Man     : $(DESTDIR)$(MANDIR)/$(MAN_PAGE).gz"
	@echo "  Desktop : $(DESTDIR)$(APPSDIR)/$(TARGET).desktop"
	@echo "  Icon    : $(DESTDIR)$(ICONDIR)/scalable/apps/$(TARGET).svg"

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/$(TARGET)
	rm -f $(DESTDIR)$(MANDIR)/$(MAN_PAGE).gz
	rm -f $(DESTDIR)$(APPSDIR)/$(TARGET).desktop
	rm -f $(DESTDIR)$(ICONDIR)/scalable/apps/$(TARGET).svg
	rm -f $(DESTDIR)$(LICENSEDIR)/LICENSE
	@echo "Uninstall complete."

.PHONY: all install uninstall
