# Simulation .Bags Grapher
This software is a magical rosbag reader & grapher. When it grows up, it will be functioning as a hard-working microservice to analyze all rosbag outputs of the people who run simulation.
## How to install
Pre-requisites: 
* Ubuntu 18.04 (Or maybe other distros, thanks Docker)
* Docker

You do not need ROS. After you install docker, run these commands:
```bash
git clone https://github.com/FOL4HighwayPilot/sim-rosbag-grapher.git
cd sim-rosbag-grapher
sudo docker build -t watchdog:v1 .
sudo docker run watchdog:v1
```
After this step, docker image is built (hopefully) and running.
You can check if container is running with:

```bash
sudo docker ps
```
## Intermediate Step
```bash
:~/sim-rosbag-grapher$ sudo chmod +x copy_rb.sh && chmod +x copy_svg.sh
``` 
These two scripts are required to copy *.bag* files in container and *.svg* (result) files out of it.

## How to run?
After you install and run the container and complete the intermediate step 
* **0: Ensure you name *.bag* files with manners:**
`UCXXX-TSXXX-DDMMYYYY` 

**UCXXX**: Use case number
**TSXXX**: Variant of that use case 
**DDMMYYYY**: DayMonthYear info of the generated sim result(no "-" or "_" or "/" in date, only "-"s are between UCXXX and TSXXX and TSXXX and DDMMYYYY)
* **1: Put your *.bag* files under a directory, copy directory's path**
* **2: run** `sudo ./copy_rb.sh`

Terminal will look like this:
```bash
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
5cfe139f018f        doggy:doggy         "/bin/sh -c 'mkdir /…"   9 seconds ago       Up 8 seconds                            confident_merkle


Enter where sim rosbags are: <your .bag directory>

Weird name of your docker container: confident_merkle
```
That weird name changes everytime you run an image, it will be fixed. But for now, get used to funny docker generated names.

* **3:**  After that, wait. (or check the docker terminal, there are some printouts which will make you feel something really complex is running in that container) For each *.bag* file under your directory, it processes the messages, etc and there isn't a measurement I've took. I will.
* **4: run** `sudo ./copy_svg.sh`

Similar Story, just write your container's name this time and it will provide you the result graphs under 
`home/$USER/Simulativ_Serviced`

## Having Issues?
You know who to contact.
