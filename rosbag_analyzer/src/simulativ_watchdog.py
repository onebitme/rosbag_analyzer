from posixpath import dirname
import getpass
import datetime
import sys, os
import time
import json
import logging
import rosbag
import numpy as np
from watchdog import observers
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler, FileSystemEventHandler

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plotter, use

username= getpass.getuser()
username = "esozen1"
path_rosbag = "/home/"+username+"/Simulativ_Serviced/sim_result_rosbags"

#TODO: temporary declaration for LO calculation
lane_width = 3.5
lane_overshoot = lane_width/10

#temporary declaration for Lane Change Distance Calculation
#lane_change_distance_msg needs to be smaller than following distance msg

def slicer(anypath, sub):
    index = anypath.find(sub)
    if index != -1:
        return anypath[index:]
    else:
        raise Exception('Sub String not found!')

def check_uc(anypath):
    get_uc=slicer(anypath, "UC")
    #Old: 2-5 new: 3-6
    what_is_uc = get_uc[3:6]
    print("the UC name is: "+what_is_uc)
    return what_is_uc

def check_ts(anypath):
    get_bagname_first = slicer(anypath, "UC")
    get_ts_now = slicer(get_bagname_first, "-")
    #Old: 3-6 new: 4-6
    what_is_ts = get_ts_now[7:10]
    print("the TS name is: "+what_is_ts)
    return what_is_ts

def make_folder(uc, var, date_time):
    parent_dir = "/home/"+username+"/Simulativ_Serviced/output_files/"
    dirName = uc + var + date_time
    graph_dir = parent_dir + dirName
    try:
        os.makedirs(graph_dir)    
        print("Directory " , dirName ,  " Created ")
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")
    return graph_dir

