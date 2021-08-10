#!/bin/bash
docker ps

read -p "Enter where sim rosbags are: " a 
echo $a
read -p "Weird name of your docker container: " b
echo $b

docker cp $a/. $b:/home/$USER/Simulativ_Serviced/sim_result_rosbags/
#



#while :
#do
#    echo "Input Me"
#	read a
#    sleep 1
#	if [ "$a" = 0 ]
#	then
#		break
#	fi
#	echo $a
#done