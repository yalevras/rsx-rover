#! /bin/bash

sleep 5

while true; do

    rosrun map_server map_saver -f ~/rsx_ws/src/rsx-rover/rover/autonomy/maps/current_map map:=/ransac_grid
    echo done!
    sleep 5

done

