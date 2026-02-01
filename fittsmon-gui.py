#!/usr/bin/env python3
"""
fittsmon Configuration GUI - Simple Edition
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import subprocess
import os
import time
from pathlib import Path


# =============================================================================
# TRANSLATIONS
# =============================================================================

TRANSLATIONS = {
    'en': {
        # Window
        'window_title': 'fittsmon',
        'app_title': 'fittsmon action manager',
        'app_subtitle': 'Screen Corner Hotspots',
        
        # Labels
        'monitor': 'Monitor:',
        'select_zone': 'Select Zone:',
        'event': 'Event:',
        'command': 'Command:',
        'primary': '[PRIMARY]',
        
        # Buttons
        'help': '❓ Help',
        'test': '🧪 Test',
        'edit_file': '✏️  Edit File',
        'show_hotspots': '👁️  Show Hotspots',
        'hide_hotspots': '👁️  Hide Hotspots',
        'save': '💾 Save',
        'restart': '⟳ Restart',
        'clear_conflict': '✓ Clear Conflict',
        'close': 'Close',
        
        # Status messages
        'status_ready': 'Ready',
        'status_saved': 'Saved',
        'status_stopping': 'Stopping',
        'status_starting': 'Starting',
        'status_failed_start': 'Failed to start',
        'status_executed': 'Executed',
        'status_opening_editor': 'Opening editor',
        'status_showing_hotspots': 'Showing hotspots on all monitors',
        'status_hotspots_hidden': 'Hotspots hidden',
        'status_enter_command': 'Enter a command first',
        'status_error': 'Error',
        'status_cleared': 'Cleared',
        'status_restarting_closing': 'Restarting daemon before closing',
        'status_daemon_restarted': 'Daemon restarted, closing',
        'status_daemon_failed': 'Warning: Failed to restart daemon',
        
        # Event descriptions
        'event_wheel_up': 'Scroll wheel UP',
        'event_wheel_down': 'Scroll wheel DOWN',
        'event_wheel_up_once': 'Scroll UP once per 2 seconds',
        'event_wheel_down_once': 'Scroll DOWN once per 2 seconds',
        'event_left_button': 'Left mouse button',
        'event_right_button': 'Right mouse button',
        'event_middle_button': 'Middle mouse button',
        'event_enter': 'Mouse enters corner',
        'event_leave': 'Mouse leaves corner',
        
        # Placeholder
        'command_placeholder': 'e.g., amixer -D pulse set Master 5%+',
        
        # Warnings
        'warn_already_set': 'already set!',
        'warn_cant_use_both': "Can't use both",
        'warn_and': 'and',
        'warn_button_conflict_title': 'Warning:',
        'warn_zone_has_buttons': 'This zone has button clicks:',
        'warn_enter_leave_unreliable': 'Enter/Leave events may not work reliably with button clicks in the same zone.',
        'warn_button_fire_unexpected': 'When entering/leaving the corner, button clicks can fire unexpectedly.',
        'warn_zone_has_motion': 'This zone has motion events:',
        'warn_buttons_unreliable': 'Button clicks may not work reliably with Enter/Leave in the same zone.',
        'warn_consider_one_type': 'Consider using only one type of event per zone.',
        
        # Help dialog
        'help_title': 'fittsmon Help',
        'help_text': """<big><b>fittsmon - Screen Corner Actions</b></big>

<b>What is fittsmon?</b>
With fittsmon one can set mouse events on hotcorners and edges.

<b>Zones</b>
There are 8 hotspot zones around the screen: the 4 corners (TopLeft, TopRight, BottomLeft, BottomRight) and 4 edges (TopCenter, Left, Right, BottomCenter).

<b>Events</b>
Each zone can respond to different mouse events:

  <b>Wheel Events:</b>
  • <b>WheelUp / WheelDown</b> - Continuous scrolling (fires repeatedly)
  • <b>WheelUpOnce / WheelDownOnce</b> - Single scroll (2 sec cooldown)
  
  <i>Note: WheelUp conflicts with WheelUpOnce, same for WheelDown. Only one can be active per zone.</i>

  <b>Button Events:</b>
  • <b>LeftButton</b> - Left mouse click
  • <b>RightButton</b> - Right mouse click
  • <b>MiddleButton</b> - Middle mouse click

  <b>Motion Events:</b>
  • <b>Enter</b> - Mouse enters the zone
  • <b>Leave</b> - Mouse leaves the zone
  
  <i>⚠️ Warning: Enter/Leave events conflict with button clicks in the same zone. When you enter or leave a corner, you can't reliably click at the same time.</i>

<b>Multi-Monitor Support</b>
Each monitor can have its own independent hotspot configuration. Select a monitor from the dropdown to configure it.

<b>Tips</b>
• Use <b>Show Hotspots</b> to visualize active zones on all monitors
• Use <b>Test</b> to try your command before saving
• After editing, click <b>Restart</b> to apply changes to the running daemon

