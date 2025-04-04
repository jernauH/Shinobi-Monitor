#!/bin/python3
import paho.mqtt.client as mqtt
import time
import os
from pathlib import Path
import psutil
import shutil

# MQTT server details
MQTT_BROKER = "192.168.x.x"  # Replace with your MQTT server address
MQTT_PORT = 1883
MQTT_TOPIC_TEMP = "CCTV/temp"
MQTT_TOPIC_UPTIME = "CCTV/uptime"
MQTT_TOPIC_DISKSPACE = "CCTV/diskspace"
MQTT_TOPIC_CCTV_DISKSPACE = "CCTV/storage"
MQTT_TOPIC_CCTV_RAMFREE = "CCTV/memfree"
MQTT_TOPIC_CCTV_CPU = "CCTV/cpuutil"
MQTT_USERNAME = "username"   # Replace with your MQTT username
MQTT_PASSWORD = "password"   # Replace with your MQTT password

# Read temperature from /sys/class/thermal/thermal_zone0/temp
def read_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = round(float(f.read().strip()) / 1000.0, 1)
    return temp

# Read system uptime in hours
def read_uptime():
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.read().split()[0])
    uptime_hours = round(uptime_seconds / 3600.0, 2)
    return uptime_hours

# Read available disk space on / filesystem in GB
def read_diskspace():
    available_space = round(shutil.disk_usage("/")[1]/1000000000,2)
    return available_space

# Read disk space used on /mnt/cctv filesystem in GB
def read_cctv_diskspace():
    used_space = round( sum (os.path.getsize(os.path.join(dirpath,filename)) for dirpath, dirnames, filenames in os.walk( "/mnt/cctv" ) for filename in filenames )/1000000000, 1)
    return used_space

# read cpu utilizatoion
def read_cpu():
    cpu_util = psutil.cpu_percent()
    return cpu_util

#read fee RAM
def read_free_ram():
    free_ram = psutil.virtual_memory()[2]
    return free_ram


# Create MQTT client and set username/password
client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Connect to MQTT server
client.connect(MQTT_BROKER, MQTT_PORT, 60)

temperature = read_temperature()
uptime = read_uptime()
diskspace = read_diskspace()
cctv_diskspace = read_cctv_diskspace()
cpu = read_cpu()
ram = read_free_ram()

client.publish(MQTT_TOPIC_TEMP, temperature)
time.sleep(1)
client.publish(MQTT_TOPIC_UPTIME, uptime)
time.sleep(1)
client.publish(MQTT_TOPIC_DISKSPACE, diskspace)
time.sleep(1)
client.publish(MQTT_TOPIC_CCTV_DISKSPACE, cctv_diskspace)
time.sleep(1)
client.publish(MQTT_TOPIC_CCTV_CPU, cpu)
time.sleep(1)
client.publish(MQTT_TOPIC_CCTV_RAMFREE, ram)
time.sleep(1)

# Disconnect from MQTT server
client.disconnect()
