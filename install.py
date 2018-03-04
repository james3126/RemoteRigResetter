# Installer for RRR!
import os
from subprocess import Popen, PIPE, STDOUT, call
import sys

if sys.version_info < (3, 0):
	print("Sorry, please use python 3.x by running 'python3 install.py'\n")
	exit()
	
print("WELCOME TO JAMES K's INSTALLER FOR RRR!")
print("THIS WILL SET EVERYTHING UP, INCLUDING A CONTROL WEBPAGE ACCESSIBLE ON YOUR LOCAL NETWORK!")
proc = Popen("hostname -I", shell=True, stdout=PIPE)
output = proc.communicate()[0]
ip = output.decode("utf-8").rstrip('\n')

print("Updating Pi...")
os.system("sudo apt-get update")
print("Pi updated...")

print("Installing apache2...")
os.system("sudo apt-get install apache2 -y")
print("\n\nApache2 installed...")

print("Taking ownership of index.html file...")
os.system("sudo chown $USER /var/www/html/index.html")
print("Ownership taken...")

print("Installing PHP5...")
os.system("sudo apt-get install php5 libapache2-mod-php5 -y")
print("\n\nPHP5 installed...")

print("Removing index.html...")
os.system("sudo rm /var/www/html/index.html")
print("index.html removed....")

print("Creating index.php file...")
os.system("sudo touch /var/www/html/index.php")
print("index.php created...")

print("Taking ownership of index.php...")
os.system("sudo chown $USER /var/www/html/index.php")
print("Ownership taken...")

print("Opening index.php file...")
file = open('/var/www/html/index.php','w')
print("index.php file opened...")

print("Writing to index.php file...")
file.write("<?php\necho 'Hello world!<br>';\necho date('Y-m-d H:i:s');\nphpinfo();\n?>")
print("Written to index.php file...UNSAVED")

print("Saving index.php file...")
file.close()
print("File created...")

print("Restarting apache2...")
os.system("sudo service apache2 restart")
print("Apache2 restarted...")

print("\n\n\nPLEASE NAVIGATE TO THE FOLLOWING IP, USING ANOTHER COMPUTER ON YOUR NETWORK:\n\n"+str(ip)+"\n\n")
response = input("Did the page show up with:\n--Hello world\n--Date and time\n--Lots of PHP information\n\n[Y|n] : ")
if response == "N":
	print("ERROR! Please contact: 'mail@jammyworld.com' with error code '2'")
	exit()

print("Successfull installation!")
print("Please now connect your relay board to your Pi's GPIO pins if you haven't already!")
print("DO NOT CONNECT THE RELAYS TO YOUR RIGS YET!")
print("Now run the following command to continue:\n\npython3 configCreator.py")
