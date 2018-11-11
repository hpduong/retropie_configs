pkill -STOP mpg123
ifexist=`ls /home/pi/RetroPie/videoloadingscreens/$1.mp4 |wc -l`
if [[ $ifexist > 0 ]];then
 omxplayer_silent --blank /home/pi/RetroPie/videoloadingscreens/$1.mp4
else
 omxplayer_silent --blank /home/pi/RetroPie/videoloadingscreens/default.mp4
fi