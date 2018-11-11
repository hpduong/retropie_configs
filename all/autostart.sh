while pgrep omxplayer >/dev/null; do sleep 1; done
(sleep 10; mpg123 -Z /home/pi/RetroPie/backgroundmusic/*.mp3 >/dev/null 2>&1) &
emulationstation
