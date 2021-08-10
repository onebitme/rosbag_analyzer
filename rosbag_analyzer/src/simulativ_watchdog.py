from posixpath import dirname
import datetime
import sys, os
import time
import json
import logging
import rosbag
import numpy as np

from types import DynamicClassAttribute
from watchdog import observers
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler, FileSystemEventHandler

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plotter


path_rosbag = "/home/esozen1/Simulativ_Serviced/sim_result_rosbags"

def slicer(anypath, sub):
    index = anypath.find(sub)
    if index != -1:
        return anypath[index:]
    else:
        raise Exception('Sub String not found!')

def check_uc(anypath):
    get_uc=slicer(anypath, "UC")
    what_is_uc = get_uc[2:5]
    return what_is_uc

def check_ts(anypath):
    get_bagname_first = slicer(anypath, "UC")
    get_ts_now = slicer(get_bagname_first, "-")
    what_is_ts = get_ts_now[3:6]
    return what_is_ts

def make_folder(uc, var, date_time):
    parent_dir = "/home/esozen1/Simulativ_Serviced/output_files/"
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
    if limit_of_metric == "":
        limit_of_metric = 0
    x = datetime.datetime.now()
    date_time = '{:%d-%m-%Y}'.format(x)
    save_graph_here = make_folder(uc,var,date_time)
    print("Created Folder: " + save_graph_here)
    bag = rosbag.Bag(ros_bag_path)
    #print(bag.get_type_and_topic_info()[1])

    if type_of_graph =="lonlat":
        y_axis_of_graph = []
        time_axis_of_graph =[]
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            #y_axis_of_graph.append(msg.PosnLgt)
            #time_axis_of_graph.append(msg.PosnLat)
            print(msg)
        #print("Fixed Graph: "+ type_of_graph)
        #plotter.plot(time_axis_of_graph,y_axis_of_graph)
        #plotter.savefig(save_graph_here+"/"+type_of_graph+".svg")
    
    elif type_of_graph == "speed_variance":
        y_axis_of_graph = []
        exceed_values = []
        time_axis_of_graph =[]
        #Reading messages
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            y_axis_of_graph.append(msg.speed_variance)
        
        for i in range(len(y_axis_of_graph)):
            val_check = y_axis_of_graph[i]
            if val_check > limit_of_metric:
                exceed_values.append(y_axis_of_graph[i])
            else:
                exceed_values.append(np.nan)
            
        time_axis_of_graph = list(range(len(y_axis_of_graph)))
        plotter.plot(time_axis_of_graph,y_axis_of_graph, label=type_of_graph)
        plotter.plot(time_axis_of_graph, exceed_values, label="exceeding "+ type_of_graph)
        plotter.legend()
        plotter.savefig(save_graph_here+"/"+type_of_graph+".svg")
        plotter.clf()

    elif type_of_graph == "lane_overshoot":
        y_axis_of_graph = []
        time_axis_of_graph =[]
        exceed_values = []
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            y_axis_of_graph.append(msg.lane_overshoot)
        
        for i in range(len(y_axis_of_graph)):
            val_check = y_axis_of_graph[i]
            if abs(val_check) > limit_of_metric:
                exceed_values.append(y_axis_of_graph[i])
            else:
                exceed_values.append(np.nan)
            
        time_axis_of_graph = list(range(len(y_axis_of_graph)))
        plotter.plot(time_axis_of_graph,y_axis_of_graph, label=type_of_graph)
        plotter.plot(time_axis_of_graph, exceed_values, label="exceeding "+ type_of_graph)
        plotter.legend()
        plotter.savefig(save_graph_here+"/"+type_of_graph+".svg")
        plotter.clf()
    
    elif type_of_graph == "av_deceleration":
        y_axis_of_graph = []
        time_axis_of_graph =[]
        exceed_values = []
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            y_axis_of_graph.append(msg.av_deceleration)
        
        for i in range(len(y_axis_of_graph)):
            val_check = y_axis_of_graph[i]
            if abs(val_check) > limit_of_metric:
                exceed_values.append(y_axis_of_graph[i])
            else:
                exceed_values.append(np.nan)
            
        time_axis_of_graph = list(range(len(y_axis_of_graph)))
        plotter.plot(time_axis_of_graph,y_axis_of_graph, label=type_of_graph)
        plotter.plot(time_axis_of_graph, exceed_values, 'ro', label="exceeding "+ type_of_graph)
        plotter.legend()
        plotter.savefig(save_graph_here+"/"+type_of_graph+".svg")
        plotter.clf()
    
    elif type_of_graph == "following_distance":
        y_axis_of_graph = []
        time_axis_of_graph =[]
        exceed_values = []
        for topic,msg,t  in bag.read_messages(topics=['/validation_metrics']):
            y_axis_of_graph.append(msg.following_distance)
            print("Following distance: " + str(msg.following_distance) + "  vs  " + str(msg.distance_to_vehicle))
            exceed_values.append(msg.distance_to_vehicle)

        for i in range(len(exceed_values)):
            val_check = exceed_values[i]
            if val_check < limit_of_metric:
                exceed_values[i] = y_axis_of_graph[i]
            else:
                exceed_values[i] = np.nan
            
        time_axis_of_graph = list(range(len(y_axis_of_graph)))
        plotter.plot(time_axis_of_graph,y_axis_of_graph, label=type_of_graph)
        plotter.plot(time_axis_of_graph, exceed_values,'ro', label="exceeding "+ type_of_graph)
        plotter.legend()
        plotter.savefig(save_graph_here+"/"+type_of_graph+".svg")
        plotter.clf()
        print("Criteria: " + type_of_graph)
    
    
    elif type_of_graph == "stpdst":
        print("Criteria: " + type_of_graph)
    
    
    elif type_of_graph == "avacc":
        print("Criteria: " + type_of_graph)
    
    
    elif type_of_graph == "offego":
        print("Criteria: " + type_of_graph)
    
    
    elif type_of_graph == "offstr":
        print("Criteria: " + type_of_graph)        
    
    
    elif type_of_graph == "lanech":
        print("Criteria: " + type_of_graph)
    
