import sys
import time
import logging
import rosbag
from watchdog import observers
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler, FileSystemEventHandler


def on_created_rb(event):
    path = event.src_path
    print("Starting reading ")
    bag = rosbag.Bag(path)
    print(bag.get_type_and_topic_info()[1])
    for topic,msg,t  in bag.read_messages(topics=['/ego_pose']):
        print(msg.PosnLgt)
    print(f"hey, {event.src_path} has been created!")

def on_deleted_rb(event):
    path = event.src_path
    print(f"{event.src_path} is deleted!")

def on_modified_rb(event):
    path = event.src_path
    print("Starting reading ")
    bag = rosbag.Bag(path)
    print(bag.get_type_and_topic_info()[1])
    for topic,msg,t  in bag.read_messages(topics=['/ego_pose']):
        print(msg.PosnLgt)

def on_moved_rb(event):
    path = event.src_path
    print("Starting reading ")
    bag = rosbag.Bag(path)
    print(bag.get_type_and_topic_info()[1])
    for topic,msg,t  in bag.read_messages(topics=['/ego_pose']):
        print(msg.PosnLgt)
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

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

    path_rosbag = "/home/esozen1/Simulativ_Serviced/sim_result_rosbags"
    path_json = "/home/esozen1/Simulativ_Serviced/sim_result_jsons"
    
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