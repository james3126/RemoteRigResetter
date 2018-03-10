# Config Creator For James K's Remote Rig Resetter
import sys

if sys.version_info < (3, 0):
	print("Sorry, please use python 3.x by running 'python3 install.py'")
	exit()
	
import configparser
import RPi.GPIO as GPIO
import time

try:
	print("THIS SETUP WILL TAKE 1-3 MINUTES!\n")
	print("Please ensure your relay is plugged in to the correct GPIO headers.")
	print("Double check that you dont have relay control pins connected to 5V, 3V or ground pins!")
	print("Double check that you have all control pins connected to a numbered GPIO pin!")
	print("Additionally, ensure that you have NOT connected any rigs to the relays!\n\n")
	print("You will be asked a question as each pin is tested -> 'DID ANYTHING HAPPEN: '")
	print("You can answer: Y | N\n\n")
	print("If you answer Y, you will then be asked 'WHICH RELAY HAS ACTIVATED: '")
	print("You can answer: 1-[NumberOfRelaysYouHave]\n\n\n")
	totalRelays = int(input("How many relays do you have connected: "))

	GPIO.setmode(GPIO.BCM)

	config = configparser.ConfigParser()
	config['PINS'] = {}
	config['TOTAL_RELAYS'] = {}
	config['RELAY_NAMES'] = {}
	config['RELAYS']["total"] = str(totalRelays)
	
	ALLPINS = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,14,15,18,23,25,8,7,12,16,20,21]
	mappedPins = 0
	testNum = 0	

	while mappedPins <= totalRelays-1:
		pin = ALLPINS[testNum]
		testNum += 1
		time.sleep(1)
		print("TESTING PIN: "+str(pin))
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)
		time.sleep(1)
		GPIO.output(pin, GPIO.HIGH)

		anything = input("DID ANYTHING HAPPEN [Y|N]: ").upper()
		if anything == "Y":
			GPIO.output(pin, GPIO.LOW)
			activeRelay = int(input("WHICH RELAY HAS ACTIVATED: "))
			if isinstance(activeRelay, int) == True:
				GPIO.output(pin, GPIO.HIGH)
				config['PINS']["rig"+str(activeRelay)] = str(pin)
				print("Mapped pin ("+str(pin)+") to relay ("+str(activeRelay)+")")
				mappedPins += 1
			else:
				GPIO.output(pin, GPIO.HIGH)

	else:
		print("All relays have been mapped!")
		print("WRITING TO INI FILE...")
		with open('config.ini', 'w') as configfile:
			config.write(configfile)
		print("You may now connect relays to your rigs!")

	GPIO.cleanup()
	exit()
	
except KeyboardInterrupt:
	print("CANCELED... EXITING...")
	GPIO.cleanup()
	exit()
