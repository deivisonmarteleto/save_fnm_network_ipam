Olá!

We will collect the Subnet registered in the PHPIpam application and save it in "/ etc / networks_list" and restart the Fastnetmon application.

# To work properly:
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1) install "requirements.txt":
      pip3 install requirements.txt

2) Upload an image from the local "mongodb" (Fastnetmon uses local Mongo to save attacks).
     - In the app_mongo.py file, set the SRV MONGO ip.

3) adjust the location of the log file.

4) Set the PHP Ipam key and ip in the "app_ipam.py" file
     - in this file there is the variable NEXTHOP_DEFAULT,
this variable complements another Fastnetmon automation project.

5) Adjust the location of the "networks_list" file.

6) The script uses the "sched" library, avoiding the use of the server's cron. 
    python3 app_save_network.py &

7) enjoy!
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Use suggestion for who is ISP or Operator and has ANS behind your ASN. Is to customize PHP Ipam:

- Configure the "Section" option with the customer's ASN.
- ISP or not, use blocks equal to or less than "/ 24". 
