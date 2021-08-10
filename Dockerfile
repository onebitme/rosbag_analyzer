FROM python:3

COPY requirements.txt /
RUN pip install --extra-index-url https://rospypi.github.io/simple/ rospy rosbag
RUN pip install watchdog
RUN python3 -m pip install -r requirements.txt


#ADD run.sh /run.sh
#RUN chmod +x /run.sh
#ENTRYPOINT ["./run.sh"]
ADD rosbag_analyzer/src/simulativ_watchdog.py /home/$USER/Simulativ_Serviced/rosbag_analyzer/src/
ADD rosbag_analyzer/src/metadata_json_v2.json /home/$USER/Simulativ_Serviced/rosbag_analyzer/src/
#ADD rosbag_analyzer/src/rosbag_copier.py /home/Simulativ_Serviced/rosbag_analyzer/src
#CMD ./run.sh & python -u /home/esozen1/Simulativ_Serviced/rosbag_analyzer/src/simulativ_watchdog.py

CMD python -u /home/$USER/Simulativ_Serviced/rosbag_analyzer/src/simulativ_watchdog.py
