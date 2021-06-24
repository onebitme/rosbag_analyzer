import sys, os
import time
import json
import logging
from types import DynamicClassAttribute
import rosbag
from watchdog import observers
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler, FileSystemEventHandler

path_rosbag = "/home/esozen1/Simulativ_Serviced/sim_result_rosbags"
path_json = "/home/esozen1/Simulativ_Serviced/sim_result_jsons"

def on_created_rb(event):
    path_rosbag = event.src_path
    print(f"hey, {event.src_path} has been created!")
    if str(path_rosbag).__contains__('UC'):
        print("ROSBAG Uploaded for a Use Case")
        print("Checking Metadata File")
        if os.path.isfile('./metadata_json_v2.json'):
            print("Metadata file exists, Checking Validation Result")
            meta_file = open('metadata_json_v2.json')
            meta_json = json.load(meta_file)
            if os.listdir("/home/esozen1/Simulativ_Serviced/sim_result_jsons") == []:
                print("There are no validation results available in dedicated folder")
            else:
                uc = "001"
                var = "001"
                validation_file = open("/home/esozen1/Simulativ_Serviced/sim_result_jsons/uc_"+uc+"_var_"+var+"_json.txt")
                validation_json = json.load(validation_file)
                print(validation_json['CriticalZone'])
                for i in meta_json['Use_Cases']:
                    print(i['UC'])
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