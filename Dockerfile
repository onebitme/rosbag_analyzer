FROM python:3

ADD rosbag_analyzer/src/simulativ_watchdog.py /
ADD rosbag_analyzer/src/metadata_json_v2.json /
COPY /output_files /output_files
COPY /sim_result_jsons /home/esozen1/Simulativ_Serviced/sim_result_jsons
COPY /sim_result_rosbags /home/esozen1/Simulativ_Serviced/sim_result_rosbags
COPY requirements.txt /
RUN pip install --extra-index-url https://rospypi.github.io/simple/ rospy rosbag
RUN pip install watchdog
RUN python3 -m pip install -r requirements.txt
CMD ["python", "-u"  , "./simulativ_watchdog.py"]