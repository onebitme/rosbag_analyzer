#!/bin/bash
docker ps

read -p "Weird name of your docker container: " a
echo $a

docker cp $a:/home/esozen1/Simulativ_Serviced/output_files/ /home/esozen1/Simulativ_Serviced/
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