def graph_it(uc, var, type_of_graph, limit_of_metric, ros_bag_path):
    #TODO: No Time Messages in '/validation_metrics' tab
    #TODO: implement value check
    print(limit_of_metric)
    x = datetime.datetime.now()
    date_time = '{:%d-%m-%Y}'.format(x)
    save_graph_here = make_folder(uc,var,date_time)
    print("Created Folder: " + save_graph_here)
    bag = rosbag.Bag(ros_bag_path)

    if type_of_graph =="lonlat":
        y_axis_of_graph = []
        time_axis_of_graph =[]
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            print(msg)
    
    elif type_of_graph == "speed_variance":
        y_axis_of_graph = []
        exceed_values = []
        time_axis_of_graph =[]
        #Reading messages
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            y_axis_of_graph.append(msg.speed_variance)
        
        for i in range(len(y_axis_of_graph)):
            val_check = y_axis_of_graph[i]
            if val_check >= limit_of_metric:
                exceed_values.append(y_axis_of_graph[i])
            else:
                exceed_values.append(np.nan)
            
        time_axis_of_graph = list(range(len(y_axis_of_graph)))
        plotter.plot(time_axis_of_graph,y_axis_of_graph, label=type_of_graph)
        plotter.plot(time_axis_of_graph, exceed_values, label="exceeding "+ type_of_graph)
        plotter.legend()
        plotter.savefig(save_graph_here+"/"+type_of_graph+".svg")
        plotter.clf()
    #TODO: Lane Change vs Lane Overshoot
    elif type_of_graph == "lane_overshoot":
        y_axis_of_graph = []
        time_axis_of_graph =[]
        exceed_values = []
        second = 0
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            y_axis_of_graph.append(msg.lane_overshoot)
            time_axis_of_graph.append(second)
            second = second + 0.05
        
        for i in range(len(y_axis_of_graph)):
            val_check = y_axis_of_graph[i]
            if abs(val_check) > limit_of_metric:
                exceed_values.append(y_axis_of_graph[i])
            else:
                exceed_values.append(np.nan)
            
        #time_axis_of_graph = list(range(len(y_axis_of_graph)))
        plotter.plot(time_axis_of_graph,y_axis_of_graph, label=type_of_graph)
        plotter.plot(time_axis_of_graph, exceed_values, label="exceeding "+ type_of_graph)
        plotter.legend()
        plotter.savefig(save_graph_here+"/"+type_of_graph+".svg")
        plotter.clf()
    
    elif type_of_graph == "av_deceleration":
        y_axis_of_graph = []
        time_axis_of_graph =[]
        exceed_values = []
        second = 0
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            y_axis_of_graph.append(msg.av_deceleration)
            time_axis_of_graph.append(second)
            second = second + 0.05
        
        for i in range(len(y_axis_of_graph)):
            val_check = y_axis_of_graph[i]
            if val_check < -1 * limit_of_metric: #now in unit of acceleration
                exceed_values.append(y_axis_of_graph[i])
            else:
                exceed_values.append(np.nan)
            
        #time_axis_of_graph = list(range(len(y_axis_of_graph)))
        plotter.plot(time_axis_of_graph,y_axis_of_graph, label="AV Acceleration")
        plotter.plot(time_axis_of_graph, exceed_values, 'ro', label="Exceeding AV Acceleration")
        plotter.legend()
        plotter.savefig(save_graph_here+"/"+type_of_graph+".svg")
        plotter.clf()
    
    elif type_of_graph == "following_distance":
        following_distance_desired = []
        following_distance_actual = []
        exceed_values = []
        time_axis_of_graph =[]
        second = 0
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            following_distance_desired.append(msg.following_distance)
            following_distance_actual.append(msg.distance_to_vehicle)
            exceed_values.append(np.nan)
            time_axis_of_graph.append(second)
            second = second + 0.05
            print("Following distance: " + str(msg.following_distance) + "  vs  " + str(msg.distance_to_vehicle))
        
        for i in range(len(following_distance_actual)):
            if following_distance_actual[i]<following_distance_desired[i]:
                exceed_values[i] = following_distance_actual[i]

            
        #time_axis_of_graph = list(range(len(y_axis_of_graph)))
        plotter.plot(time_axis_of_graph,following_distance_actual, label=type_of_graph)
        plotter.plot(time_axis_of_graph, exceed_values,'ro', label="Violating "+ type_of_graph)
        plotter.legend()
        plotter.savefig(save_graph_here+"/"+type_of_graph+".svg")
        plotter.clf()
        print("Criteria: " + type_of_graph)
    
    
    elif type_of_graph == "stopping_distance":
        y_axis_of_graph = []
        time_axis_of_graph =[]
        exceed_values = []
        second = 0
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            y_axis_of_graph.append(msg.stopping_distance)
            time_axis_of_graph.append(second)
            second = second + 0.05
        
        for i in range(len(y_axis_of_graph)):
            val_check = y_axis_of_graph[i]
            if abs(val_check) > limit_of_metric:
                exceed_values.append(y_axis_of_graph[i])
            else:
                exceed_values.append(np.nan)

        print("Criteria: " + type_of_graph)
    
    #TODO: Currently no implementation of offset_of_ego
    #elif type_of_graph == "offset_of_ego":
    #    print("Criteria: " + type_of_graph)
    
    #TODO: Offset Start is not implemented
    #elif type_of_graph == "offstr":
    #    print("Criteria: " + type_of_graph)        
    
    
    elif type_of_graph == "lane_change_distance":
        following_distance = []
        time_axis_of_graph =[]
        lane_change_distance = []
        violation_array = []
        second = 0

        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            following_distance.append(msg.following_distance)
            print("Lane Change Distance: " + str(msg.lane_change_distance) + "  vs  " + str(msg.following_distance))
            lane_change_distance.append(msg.lane_change_distance)
            violation_array.append(np.nan)
            time_axis_of_graph.append(second)
            second = second + 0.05

        for i in range(len(lane_change_distance)):
            if lane_change_distance[i] > following_distance[i]:
                violation_array[i] = np.nan
            elif lane_change_distance[i] < following_distance[i]:
                violation_array[i] = lane_change_distance[i]
            elif lane_change_distance[i] == 0:
                violation_array[i]=np.nan

        plotter.plot(time_axis_of_graph,lane_change_distance, label=type_of_graph)
        plotter.plot(time_axis_of_graph, violation_array,'ro', label="exceeding "+ type_of_graph)
        plotter.legend()
        plotter.savefig(save_graph_here+"/"+type_of_graph+".svg")
        plotter.clf()
        print("Criteria: " + type_of_graph)
        print("Criteria: " + type_of_graph)
    