<b>Example Commands</b>
• Volume: <tt>amixer -D pulse set Master 5%+</tt>
• Brightness: <tt>brightnessctl set +10%</tt>
• Workspace: <tt>i3-msg workspace next</tt>
• Application: <tt>rofi -show drun</tt>
"""
    },
    
    'es': {
        # Window
        'window_title': 'fittsmon',
        'app_title': 'gestor de acciones fittsmon',
        'app_subtitle': 'Esquinas Activas de Pantalla',
        
        # Labels
        'monitor': 'Monitor:',
        'select_zone': 'Seleccionar Zona:',
        'event': 'Evento:',
        'command': 'Comando:',
        'primary': '[PRINCIPAL]',
        
        # Buttons
        'help': '❓ Ayuda',
        'test': '🧪 Probar',
        'edit_file': '✏️  Editar Archivo',
        'show_hotspots': '👁️  Mostrar Zonas',
        'hide_hotspots': '👁️  Ocultar Zonas',
        'save': '💾 Guardar',
        'restart': '⟳ Reiniciar',
        'clear_conflict': '✓ Limpiar Conflicto',
        'close': 'Cerrar',
        
        # Status messages
        'status_ready': 'Listo',
        'status_saved': 'Guardado',
        'status_stopping': 'Deteniendo',
        'status_starting': 'Iniciando',
        'status_failed_start': 'Error al iniciar',
        'status_executed': 'Ejecutado',
        'status_opening_editor': 'Abriendo editor',
        'status_showing_hotspots': 'Mostrando zonas en todos los monitores',
        'status_hotspots_hidden': 'Zonas ocultas',
        'status_enter_command': 'Ingrese un comando primero',
        'status_error': 'Error',
        'status_cleared': 'Limpiado',
        'status_restarting_closing': 'Reiniciando daemon antes de cerrar',
        'status_daemon_restarted': 'Daemon reiniciado, cerrando',
        'status_daemon_failed': 'Advertencia: Error al reiniciar daemon',
        
        # Event descriptions
        'event_wheel_up': 'Rueda de scroll ARRIBA',
        'event_wheel_down': 'Rueda de scroll ABAJO',
        'event_wheel_up_once': 'Scroll ARRIBA una vez cada 2 segundos',
        'event_wheel_down_once': 'Scroll ABAJO una vez cada 2 segundos',
        'event_left_button': 'Botón izquierdo del ratón',
        'event_right_button': 'Botón derecho del ratón',
        'event_middle_button': 'Botón central del ratón',
        'event_enter': 'El ratón entra en la esquina',
        'event_leave': 'El ratón sale de la esquina',
        
        # Placeholder
        'command_placeholder': 'ej., amixer -D pulse set Master 5%+',
        
        # Warnings
        'warn_already_set': 'ya está configurado!',
        'warn_cant_use_both': 'No se pueden usar ambos',
        'warn_and': 'y',
        'warn_button_conflict_title': 'Advertencia:',
        'warn_zone_has_buttons': 'Esta zona tiene clics de botón:',
        'warn_enter_leave_unreliable': 'Los eventos Enter/Leave pueden no funcionar bien con clics en la misma zona.',
        'warn_button_fire_unexpected': 'Al entrar/salir de la esquina, los clics pueden activarse inesperadamente.',
        'warn_zone_has_motion': 'Esta zona tiene eventos de movimiento:',
        'warn_buttons_unreliable': 'Los clics pueden no funcionar bien con Enter/Leave en la misma zona.',
        'warn_consider_one_type': 'Considere usar solo un tipo de evento por zona.',
        
        # Help dialog
        'help_title': 'Ayuda de fittsmon',
        'help_text': """<big><b>fittsmon - Acciones en Esquinas de Pantalla</b></big>

<b>¿Qué es fittsmon?</b>
Con fittsmon se pueden configurar eventos del ratón en esquinas y bordes activos.

<b>Zonas</b>
Hay 8 zonas activas alrededor de la pantalla: las 4 esquinas (TopLeft, TopRight, BottomLeft, BottomRight) y 4 bordes (TopCenter, Left, Right, BottomCenter).

<b>Eventos</b>
Cada zona puede responder a diferentes eventos del ratón:

  <b>Eventos de Rueda:</b>
  • <b>WheelUp / WheelDown</b> - Scroll continuo (se repite)
  • <b>WheelUpOnce / WheelDownOnce</b> - Scroll único (2 seg de espera)
  
  <i>Nota: WheelUp conflictúa con WheelUpOnce, igual para WheelDown. Solo uno puede estar activo por zona.</i>

  <b>Eventos de Botón:</b>
  • <b>LeftButton</b> - Clic izquierdo
  • <b>RightButton</b> - Clic derecho
  • <b>MiddleButton</b> - Clic central

  <b>Eventos de Movimiento:</b>
  • <b>Enter</b> - El ratón entra en la zona
  • <b>Leave</b> - El ratón sale de la zona
  
  <i>⚠️ Advertencia: Los eventos Enter/Leave conflictúan con clics de botón en la misma zona. Al entrar o salir de una esquina, no se puede hacer clic de forma fiable.</i>

<b>Soporte Multi-Monitor</b>
Cada monitor puede tener su propia configuración independiente. Seleccione un monitor del menú desplegable para configurarlo.

<b>Consejos</b>
• Use <b>Mostrar Zonas</b> para visualizar las zonas activas en todos los monitores
• Use <b>Probar</b> para probar su comando antes de guardar
• Después de editar, haga clic en <b>Reiniciar</b> para aplicar los cambios

<b>Comandos de Ejemplo</b>
• Volumen: <tt>amixer -D pulse set Master 5%+</tt>
• Brillo: <tt>brightnessctl set +10%</tt>
• Espacio de trabajo: <tt>i3-msg workspace next</tt>
• Aplicación: <tt>rofi -show drun</tt>
"""
    },
    
    'pl': {
        # Window
        'window_title': 'fittsmon',
        'app_title': 'menedżer akcji fittsmon',
        'app_subtitle': 'Aktywne Rogi Ekranu',
        
        # Labels
        'monitor': 'Monitor:',
        'select_zone': 'Wybierz Strefę:',
        'event': 'Zdarzenie:',
        'command': 'Polecenie:',
        'primary': '[GŁÓWNY]',
        
        # Buttons
        'help': '❓ Pomoc',
        'test': '🧪 Testuj',
        'edit_file': '✏️  Edytuj Plik',
        'show_hotspots': '👁️  Pokaż Strefy',
        'hide_hotspots': '👁️  Ukryj Strefy',
        'save': '💾 Zapisz',
        'restart': '⟳ Restart',
        'clear_conflict': '✓ Usuń Konflikt',
        'close': 'Zamknij',
        
        # Status messages
        'status_ready': 'Gotowy',
        'status_saved': 'Zapisano',
        'status_stopping': 'Zatrzymywanie',
        'status_starting': 'Uruchamianie',
        'status_failed_start': 'Nie udało się uruchomić',
        'status_executed': 'Wykonano',
        'status_opening_editor': 'Otwieranie edytora',
        'status_showing_hotspots': 'Pokazywanie stref na wszystkich monitorach',
        'status_hotspots_hidden': 'Strefy ukryte',
        'status_enter_command': 'Najpierw wpisz polecenie',
        'status_error': 'Błąd',
        'status_cleared': 'Usunięto',
        'status_restarting_closing': 'Restartowanie demona przed zamknięciem',
        'status_daemon_restarted': 'Demon zrestartowany, zamykanie',
        'status_daemon_failed': 'Uwaga: Nie udało się zrestartować demona',
        
        # Event descriptions
        'event_wheel_up': 'Kółko myszy W GÓRĘ',
        'event_wheel_down': 'Kółko myszy W DÓŁ',
        'event_wheel_up_once': 'Scroll W GÓRĘ raz na 2 sekundy',
        'event_wheel_down_once': 'Scroll W DÓŁ raz na 2 sekundy',
        'event_left_button': 'Lewy przycisk myszy',
        'event_right_button': 'Prawy przycisk myszy',
        'event_middle_button': 'Środkowy przycisk myszy',
        'event_enter': 'Mysz wchodzi w róg',
        'event_leave': 'Mysz opuszcza róg',
        
        # Placeholder
        'command_placeholder': 'np. amixer -D pulse set Master 5%+',
        
        # Warnings
        'warn_already_set': 'już ustawione!',
        'warn_cant_use_both': 'Nie można używać obu',
        'warn_and': 'i',
        'warn_button_conflict_title': 'Uwaga:',
        'warn_zone_has_buttons': 'Ta strefa ma kliknięcia przycisków:',
        'warn_enter_leave_unreliable': 'Zdarzenia Enter/Leave mogą nie działać poprawnie z kliknięciami w tej samej strefie.',
        'warn_button_fire_unexpected': 'Przy wchodzeniu/wychodzeniu z rogu, kliknięcia mogą się aktywować niespodziewanie.',
        'warn_zone_has_motion': 'Ta strefa ma zdarzenia ruchu:',
        'warn_buttons_unreliable': 'Kliknięcia mogą nie działać poprawnie z Enter/Leave w tej samej strefie.',
        'warn_consider_one_type': 'Rozważ użycie tylko jednego typu zdarzenia na strefę.',
        
        # Help dialog
        'help_title': 'Pomoc fittsmon',
        'help_text': """<big><b>fittsmon - Akcje w Rogach Ekranu</b></big>

