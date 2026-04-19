# Maintainer: musqz <https://github.com/musqz>
pkgname=fittsmon-gui
pkgver=0.0.1
pkgrel=1
pkgdesc="Lightweight GTK3 GUI to configure fittsmon screen-corner hotspots"
arch=('any')
url="https://github.com/musqz/fittsmon-gui"
license=('GPL-2.0-or-later')
depends=(
    'python'
    'python-gobject'
    'gtk3'
    'fittsmon'
)
optdepends=(
    'arandr: set primary monitor (required for correct config file detection)'
)
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$pkgname-$pkgver"

    # Binary
    install -Dm755 fittsmon-gui.py "$pkgdir/usr/bin/fittsmon-gui"

    # Man page
    install -Dm644 fittsmon-gui.1 "$pkgdir/usr/share/man/man1/fittsmon-gui.1"
    gzip -n "$pkgdir/usr/share/man/man1/fittsmon-gui.1"

    # Desktop entry
    install -Dm644 /dev/stdin "$pkgdir/usr/share/applications/fittsmon-gui.desktop" <<EOF
[Desktop Entry]
Name=fittsmon-gui
Comment=Configure fittsmon screen corner hotspots
Exec=/usr/bin/fittsmon-gui
Terminal=false
Type=Application
Categories=Utility;
Icon=fittsmon-gui
EOF

    # Icon
    if [ -f icons/scalable/apps/fittsmon-gui.svg ]; then
        install -Dm644 icons/scalable/apps/fittsmon-gui.svg \
            "$pkgdir/usr/share/icons/hicolor/scalable/apps/fittsmon-gui.svg"
    fi
}