def on_created_rb(event):
    path = event.src_path
    historicalSize = -1
    while (historicalSize != os.path.getsize(path)):
        historicalSize = os.path.getsize(path)
        print("we are in the loop")
        time.sleep(10)
    
    sim_result_graphlist = []
    path_rosbag = event.src_path
    print(f"hey, {event.src_path} has been created!")
    if str(path_rosbag).__contains__('UC'):
        print("ROSBAG Uploaded for a Use Case")
        print("Checking Metadata File")
        UC = check_uc(path_rosbag)
        TS = check_ts(path_rosbag)
        if os.path.isfile('/home/esozen1/Simulativ_Serviced/rosbag_analyzer/src/metadata_json_v2.json'):
            print("Metadata file exists, Checking Validation Result")
            meta_file = open('/home/esozen1/Simulativ_Serviced/rosbag_analyzer/src/metadata_json_v2.json')
            meta_json = json.load(meta_file)
            for i in meta_json['Use_Cases']:
                if i['UC'] == UC:
                    metrics = i['Metrics']
                    for item in metrics.items():
                        print(str(item))
                        sim_result_graphlist.append(item)
                        #sim_result_metric_values.append(value)
                else:
                    print("UC not Found in Metadata")
            for key, value in sim_result_graphlist:
                graph_it(UC, TS, key, value ,path_rosbag)

        else:
            print("Metadata File is not available to report sim results")
    else:
        print("Uploaded ROSBAG is not valid in terms of naming")
    print("On Modified RB " + path)

def on_deleted_rb(event):
    path = event.src_path
    print(f"{event.src_path} is deleted!")

def on_modified_rb(event):
    path = event.src_path
    historicalSize = -1
    while (historicalSize != os.path.getsize(path)):
        historicalSize = os.path.getsize(path)
        print("we are in the loop")
        time.sleep(10)
    
    sim_result_graphlist = []
    path_rosbag = event.src_path
    print(f"hey, {event.src_path} has been created!")
    if str(path_rosbag).__contains__('UC'):
        print("ROSBAG Uploaded for a Use Case")
        print("Checking Metadata File")
        UC = check_uc(path_rosbag)
        TS = check_ts(path_rosbag)
        if os.path.isfile('/home/esozen1/Simulativ_Serviced/rosbag_analyzer/src/metadata_json_v2.json'):
            print("Metadata file exists, Checking Validation Result")
            meta_file = open('/home/esozen1/Simulativ_Serviced/rosbag_analyzer/src/metadata_json_v2.json')
            meta_json = json.load(meta_file)
            for i in meta_json['Use_Cases']:
                if i['UC'] == UC:
                    metrics = i['Metrics']
                    for item in metrics.items():
                        print(str(item))
                        sim_result_graphlist.append(item)
                        #sim_result_metric_values.append(value)
                else:
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
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
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
    #pattern_json = ["*.txt"]
    
    custom_event_handler_rb = PatternMatchingEventHandler(pattern_rb, ignore_patterns, ignore_directories = True)

    custom_event_handler_rb.on_created = on_created_rb
    custom_event_handler_rb.on_deleted = on_deleted_rb
    custom_event_handler_rb.on_modified = on_modified_rb
    custom_event_handler_rb.on_moved = on_moved_rb

    #custom_event_handler_json = PatternMatchingEventHandler(pattern_json, ignore_patterns, ignore_directories = True)

    #custom_event_handler_json.on_modified = on_modified_json
    #custom_event_handler_json.on_moved = on_moved_json
    #custom_event_handler_json.on_deleted = on_deleted_json
    #custom_event_handler_json.on_created = on_created_json

    observer1 = Observer()
    observer2 = Observer()
    observer1.schedule(custom_event_handler_rb, path_rosbag, recursive=False)
    #observer2.schedule(custom_event_handler_json, path_json, recursive=False)
    observer1.start()
    observer2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer1.stop()
        #observer2.stop()