<b>Co to jest fittsmon?</b>
Za pomocą fittsmon można ustawić zdarzenia myszy na aktywnych rogach i krawędziach.

<b>Strefy</b>
Jest 8 aktywnych stref wokół ekranu: 4 rogi (TopLeft, TopRight, BottomLeft, BottomRight) i 4 krawędzie (TopCenter, Left, Right, BottomCenter).

<b>Zdarzenia</b>
Każda strefa może reagować na różne zdarzenia myszy:

  <b>Zdarzenia Kółka:</b>
  • <b>WheelUp / WheelDown</b> - Ciągłe przewijanie (powtarza się)
  • <b>WheelUpOnce / WheelDownOnce</b> - Pojedyncze przewinięcie (2 sek odstępu)
  
  <i>Uwaga: WheelUp konfliktuje z WheelUpOnce, podobnie WheelDown. Tylko jedno może być aktywne w strefie.</i>

  <b>Zdarzenia Przycisków:</b>
  • <b>LeftButton</b> - Lewy przycisk myszy
  • <b>RightButton</b> - Prawy przycisk myszy
  • <b>MiddleButton</b> - Środkowy przycisk myszy

  <b>Zdarzenia Ruchu:</b>
  • <b>Enter</b> - Mysz wchodzi w strefę
  • <b>Leave</b> - Mysz opuszcza strefę
  
  <i>⚠️ Uwaga: Zdarzenia Enter/Leave konfliktują z kliknięciami w tej samej strefie. Przy wchodzeniu lub wychodzeniu z rogu nie można niezawodnie klikać.</i>

<b>Obsługa Wielu Monitorów</b>
Każdy monitor może mieć własną niezależną konfigurację. Wybierz monitor z listy rozwijanej, aby go skonfigurować.

<b>Wskazówki</b>
• Użyj <b>Pokaż Strefy</b> aby zobaczyć aktywne strefy na wszystkich monitorach
• Użyj <b>Testuj</b> aby wypróbować polecenie przed zapisaniem
• Po edycji kliknij <b>Restart</b> aby zastosować zmiany