def on_created_rb(event):
    path = event.src_path
    historicalSize = -1
    while (historicalSize != os.path.getsize(path)):
        historicalSize = os.path.getsize(path)
        print("Processing...")
        time.sleep(3)
    
    sim_result_graphlist = []
    path_rosbag = event.src_path
    if str(path_rosbag).__contains__('UC'):
        print("ROSBAG Uploaded for a Use Case")
        print("Checking Metadata File")
        UC = check_uc(path_rosbag)
        TS = check_ts(path_rosbag)
        if os.path.isfile("/home/"+username+"/Simulativ_Serviced/rosbag_analyzer/src/uc_ts_metadata.json"):
            print("Metadata file exists, Checking Validation Result")
            meta_file = open("/home/"+username+"/Simulativ_Serviced/rosbag_analyzer/src/uc_ts_metadata.json")
            meta_json = json.load(meta_file)
            for i in meta_json['Use_Cases']:
                if i['UC'] == UC:
                    print(UC + " I can find this in metadata")
                    metrics = i['Metrics']
                    for item in metrics.items():
                        print(str(item))
                        sim_result_graphlist.append(item)
                    break
                else:
                    print(UC + " Not yet the desired UC or cant find the UC")
                    #print("UC not Found in Metadata")
            for key, value in sim_result_graphlist:
                graph_it(UC, TS, key, value ,path_rosbag)

        else:
            print("Metadata File is not available to report sim results")
    else:
        print("Uploaded ROSBAG is not valid in terms of naming")
    print("On Modified RB " + path)

def on_deleted_rb(event):
    path = event.src_path

def on_modified_rb(event):
    path = event.src_path
    historicalSize = -1
    while (historicalSize != os.path.getsize(path)):
        historicalSize = os.path.getsize(path)
        print("Processing...")
        time.sleep(3)
    
    sim_result_graphlist = []
    path_rosbag = event.src_path

    if str(path_rosbag).__contains__('UC'):
        print("ROSBAG Uploaded for a Use Case")
        print("Checking Metadata File")
        UC = check_uc(path_rosbag)
        TS = check_ts(path_rosbag)
        if os.path.isfile("/home/"+username+"/Simulativ_Serviced/rosbag_analyzer/src/uc_ts_metadata.json"):
            print("Metadata file exists, Checking Validation Result")
            meta_file = open("/home/"+username+"/Simulativ_Serviced/rosbag_analyzer/src/uc_ts_metadata.json")
            meta_json = json.load(meta_file)
            for i in meta_json['Use_Cases']:
                if i['UC'] == UC:
                    metrics = i['Metrics']
                    for item in metrics.items():
                        print(str(item))
                        sim_result_graphlist.append(item)

                else:
                    print(UC)
                    print("UC not Found in Metadata")
            for key, value in sim_result_graphlist:
                graph_it(UC, TS, key, value ,path_rosbag)

        else:
            print("Metadata File is not available to report sim results")
    else:
        print("Uploaded ROSBAG is not valid in terms of naming")
    print("On Modified RB " + path)

def on_moved_rb(event):
    path = event.src_path
    bag = rosbag.Bag(path)
    print("On Moved_RB"+path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    ignore_patterns = ["*.tmp"]
    ignore_directories = True
    case_sensitive = True
    #Every sim ouput to put here: 01.232.4.5. 
    
    pattern_rb = ["*.bag"]
    
    custom_event_handler_rb = PatternMatchingEventHandler(pattern_rb, ignore_patterns, ignore_directories = True)

    custom_event_handler_rb.on_created = on_created_rb
    custom_event_handler_rb.on_deleted = on_deleted_rb
    custom_event_handler_rb.on_modified = on_modified_rb
    custom_event_handler_rb.on_moved = on_moved_rb

    observer1 = Observer()
    observer1.schedule(custom_event_handler_rb, path_rosbag, recursive=False)
    observer1.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer1.stop()
