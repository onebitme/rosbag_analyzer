import sys
import time
import logging
import rosbag
from watchdog import observers
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, PatternMatchingEventHandler, FileSystemEventHandler


def on_created(event):
    path = str(event.src_path)
    bag = rosbag.Bag(path)
    print(bag.get_type_and_topic_info()[1])
    for topic,msg,t  in bag.read_messages(topics=['/ego_pose']):
        print(msg.PosnLgt)
    print("Osman_event_happens_only_once????")
    #if ".bag" in str(event.src_path):
    #    print("osmanlandınız")
    #print(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    path = event.src_path
    print(path)
    #print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    path = event.src_path
    print("shit happens during copy paste")
    bag = rosbag.Bag(path)
    print(bag.get_type_and_topic_info()[1])
    for topic,msg,t  in bag.read_messages(topics=['/ego_pose']):
        print(msg.PosnLgt)
    #print(f"hey buddy, {event.src_path} has been modified")

def on_moved(event):
    path = event.src_path
    print("Osman")
    #print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    #path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = "/home/esozen1/Simulativ_Serviced/sim_result_rosbags"
    #event_handler = LoggingEventHandler()

    patterns = ["*.bag"]
    ignore_patterns = ["*.tmp"]
    ignore_directories = True
    case_sensitive = True
    
    #file_system_eHandler = FileSystemEventHandler()

    #file_system_eHandler.on_created = on_created
    #file_system_eHandler.on_modified = on_modified
    
    
    custom_event_handler = PatternMatchingEventHandler(patterns,ignore_patterns=ignore_patterns, ignore_directories = True)
    
    custom_event_handler.on_created = on_created
    custom_event_handler.on_deleted = on_deleted
    custom_event_handler.on_modified = on_modified
    custom_event_handler.on_moved = on_moved

    observer = Observer()
    observer.schedule(custom_event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()