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