<b>Przykładowe Polecenia</b>
• Głośność: <tt>amixer -D pulse set Master 5%+</tt>
• Jasność: <tt>brightnessctl set +10%</tt>
• Pulpit: <tt>i3-msg workspace next</tt>
• Aplikacja: <tt>rofi -show drun</tt>
"""
    }
}


def detect_language():
    """Detect language from $LANG environment variable"""
    lang_env = os.environ.get('LANG', 'en_US.UTF-8')
    lang_code = lang_env.split('_')[0].lower()
    
    if lang_code in TRANSLATIONS:
        print(f"[I18N] Detected language: {lang_code}")
        return lang_code
    
    print(f"[I18N] Language '{lang_code}' not available, using 'en'")
    return 'en'


# Global language setting
CURRENT_LANG = detect_language()


def _(key):
    """Get translated string for key"""
    return TRANSLATIONS[CURRENT_LANG].get(key, TRANSLATIONS['en'].get(key, key))


# =============================================================================
# CLASSES
# =============================================================================

class ConfigParser:
    """Custom config parser that preserves case"""
    
    def __init__(self):
        self.data = {}
    
    def read(self, filepath):
        """Read config file preserving case"""
        self.data = {}
        if not filepath.exists():
            return
        
        current_section = None
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                
                if not line or line.startswith('#'):
                    continue
                
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    self.data[current_section] = {}
                    continue
                
                if '=' in line and current_section:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    self.data[current_section][key] = value
    
    def write(self, filepath, zones, events, monitors):
        """
        Write config file preserving case
        Writes ALL sections for ALL zones with ALL events (even if empty)
        Order: Primary first, then each secondary monitor
        """
        with open(filepath, 'w') as f:
            f.write("# fittsmon Configuration\n")
            f.write("# Generated by fittsmon GUI\n\n")
            
            # Sort monitors: primary first, then others
            primary_mon = None
            secondary_mons = []
            
            for mon in monitors:
                if mon['primary']:
                    primary_mon = mon
                else:
                    secondary_mons.append(mon)
            
            sorted_monitors = []
            if primary_mon:
                sorted_monitors.append(primary_mon)
            sorted_monitors.extend(secondary_mons)
            
            # Write all monitors in order
            for mon in sorted_monitors:
                mon_name = mon['name']
                
                # Write all zones for this monitor
                for zone in zones:
                    # Create section name
                    if mon['primary']:
                        section_name = zone
                    else:
                        section_name = f"{mon_name}-{zone}"
                    
                    f.write(f"[{section_name}]\n")
                    
                    # Write ALL events (even if empty)
                    for event in events:
                        value = self.data.get(section_name, {}).get(event, "")
                        f.write(f"{event}={value}\n")
                    
                    f.write("\n")
    
    def has_section(self, section):
        return section in self.data
    
    def add_section(self, section):
        if section not in self.data:
            self.data[section] = {}
    
    def get(self, section, option, fallback=""):
        try:
            return self.data[section][option]
        except KeyError:
            return fallback
    
    def set(self, section, option, value):
        if section not in self.data:
            self.data[section] = {}
        self.data[section][option] = value
    
    def remove_option(self, section, option):
        if section in self.data and option in self.data[section]:
            del self.data[section][option]


class HotspotWindow(Gtk.Window):
    """Individual hotspot detail window"""
    
    ZONE_INFO = {
        'TopLeft': {'pos': (0, 0), 'emoji': '↖️'},
        'TopCenter': {'pos': (0.5, 0), 'emoji': '⬆️'},
        'TopRight': {'pos': (1, 0), 'emoji': '↗️'},
        'Left': {'pos': (0, 0.5), 'emoji': '⬅️'},
        'Right': {'pos': (1, 0.5), 'emoji': '➡️'},
        'BottomLeft': {'pos': (0, 1), 'emoji': '↙️'},
        'BottomCenter': {'pos': (0.5, 1), 'emoji': '⬇️'},
        'BottomRight': {'pos': (1, 1), 'emoji': '↘️'},
    }
    
    def __init__(self, zone, monitor_name, commands_dict, monitor_geom):
        Gtk.Window.__init__(self, type=Gtk.WindowType.POPUP)
        
        self.zone = zone
        self.monitor_name = monitor_name
        self.commands = commands_dict
        self.monitor_geom = monitor_geom
        
        # Window setup
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_app_paintable(True)
        self.set_type_hint(Gdk.WindowTypeHint.POPUP_MENU)
        
        # Transparency
        screen = Gdk.Screen.get_default()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
        self.connect("draw", self.on_draw)
        
        # Content
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_margin_top(15)
        box.set_margin_bottom(15)
        box.set_margin_start(15)
        box.set_margin_end(15)
        
        # Zone header
        header = Gtk.Label()
        header.set_markup(
            f"<big><b>{self.ZONE_INFO[zone]['emoji']} {zone}</b></big>\n"
            f"<small>{monitor_name}</small>"
        )
        header.set_halign(Gtk.Align.CENTER)
        box.pack_start(header, False, False, 0)
        
        # Commands list
        for event, command in commands_dict.items():
            if command.strip():
                cmd_display = command if len(command) < 30 else command[:27] + "..."
                event_label = Gtk.Label()
                event_label.set_markup(f"<small><b>{event}</b>\n{cmd_display}</small>")
                event_label.set_halign(Gtk.Align.START)
                event_label.set_line_wrap(True)
                event_label.set_max_width_chars(35)
                box.pack_start(event_label, False, False, 0)
        
        self.add(box)
        self.set_size_request(300, -1)
        self.show_all()
        self.position_window()
    
    def position_window(self):
        """Position window at zone location on specific monitor"""
        geom = self.monitor_geom
        
        x_pos, y_pos = self.ZONE_INFO[self.zone]['pos']
        
        window_width = 300
        padding = 20
        
        if x_pos == 0:
            x = geom['x'] + padding
        elif x_pos == 0.5:
            x = geom['x'] + (geom['width'] // 2) - (window_width // 2)
        else:
            x = geom['x'] + geom['width'] - window_width - padding
        
        if y_pos == 0:
            y = geom['y'] + padding
        elif y_pos == 0.5:
            y = geom['y'] + (geom['height'] // 2)
        else:
            y = geom['y'] + geom['height']
        
        self.move(int(x), int(y))
        GLib.idle_add(self._reposition_after_layout, geom, x_pos, y_pos)
    
    def _reposition_after_layout(self, geom, x_pos, y_pos):
        """Reposition window after it's been fully drawn"""
        _, window_height = self.get_size()
        x, _ = self.get_position()
        
        padding = 20
        
        if y_pos == 0:
            y = geom['y'] + padding
        elif y_pos == 0.5:
            y = geom['y'] + (geom['height'] // 2) - (window_height // 2)
        else:
            y = geom['y'] + geom['height'] - window_height - padding
        
        self.move(int(x), int(y))
        return False
    
    def on_draw(self, widget, context):
        """Draw semi-transparent background"""
        context.set_source_rgba(0.1, 0.1, 0.1, 0.88)
        context.paint()
        return False


class MonitorHelper:
    """Helper class to manage monitor information"""
    
    def __init__(self):
        self.monitors = {}
    
    def detect_monitors(self):
        """Detect all monitors and their geometry using modern Gdk.Display API"""
        self.monitors = {}
        display = Gdk.Display.get_default()
        
        n_monitors = display.get_n_monitors()
        for i in range(n_monitors):
            monitor = display.get_monitor(i)
            geom = monitor.get_geometry()
            
            monitor_name = monitor.get_model()
            if not monitor_name:
                monitor_name = f"Monitor-{i}"
            
            if monitor_name in self.monitors:
                monitor_name = f"{monitor_name}-{i}"
            
            self.monitors[monitor_name] = {
                'index': i,
                'x': geom.x,
                'y': geom.y,
                'width': geom.width,
                'height': geom.height
            }
            
            print(f"[MONITOR] {monitor_name}: {geom.x},{geom.y} ({geom.width}x{geom.height})")
        
        return self.monitors
    
    def get_monitor_geom(self, monitor_name):
        """Get geometry for specific monitor"""
        if monitor_name in self.monitors:
            return self.monitors[monitor_name]
        
        if self.monitors:
            return list(self.monitors.values())[0]
        
        return {'x': 0, 'y': 0, 'width': 1920, 'height': 1080}


class ZoneGridWidget(Gtk.Grid):
    """Visual 8-zone grid selector"""
    
    ZONE_INFO = {
        'TopLeft': {'emoji': '↖️', 'pos': (0, 0)},
        'TopCenter': {'emoji': '⬆️', 'pos': (1, 0)},
        'TopRight': {'emoji': '↗️', 'pos': (2, 0)},
        'Left': {'emoji': '⬅️', 'pos': (0, 1)},
        'Right': {'emoji': '➡️', 'pos': (2, 1)},
        'BottomLeft': {'emoji': '↙️', 'pos': (0, 2)},
        'BottomCenter': {'emoji': '⬇️', 'pos': (1, 2)},
        'BottomRight': {'emoji': '↘️', 'pos': (2, 2)},
    }
    
    def __init__(self, zones, callback):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(8)
        self.set_row_spacing(8)
        self.set_halign(Gtk.Align.CENTER)
        
        self.zones = zones
        self.callback = callback
        self.buttons = {}
        self.active_zone = zones[0]
        
        for row in range(3):
            for col in range(3):
                if row == 1 and col == 1:
                    continue
                
                zone = None
                for z, info in self.ZONE_INFO.items():
                    if info['pos'] == (col, row):
                        zone = z
                        break
                
                if zone:
                    btn = Gtk.Button()
                    btn.set_size_request(60, 60)
                    btn.set_label(f"{self.ZONE_INFO[zone]['emoji']}\n{zone.replace('Center', 'C').replace('Left', 'L').replace('Right', 'R')}")
                    btn.set_tooltip_text(zone)
                    btn.connect("clicked", self.on_zone_clicked, zone)
                    
                    self.buttons[zone] = btn
                    self.attach(btn, col, row, 1, 1)
        
        self.update_colors()
        self.show_all()
    
    def on_zone_clicked(self, button, zone):
        self.active_zone = zone
        self.update_colors()
        self.callback(zone)
    
    def update_colors(self):
        for zone, btn in self.buttons.items():
            if zone == self.active_zone:
                btn.get_style_context().remove_class("zone-inactive")
                btn.get_style_context().add_class("zone-active")
            else:
                btn.get_style_context().remove_class("zone-active")
                btn.get_style_context().add_class("zone-inactive")
    
    def set_active_zone(self, zone):
        if zone in self.buttons:
            self.active_zone = zone
            self.update_colors()


class HelpDialog(Gtk.Dialog):
    """Help dialog with usage information"""
    
    def __init__(self, parent):
        Gtk.Dialog.__init__(
            self,
            title=_('help_title'),
            parent=parent,
            flags=0
        )
        self.add_button(_('close'), Gtk.ResponseType.CLOSE)
        self.set_default_size(500, 450)
        
        content = self.get_content_area()
        content.set_margin_top(15)
        content.set_margin_bottom(15)
        content.set_margin_start(15)
        content.set_margin_end(15)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        help_label = Gtk.Label()
        help_label.set_markup(_('help_text'))
        help_label.set_line_wrap(True)
        help_label.set_xalign(0)
        help_label.set_selectable(True)
        
        scroll.add(help_label)
        content.pack_start(scroll, True, True, 0)
        self.show_all()


class FittsmonGUI:
    WHEEL_CONFLICT_PAIRS = {
        'WheelUp': 'WheelUpOnce',
        'WheelUpOnce': 'WheelUp',
        'WheelDown': 'WheelDownOnce',
        'WheelDownOnce': 'WheelDown'
    }
    
    ENTER_LEAVE_EVENTS = {'Enter', 'Leave'}
    BUTTON_EVENTS = {'LeftButton', 'RightButton', 'MiddleButton'}
    
    def __init__(self):
        self.config_dir = Path.home() / ".config/fittsmon"
        self.config_file = self.config_dir / "fittsmonrc"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.monitors = []
        self.config = ConfigParser()
        self.hotspot_windows = []
        self.monitor_helper = MonitorHelper()
        self.daemon_was_running = False
        self.is_restarting = False
        
        self.zones = [
            "TopLeft", "TopCenter", "TopRight",
            "Left", "Right",
            "BottomLeft", "BottomCenter", "BottomRight"
        ]
        
        self.events = [
            "WheelUp", "WheelDown", "WheelUpOnce", "WheelDownOnce",
            "LeftButton", "RightButton", "MiddleButton",
            "Enter", "Leave"
        ]
        
        self.detect_monitors()
        self.load_config()
        self.check_daemon_status()
        self.setup_gui()
        self.setup_styles()
    
    def detect_monitors(self):
        try:
            result = subprocess.run(
                ["xrandr", "--query"],
                capture_output=True, text=True, timeout=5
            )
            
            for line in result.stdout.split('\n'):
                if ' connected' in line:
                    parts = line.split()
                    if len(parts) > 0:
                        monitor_name = parts[0]
                        is_primary = 'primary' in line
                        self.monitors.append({
                            'name': monitor_name,
                            'primary': is_primary
                        })
                        print(f"[DETECT] Monitor: {monitor_name} {'[PRIMARY]' if is_primary else ''}")
        except Exception as e:
            print(f"[ERROR] Monitor detection failed: {e}")
            self.monitors = [{'name': 'default', 'primary': True}]
        
        self.monitor_helper.detect_monitors()
    
    def load_config(self):
        self.config = ConfigParser()
        if self.config_file.exists():
            print(f"[CONFIG] Loading: {self.config_file}")
            self.config.read(self.config_file)
        else:
            print(f"[CONFIG] File not found - will create on save")
    
    def save_config(self):
        try:
            self.config.write(self.config_file, self.zones, self.events, self.monitors)
            print(f"[CONFIG] Saved: {self.config_file}")
            self.set_status(_('status_saved'), error=False)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save config: {e}")
            self.set_status(f"{_('status_error')}: {e}", error=True)
            return False
    
    def get_section_name(self, monitor, zone):
        if monitor == self.monitors[0]['name'] and self.monitors[0]['primary']:
            return zone
        else:
            return f"{monitor}-{zone}"
    
    def get_command(self, monitor, zone, event):
        section = self.get_section_name(monitor, zone)
        return self.config.get(section, event, fallback="")
    
    def set_command(self, monitor, zone, event, command):
        section = self.get_section_name(monitor, zone)
        
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        if command and event in self.WHEEL_CONFLICT_PAIRS:
            conflict_event = self.WHEEL_CONFLICT_PAIRS[event]
            conflict_cmd = self.config.get(section, conflict_event, fallback="")
            if conflict_cmd:
                print(f"[CONFIG] Auto-clearing: {section}.{conflict_event}")
                self.config.remove_option(section, conflict_event)
        
        self.config.set(section, event, command)
        print(f"[CONFIG] Set {section}.{event} = '{command}'")
    
    def check_wheel_conflict(self, event):
        if event not in self.WHEEL_CONFLICT_PAIRS:
            return None
        
        conflict_event = self.WHEEL_CONFLICT_PAIRS[event]
        current_cmd = self.get_command(self.current_monitor, self.current_zone, event)
        conflict_cmd = self.get_command(self.current_monitor, self.current_zone, conflict_event)
        
        if current_cmd == "" and conflict_cmd:
            return {
                'event': event,
                'conflict_event': conflict_event,
                'conflict_value': conflict_cmd,
                'type': 'wheel'
            }
        
        return None
    
    def check_enter_leave_conflict(self, event):
        section = self.get_section_name(self.current_monitor, self.current_zone)
        
        if event in self.ENTER_LEAVE_EVENTS:
            conflicting_buttons = []
            for btn_event in self.BUTTON_EVENTS:
                cmd = self.config.get(section, btn_event, fallback="")
                if cmd:
                    conflicting_buttons.append(btn_event)
            
            if conflicting_buttons:
                return {
                    'event': event,
                    'conflict_events': conflicting_buttons,
                    'type': 'enter_leave'
                }
        
        if event in self.BUTTON_EVENTS:
            conflicting_motion = []
            for motion_event in self.ENTER_LEAVE_EVENTS:
                cmd = self.config.get(section, motion_event, fallback="")
                if cmd:
                    conflicting_motion.append(motion_event)
            
            if conflicting_motion:
                return {
                    'event': event,
                    'conflict_events': conflicting_motion,
                    'type': 'button_motion'
                }
        
        return None
    
    def is_daemon_running(self):
        try:
            result = subprocess.run(
                ["pgrep", "-f", "fittsmon"],
                capture_output=True, text=True, timeout=2
            )
            is_running = result.returncode == 0
            print(f"[DAEMON] Status check: {'Running' if is_running else 'Not running'}")
            return is_running
        except Exception as e:
            print(f"[ERROR] Failed to check daemon status: {e}")
            return False
    
    def check_daemon_status(self):
        self.daemon_was_running = self.is_daemon_running()
        print(f"[DAEMON] Initial status at startup: {'Running' if self.daemon_was_running else 'Not running'}")
    
    def kill_fittsmon(self):
        try:
            subprocess.run(
                ["killall", "fittsmon"],
                capture_output=True, text=True, timeout=3
            )
            print("[DAEMON] Killed fittsmon")
            time.sleep(0.5)
            return True
        except:
            return False
    
    def start_fittsmon(self):
        try:
            cmd = ["fittsmon", "--monitor"] + [m['name'] for m in self.monitors]
            print(f"[DAEMON] Starting: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                close_fds=True,
                preexec_fn=os.setsid if hasattr(os, 'setsid') else None
            )
            
            time.sleep(1)
            
            if process.poll() is None:
                print(f"[DAEMON] Started successfully (PID: {process.pid})")
                return True
            else:
                return False
        except Exception as e:
            print(f"[ERROR] Failed to start fittsmon: {e}")
            return False
    
    def restart_fittsmon(self):
        if self.is_restarting:
            return False
        
        self.is_restarting = True
        self.set_buttons_sensitive(False)
        self.set_status(_('status_stopping'), error=False, busy=True)
        self.spinner.start()
        
        GLib.timeout_add(100, self._restart_phase_kill)
        return True
    
    def _restart_phase_kill(self):
        self.kill_fittsmon()
        GLib.timeout_add(500, self._restart_phase_start)
        return False
    
    def _restart_phase_start(self):
        self.set_status(_('status_starting'), error=False, busy=True)
        GLib.timeout_add(100, self._restart_phase_verify)
        return False
    
    def _restart_phase_verify(self):
        success = self.start_fittsmon()
        self.spinner.stop()
        self.is_restarting = False
        self.set_buttons_sensitive(True)
        
        if success:
            self.set_status(_('status_ready'), error=False)
        else:
            self.set_status(_('status_failed_start'), error=True)
        
        return False
    
    def set_buttons_sensitive(self, sensitive):
        self.restart_btn.set_sensitive(sensitive)
        self.save_btn.set_sensitive(sensitive)
        self.test_btn.set_sensitive(sensitive)
    
    def show_hotspot_windows(self):
        self.close_hotspot_windows()
        
        for mon_name in [m['name'] for m in self.monitors]:
            mon_geom = self.monitor_helper.get_monitor_geom(mon_name)
            
            for zone in self.zones:
                commands_dict = {}
                for event in self.events:
                    cmd = self.get_command(mon_name, zone, event)
                    if cmd.strip():
                        commands_dict[event] = cmd
                
                if commands_dict:
                    hotspot = HotspotWindow(zone, mon_name, commands_dict, mon_geom)
                    self.hotspot_windows.append(hotspot)
    
    def close_hotspot_windows(self):
        for window in self.hotspot_windows:
            window.destroy()
        self.hotspot_windows = []
    
    def setup_styles(self):
        css_provider = Gtk.CssProvider()
        css = """
        .zone-active {
            background-color: #2196F3;
            color: white;
        }
        .zone-inactive {
            background-color: #E0E0E0;
            color: #333333;
        }
        .zone-active:hover {
            background-color: #1976D2;
        }
        .zone-inactive:hover {
            background-color: #BDBDBD;
        }
        .warning-box {
            background-color: #FFF3E0;
            border: 1px solid #FFB74D;
            border-radius: 4px;
            padding: 8px;
            color: #5D4037;
        }
        .warning-box label {
            color: #5D4037;
        }
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def setup_gui(self):
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title(_('window_title'))
        self.window.set_default_size(850, 850)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("delete-event", self.on_window_close)
        
        try:
            self.window.set_icon_name("input-mouse")
        except:
            pass
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        main_box.set_margin_top(15)
        main_box.set_margin_bottom(15)
        main_box.set_margin_start(15)
        main_box.set_margin_end(15)
        self.window.add(main_box)
        
        # Title with help button
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        title = Gtk.Label()
        title.set_markup(f"<big><b>{_('app_title')}</b></big>\n<small>{_('app_subtitle')}</small>")
        title_box.pack_start(title, True, True, 0)
        
        help_btn = Gtk.Button(label=_('help'))
        help_btn.connect("clicked", self.on_help_clicked)
        title_box.pack_end(help_btn, False, False, 0)
        
        main_box.pack_start(title_box, False, False, 0)
        
        # Status with spinner
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        status_box.set_halign(Gtk.Align.CENTER)
        
        self.spinner = Gtk.Spinner()
        status_box.pack_start(self.spinner, False, False, 0)
        
        self.status_label = Gtk.Label()
        self.status_label.set_markup(f"<span size='large' weight='bold' foreground='green'>✓ {_('status_ready')}</span>")
        self.status_label.set_line_wrap(True)
        status_box.pack_start(self.status_label, False, False, 0)
        
        main_box.pack_start(status_box, False, False, 0)
        main_box.pack_start(Gtk.Separator(), False, False, 0)
        
        # Monitor selection
        mon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        mon_box.pack_start(Gtk.Label(label=_('monitor')), False, False, 0)
        self.monitor_combo = Gtk.ComboBoxText()
        for monitor in self.monitors:
            label = f"{monitor['name']} {_('primary') if monitor['primary'] else ''}"
            self.monitor_combo.append_text(label)
        self.monitor_combo.set_active(0)
        self.monitor_combo.connect("changed", self.on_monitor_changed)
        self.current_monitor = self.monitors[0]['name']
        mon_box.pack_start(self.monitor_combo, True, True, 0)
        main_box.pack_start(mon_box, False, False, 0)
        
        # Zone selection
        zone_label = Gtk.Label(label=_('select_zone'))
        zone_label.set_halign(Gtk.Align.START)
        main_box.pack_start(zone_label, False, False, 0)
        
        self.zone_grid = ZoneGridWidget(self.zones, self.on_zone_grid_clicked)
        main_box.pack_start(self.zone_grid, False, False, 0)
        self.current_zone = self.zones[0]
        
        main_box.pack_start(Gtk.Separator(), False, False, 0)
        
        # Event selection
        event_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        event_box.pack_start(Gtk.Label(label=_('event')), False, False, 0)
        self.event_combo = Gtk.ComboBoxText()
        for event in self.events:
            self.event_combo.append_text(event)
        self.event_combo.set_active(0)
        self.event_combo.connect("changed", self.on_event_changed)
        self.current_event = self.events[0]
        event_box.pack_start(self.event_combo, True, True, 0)
        main_box.pack_start(event_box, False, False, 0)
        
        # Event info
        self.info_label = Gtk.Label()
        self.info_label.set_line_wrap(True)
        self.info_label.set_halign(Gtk.Align.START)
        main_box.pack_start(self.info_label, False, False, 0)
        
        # Command input
        cmd_label = Gtk.Label(label=_('command'))
        cmd_label.set_halign(Gtk.Align.START)
        main_box.pack_start(cmd_label, False, False, 0)
        self.command_entry = Gtk.Entry()
        self.command_entry.set_placeholder_text(_('command_placeholder'))
        self.command_entry.connect("changed", self.on_command_changed)
        main_box.pack_start(self.command_entry, False, False, 0)
        
        # Warning box (wheel conflicts)
        self.warning_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.warning_label = Gtk.Label()
        self.warning_label.set_line_wrap(True)
        self.warning_label.set_halign(Gtk.Align.START)
        self.warning_box.pack_start(self.warning_label, False, False, 0)
        
        self.auto_clear_btn = Gtk.Button(label=_('clear_conflict'))
        self.auto_clear_btn.connect("clicked", self.on_auto_clear_clicked)
        self.warning_box.pack_start(self.auto_clear_btn, False, False, 0)
        main_box.pack_start(self.warning_box, False, False, 0)
        
        # Enter/Leave warning box
        self.enter_leave_warning_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.enter_leave_warning_box.get_style_context().add_class("warning-box")
        
        self.enter_leave_warning_label = Gtk.Label()
        self.enter_leave_warning_label.set_line_wrap(True)
        self.enter_leave_warning_label.set_halign(Gtk.Align.START)
        self.enter_leave_warning_box.pack_start(self.enter_leave_warning_label, False, False, 0)
        main_box.pack_start(self.enter_leave_warning_box, False, False, 0)
        
        self.update_command_display()
        
        # Action buttons
        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        self.test_btn = Gtk.Button(label=_('test'))
        self.test_btn.connect("clicked", self.on_test_clicked)
        action_box.pack_start(self.test_btn, True, True, 0)
        
        edit_btn = Gtk.Button(label=_('edit_file'))
        edit_btn.connect("clicked", self.on_edit_clicked)
        action_box.pack_start(edit_btn, True, True, 0)
        main_box.pack_start(action_box, False, False, 0)
        
        # Hotspot toggle
        hotspot_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.hotspot_toggle_btn = Gtk.ToggleButton(label=_('show_hotspots'))
        self.hotspot_toggle_btn.connect("clicked", self.on_hotspot_toggled)
        hotspot_box.pack_start(self.hotspot_toggle_btn, True, True, 0)
        main_box.pack_start(hotspot_box, False, False, 0)
        
        # Save & Restart
        sr_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        self.save_btn = Gtk.Button(label=_('save'))
        self.save_btn.set_size_request(-1, 40)
        self.save_btn.get_style_context().add_class("suggested-action")
        self.save_btn.connect("clicked", self.on_save_clicked)
        sr_box.pack_start(self.save_btn, True, True, 0)
        
        self.restart_btn = Gtk.Button(label=_('restart'))
        self.restart_btn.set_size_request(-1, 40)
        self.restart_btn.get_style_context().add_class("destructive-action")
        self.restart_btn.connect("clicked", self.on_restart_clicked)
        sr_box.pack_start(self.restart_btn, True, True, 0)
        main_box.pack_start(sr_box, False, False, 0)
        
        self.window.show_all()
        self.warning_box.hide()
        self.enter_leave_warning_box.hide()
    
    def on_window_close(self, widget, event):
        print("[GUI] Window close requested")
        self.close_hotspot_windows()
        
        if self.daemon_was_running:
            print("[GUI] Daemon was running before GUI started, checking status...")
            if not self.is_daemon_running():
                print("[GUI] Daemon is not running! Restarting...")
                self.set_status(_('status_restarting_closing'), error=False)
                if self.start_fittsmon():
                    time.sleep(2)
                    if self.is_daemon_running():
                        print("[GUI] Daemon successfully restarted")
                        self.set_status(_('status_daemon_restarted'), error=False)
                    else:
                        print("[GUI] Failed to restart daemon!")
                        self.set_status(_('status_daemon_failed'), error=True)
                        time.sleep(2)
            else:
                print("[GUI] Daemon is still running, closing cleanly")
        else:
            print("[GUI] Daemon was not running before, not restarting")
        
        Gtk.main_quit()
        return False
    
    def on_zone_grid_clicked(self, zone):
        self.current_zone = zone
        self.update_command_display()
    
    def get_event_info(self, event):
        info_map = {
            'WheelUp': _('event_wheel_up'),
            'WheelDown': _('event_wheel_down'),
            'WheelUpOnce': _('event_wheel_up_once'),
            'WheelDownOnce': _('event_wheel_down_once'),
            'LeftButton': _('event_left_button'),
            'RightButton': _('event_right_button'),
            'MiddleButton': _('event_middle_button'),
            'Enter': _('event_enter'),
            'Leave': _('event_leave')
        }
        return info_map.get(event, "")
    
    def update_command_display(self):
        cmd = self.get_command(self.current_monitor, self.current_zone, self.current_event)
        
        self.command_entry.handler_block_by_func(self.on_command_changed)
        self.command_entry.set_text(cmd)
        self.command_entry.handler_unblock_by_func(self.on_command_changed)
        
        self.info_label.set_markup(f"<small>{self.get_event_info(self.current_event)}</small>")
        self.zone_grid.set_active_zone(self.current_zone)
        self.show_conflict_warnings()
    
    def show_conflict_warnings(self):
        wheel_conflict = self.check_wheel_conflict(self.current_event)
        
        if wheel_conflict:
            msg = (
                f"⚠️  <b>{wheel_conflict['conflict_event']}</b> {_('warn_already_set')}\n"
                f"{_('warn_cant_use_both')} <b>{wheel_conflict['event']}</b> {_('warn_and')} <b>{wheel_conflict['conflict_event']}</b>"
            )
            self.warning_label.set_markup(msg)
            self.warning_box.show_all()
        else:
            self.warning_box.hide()
        
        enter_leave_conflict = self.check_enter_leave_conflict(self.current_event)
        
        if enter_leave_conflict:
            conflict_list = ", ".join(f"<b>{e}</b>" for e in enter_leave_conflict['conflict_events'])
            
            if enter_leave_conflict['type'] == 'enter_leave':
                msg = (
                    f"<span foreground='#5D4037'>⚠️  <b>{_('warn_button_conflict_title')}</b> {_('warn_zone_has_buttons')} {conflict_list}\n"
                    f"<small>{_('warn_enter_leave_unreliable')}\n"
                    f"{_('warn_button_fire_unexpected')}</small></span>"
                )
            else:
                msg = (
                    f"<span foreground='#5D4037'>⚠️  <b>{_('warn_button_conflict_title')}</b> {_('warn_zone_has_motion')} {conflict_list}\n"
                    f"<small>{_('warn_buttons_unreliable')}\n"
                    f"{_('warn_consider_one_type')}</small></span>"
                )
            
            self.enter_leave_warning_label.set_markup(msg)
            self.enter_leave_warning_box.show_all()
        else:
            self.enter_leave_warning_box.hide()
    
    def on_monitor_changed(self, widget):
        idx = self.monitor_combo.get_active()
        if idx >= 0:
            self.current_monitor = self.monitors[idx]['name']
            self.update_command_display()
    
    def on_event_changed(self, widget):
        idx = self.event_combo.get_active()
        if idx >= 0:
            self.current_event = self.events[idx]
            self.update_command_display()
    
    def on_command_changed(self, widget):
        command = self.command_entry.get_text()
        self.set_command(self.current_monitor, self.current_zone, self.current_event, command)
        self.save_config()
        self.show_conflict_warnings()
    
    def on_auto_clear_clicked(self, widget):
        conflict = self.check_wheel_conflict(self.current_event)
        if conflict:
            section = self.get_section_name(self.current_monitor, self.current_zone)
            self.config.remove_option(section, conflict['conflict_event'])
            self.save_config()
            self.show_conflict_warnings()
            self.set_status(f"{_('status_cleared')} {conflict['conflict_event']}", error=False)
    
    def on_test_clicked(self, widget):
        command = self.command_entry.get_text()
        if not command:
            self.set_status(_('status_enter_command'), error=True)
            return
        try:
            subprocess.Popen(command, shell=True)
            self.set_status(_('status_executed'), error=False)
        except Exception as e:
            self.set_status(f"{_('status_error')}: {e}", error=True)
    
    def on_edit_clicked(self, widget):
        try:
            subprocess.Popen(["xdg-open", str(self.config_file)])
            self.set_status(_('status_opening_editor'), error=False)
        except Exception as e:
            self.set_status(f"{_('status_error')}: {e}", error=True)
    
    def on_hotspot_toggled(self, widget):
        if widget.get_active():
            self.show_hotspot_windows()
            self.hotspot_toggle_btn.set_label(_('hide_hotspots'))
            self.set_status(_('status_showing_hotspots'), error=False)
        else:
            self.close_hotspot_windows()
            self.hotspot_toggle_btn.set_label(_('show_hotspots'))
            self.set_status(_('status_hotspots_hidden'), error=False)
    
    def on_save_clicked(self, widget):
        self.save_config()
    
    def on_restart_clicked(self, widget):
        self.restart_fittsmon()
    
    def on_help_clicked(self, widget):
        dialog = HelpDialog(self.window)
        dialog.run()
        dialog.destroy()
    
    def set_status(self, message, error=False, busy=False):
        if busy:
            color = "orange"
            symbol = "⏳"
        elif error:
            color = "red"
            symbol = "✗"
        else:
            color = "green"
            symbol = "✓"
        
        self.status_label.set_markup(
            f"<span size='large' weight='bold' foreground='{color}'>"
            f"{symbol} {message}"
            f"</span>"
        )
    
    def run(self):
        print("\n" + "="*50)
        print("  fittsmon")
        print("="*50 + "\n")
        Gtk.main()


if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # Allow Ctrl+C to exit cleanly
    app = FittsmonGUI()
    app.run()
