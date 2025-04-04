# Shinobi-Monitor
Simple Python script to run on a Shinobi server to publish system stats to an MQTT server

I created this to enable me to have a simple view of the Shinobi server metrics on my Home Assistant instance dashboard

Copy the script to your Shinobi server 
Ensure you have Paho-Python-mqtt installed (On a debian based system :- sudo apt install python3-paho-mqtt)
Edit the mqtt server details in monitor.sh to reflect your mqtt server ip/hostname and access credentials

Create a crontab to periodically execute the script (may need to run as root)
crontab -e

*/5 * * * * /root/monitor.sh > /dev/null 2>&1



The script assumes there is a mounted filesystem /mnt/cctv being used for video storage

Example Home Assistant Sensor definition 

/homeassistant/configuration.yaml

homeassistant:
..
..
mqtt: 
  sensor: !include mqtt/sensor.yaml
..
..

/homeassistant/mqtt/sensor.yaml

- name: "cctv_temp"
  unique_id: cctvtemp1
  state_topic: CCTV/temp
  unit_of_measurement: '°C'
- name: "cctv_uptime"
  unique_id: cctvup1
  state_topic: CCTV/uptime
  unit_of_measurement: 'h'
- name: "cctv_disk"
  unique_id: cctvdisk1
  state_topic: CCTV/diskspace
  unit_of_measurement: 'GB'
- name: "cctv_storage_used"
  unique_id: cctvdisk2
  state_topic: CCTV/storage
  unit_of_measurement: 'GB'
- name: "cctv_cpu"
  unique_id: cctvcpu1
  state_topic: CCTV/cpuutil
  unit_of_measurement: '%'
- name: "cctv_memfree"
  unique_id: cctvcram1
  state_topic: CCTV/memfree
  unit_of_measurement: '%'

Home Assistant Card Configuration

type: entities
entities:
  - entity: sensor.cctv_uptime
    name: Uptime
    icon: mdi:calendar-check
  - entity: sensor.cctv_cpu
    icon: mdi:cpu-64-bit
    name: CPU Utilization
  - entity: sensor.cctv_memfree
    icon: mdi:memory
    name: Free RAM
  - entity: sensor.cctv_temp
    icon: mdi:coolant-temperature
    name: CPU Temp
  - entity: sensor.cctv_disk
    name: / Used
    icon: mdi:harddisk
  - entity: sensor.cctv_storage_used
    name: Storage Used
    icon: mdi:nas
title: CCTV
