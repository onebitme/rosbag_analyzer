FROM python:3.6.9

RUN pip install --upgrade pip
COPY requirements.txt /

RUN pip install --extra-index-url https://rospypi.github.io/simple/ rospy rosbag
RUN pip install watchdog
RUN python3 -m pip install -r requirements.txt

ADD rosbag_analyzer/src/simulativ_watchdog.py /home/esozen1/Simulativ_Serviced/rosbag_analyzer/src/
ADD rosbag_analyzer/src/metadata_json_v2.json /home/esozen1/Simulativ_Serviced/rosbag_analyzer/src/

CMD mkdir /home/esozen1/Simulativ_Serviced/sim_result_rosbags & python3 -u /home/esozen1/Simulativ_Serviced/rosbag_analyzer/src/simulativ_watchdog.py
