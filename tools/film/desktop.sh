#!/bin/bash
export DISPLAY=:1
Xvfb :1 -screen 0 1920x1080x24 -nolisten tcp >/tmp/xvfb.log 2>&1 &
for i in $(seq 1 50); do xdpyinfo >/dev/null 2>&1 && break; sleep 0.2; done
eval "$(dbus-launch --sh-syntax)"
export DBUS_SESSION_BUS_ADDRESS
echo "export DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS DISPLAY=:1" > /tmp/session.env
xfconf-query -c xsettings -p /Net/ThemeName -n -t string -s Adwaita-dark 2>/dev/null
xfconf-query -c xsettings -p /Net/IconThemeName -n -t string -s Adwaita 2>/dev/null
xfconf-query -c xsettings -p /Gtk/FontName -n -t string -s "Noto Sans 12" 2>/dev/null
xfconf-query -c xsettings -p /Gtk/MonospaceFontName -n -t string -s "DejaVu Sans Mono 13" 2>/dev/null
xfconf-query -c xfwm4 -p /general/theme -n -t string -s Default 2>/dev/null
xfconf-query -c xfwm4 -p /general/title_font -n -t string -s "Noto Sans Bold 11" 2>/dev/null
mkdir -p ~/.config/gtk-3.0
printf 'textview, textview text { font-family: "DejaVu Sans Mono"; font-size: 19pt; }\n' > ~/.config/gtk-3.0/gtk.css
gsettings set org.xfce.mousepad.preferences.view word-wrap true 2>/dev/null
gsettings set org.xfce.mousepad.preferences.window statusbar-visible false 2>/dev/null
xfconf-query -c thunar -p /last-icon-view-zoom-level -n -t string -s THUNAR_ZOOM_LEVEL_200_PERCENT 2>/dev/null
xfconf-query -c thunar -p /last-show-hidden -n -t bool -s false 2>/dev/null
xfsettingsd >/tmp/xfs.log 2>&1 &
xfwm4 --compositor=off >/tmp/xfwm.log 2>&1 &
sleep 1
xfdesktop >/tmp/xfdesktop.log 2>&1 &
xfce4-panel >/tmp/panel.log 2>&1 &
sleep 2
xsetroot -cursor_name left_ptr
touch /tmp/desktop.ready
exec "$@"
