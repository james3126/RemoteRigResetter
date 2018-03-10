# James K's Relay-Based Python3 Remote Rig Resetter V1.0 - 4th March 2018 
# Import modules

import sys

if sys.version_info < (3, 0):
	print("Sorry, please use python 3.x by running 'python3 install.py'")
	exit()

import RPi.GPIO as GPIO
import time
import argparse
import configparser

# Setup arg parsing
parser = argparse.ArgumentParser(description='Restart rigs remotely!')
parser.add_argument('-c', type=str, dest="com", help="Function to execute [on/off/reboot]", required=True)
parser.add_argument('-r', type=int, dest="rig", help="Rig number to run function on", required=True)
args = parser.parse_args()

# Set vars from args
try:
	command = args.com.upper()
except AttributeError:
	print("Usage: python3 RRR.py -c [ON|BOOT|START / OFF|KILL|END / CYCLE|REBOOT|RESTART] -r [RIG-NUMBER]")
	exit()

try:
	rigNum = args.rig
except AttributeError:
	print("Uage: python3 RRR.py -c [ON|BOOT|START / OFF|KILL|END / CYCLE|REBOOT|RESTART] -r [RIG-NUMBER]")
	exit()

# Set GPIO pin mode to BCM (Pin numbers, not GPIO types)
GPIO.setmode(GPIO.BCM)

# Check for a config file. Continue if found!
try: 
	open('config.ini')
except FileNotFoundError:
	print("No config file found!\nPlease set up your config file by running 'python3 configCreator.py'")
	exit()

# Read config file and set pins
pinList = []
config = configparser.ConfigParser()
config.read('config.ini')
for key in config['PINS']:
	pinList.append(int(config['PINS'][key]))

# ----------------- DEFS ------------------
# Setup bootRig def to control pins
def controlRig(rigNumPin,com):
	rigPin = rigNumPin
	control = com

	# Setup a simulated button press duration depending on selected command
	if control == 1:
		sleepTime = 1
	elif control == 0:
		sleepTime = 6
	else:
		print("Something happened. Please contact James with the error code: '1' at the following address:\nEmail: mail@jammyworld.com")

	# Attempt to perform the control of the relays to control the rig
	try:
		print("Performing operation. This will take "+str(sleepTime)+" second(s)...\nPlease wait...")
		GPIO.setup(rigPin, GPIO.OUT)
		GPIO.output(rigPin, GPIO.LOW)
		time.sleep(sleepTime)
		GPIO.output(rigPin, GPIO.HIGH)

	# If the user cancels mid way through, then prevent a crash. Output a clean error and exit
	except KeyboardInterrupt:
		print("OPPERATION HALTED... EXITING...")
		GPIO.cleanup()
		exit()

	# Cleanup pins once complete to prevent error on next run
	GPIO.cleanup()


# Check for valid rig number arg, else exit with error
try:
	if rigNum > 0:
		rigNumPin = pinList[rigNum-1]
	else:
		print("The rig that you have chosed ("+str(rigNum)+") is outside of the selectable rigs.\nYou can choose from rigs 1 to "+str(len(pinList)))
		exit()
except IndexError:
	print("The rig that you have chosen ("+str(rigNum)+") is outside of the selectable rigs.\nYou can choose from rigs 1 to "+str(len(pinList)))
	exit()	

# Check for a valid command
if command == "BOOT" or command == "ON" or command == "START":
	controlRig(rigNumPin,1)
	print("Rig successfully booted!")
elif command == "KILL" or command == "OFF" or command == "STOP":
	controlRig(rigNumPin,0)
	print("Rig successfully killed!")
elif command == "CYLCE" or command == "RESTART" or command == "REBOOT":
	controlRig(rigNumPin,0)
	print("\n\nRig turned off... Waiting 5 seconds")
	time.sleep(5)
	print("\nTurning rig on...")
	GPIO.setmode(GPIO.BCM)
	controlRig(rigNumPin,1)
	print("Rig successfully rebooted!")
else:
	print("The command that you have chosen ("+str(command)+") does not exist.\n\nTo boot a rig: BOOT | ON | START\n\nTo kill a rig: KILL | OFF | STOP\n\nTo restart a rig: CYCLE | RESTART | REBOOT")
	exit()

