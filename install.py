# Installer for RRR!
try:
        import os
        from subprocess import Popen, PIPE, STDOUT, call
        import sys

        if sys.version_info < (3, 0):
                print("Sorry, please use python 3.x by running 'python3 install.py'")
                exit()

        print("WELCOME TO JAMES K's INSTALLER FOR RRR!")
        print("THIS WILL SET EVERYTHING UP, INCLUDING A CONTROL WEBPAGE ACCESSIBLE ON YOUR LOCAL NETWORK!")
        webhost = input("Would you like apache2 + PHP5 to be setup automatically (THIS WILL OVERWRITE ALL EXISTING WEBHOST DATA) [Y/n]: ").upper()

        proc = Popen("hostname -I", shell=True, stdout=PIPE)
        output = proc.communicate()[0]
        ip = output.decode("utf-8").rstrip('\n')

        print("Updating Pi...")
        os.system("sudo apt-get update")
        print("Pi updated...")

        if webhost == "N":
                installDir = "/var/www/html/RRR/"

                print("Creating RRR sub-directory in www root file...")
                os.system("sudo mkdir /var/www/html/RRR")
                print("File created...")

        else:
                installDir = "/var/www/html/"

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

        print("Moving index.php file to "+installDir+"...")
        os.system("sudo mv index.php "+installDir+"index.php")
        print("index.php file successfully moved...")

        print("Moving control.php file to "+installDir+"...")
        os.system("sudo mv control.php "+installDir+"control.php")
        print("control.php file successfully moved...")

        print("Giving usergroup www-data perms to control usergroup GPIO...")
        os.system("sudo usermod -a -G gpio www-data")
        print("Perms given...")

 	print("Restarting apache2...")
        os.system("sudo service apache2 restart")
        print("Apache2 restarted...")

        print("\n\n\nPLEASE NAVIGATE TO THE FOLLOWING IP, USING ANOTHER COMPUTER ON YOUR NETWORK:\n\n"+str(ip)+"\n\n")
        response = input("You should see a page with fields for controlling the pi remotely [Y|n]: ").upper()
        if response == "N":
                print("ERROR! Please contact: 'mail@jammyworld.com' with error code '2'")
                exit()

        print("Successfull installation!")
        print("Please now connect your relay board to your Pi's GPIO pins if you haven't already!")
        print("DO NOT CONNECT THE RELAYS TO YOUR RIGS YET!")
        print("Now run the following command to continue:\n\npython3 configCreator.py")

except KeyboardInterrupt:
        print("\n\nINSTALL CANCELED!")
        print("EXITING...")
        exit()



