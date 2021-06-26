import sys, os
import time
import json
import logging
from types import DynamicClassAttribute
import rosbag
from watchdog import observers
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler, FileSystemEventHandler
from matplotlib import pyplot as plotter


path_rosbag = "/home/esozen1/Simulativ_Serviced/sim_result_rosbags"
path_json = "/home/esozen1/Simulativ_Serviced/sim_result_jsons"

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

def graph_it(type_of_graph, ros_bag_path):
    bag = rosbag.Bag(ros_bag_path)
    y_axis_of_graph = []
    time_axis_of_graph =[]
    
    if type_of_graph =="lonlat":
        print("Fixed Graph: "+ type_of_graph)
    elif type_of_graph == "spdvar":
        print("Criteria: " + type_of_graph)
    elif type_of_graph == "laneov":
        print("Criteria: " + type_of_graph)
    elif type_of_graph == "foldst":
        print("Criteria: " + type_of_graph)
    elif type_of_graph == "stpdst":
        print("Criteria: " + type_of_graph)
    elif type_of_graph == "avdec":
        print("Criteria: " + type_of_graph)
    elif type_of_graph == "avacc":
        print("Criteria: " + type_of_graph)
    elif type_of_graph == "offego":
        print("Criteria: " + type_of_graph)
    elif type_of_graph == "offstr":
        print("Criteria: " + type_of_graph)        
    elif type_of_graph == "lanech":
        print("Criteria: " + type_of_graph)
    return a_result_graph
    

def on_created_rb(event):
    sim_result_graphlist = []
    path_rosbag = event.src_path
    print(f"hey, {event.src_path} has been created!")
    if str(path_rosbag).__contains__('UC'):
        print("ROSBAG Uploaded for a Use Case")
        print("Checking Metadata File")
        UC = check_uc(path_rosbag)
        TS = (check_ts(path_rosbag))
        if os.path.isfile('./metadata_json_v2.json'):
            print("Metadata file exists, Checking Validation Result")
            meta_file = open('metadata_json_v2.json')
            meta_json = json.load(meta_file)
            for i in meta_json['Use_Cases']:
                if i['UC'] == UC:
                    metrics = i['Metrics']
                    for key in metrics:
                        sim_result_graphlist.append(key)
            print(sim_result_graphlist)

            if os.listdir("/home/esozen1/Simulativ_Serviced/sim_result_jsons") == []:
                print("There are no validation results available in dedicated folder")
            else:
                uc = UC
                var = TS
                validation_file = open("/home/esozen1/Simulativ_Serviced/sim_result_jsons/uc_"+uc+"_var_"+var+"_json.txt")
                validation_json = json.load(validation_file)
                #print(validation_json['CriticalZone'])
                if str(path_rosbag).__contains__('UC'):
                        bag = rosbag.Bag(path_rosbag)
        else:
            print("Metadata File is not available to report sim results")
    else:
        print("Uploaded ROSBAG is not valid in terms of naming")


def on_deleted_rb(event):
    path = event.src_path
    print(f"{event.src_path} is deleted!")

def on_modified_rb(event):
    path = event.src_path
    print("Starting reading something ")
    bag = rosbag.Bag(path)
    print(bag.get_type_and_topic_info()[1])
    for topic,msg,t  in bag.read_messages(topics=['/ego_pose']):
        print(msg.PosnLgt)

def on_moved_rb(event):
    path = event.src_path
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
    bag = rosbag.Bag(path)
    print(bag.get_type_and_topic_info()[1])
    for topic,msg,t  in bag.read_messages(topics=['/ego_pose']):
        print(msg.PosnLgt)

def on_created_json(event):
    path = event.src_path
    print(path)

def on_deleted_json(event):
    path = event.src_path
    print(f"{event.src_path} is deleted!")

def on_modified_json(event):
    path = event.src_path
    print(path)

def on_moved_json(event):
    path = event.src_path
    print(path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    ignore_patterns = ["*.tmp"]
    ignore_directories = True
    case_sensitive = True
    #Every sim ouput to put here: 01.232.4.5. 

    
    pattern_rb = ["*.bag"]
    pattern_json = ["*.txt"]
    
    custom_event_handler_rb = PatternMatchingEventHandler(pattern_rb, ignore_patterns, ignore_directories = True)

    custom_event_handler_rb.on_created = on_created_rb
    custom_event_handler_rb.on_deleted = on_deleted_rb
    custom_event_handler_rb.on_modified = on_modified_rb
    custom_event_handler_rb.on_moved = on_moved_rb

    custom_event_handler_json = PatternMatchingEventHandler(pattern_json, ignore_patterns, ignore_directories = True)

    custom_event_handler_json.on_modified = on_modified_json
    custom_event_handler_json.on_moved = on_moved_json
    custom_event_handler_json.on_deleted = on_deleted_json
    custom_event_handler_json.on_created = on_created_json

    observer1 = Observer()
    observer2 = Observer()
    observer1.schedule(custom_event_handler_rb, path_rosbag, recursive=False)
    observer2.schedule(custom_event_handler_json, path_json, recursive=False)
    observer1.start()
    observer2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer1.stop()
        observer2.stop()