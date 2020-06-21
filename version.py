#!/usr/bin/python

from netmiko import ConnectHandler
import re
import getpass
import time
import csv

devices = []

def version():
##initialising device
	device = {
    		'device_type': 'cisco_ios',
    		'ip': '192.168.1.121',
    		'username': 'xyz',
    		'password': 'abc',
    		'secret':'efg'
    		}



##opening IP file
	ips=open("ip_list.txt")
	print ("Script to Find information of devices in list, Please enter your credential")
	device['username']=input("Username ")
	device['password']=getpass.getpass()
	print("Enter enable password: ")
	device['secret']=getpass.getpass()

	
##Find Information of each devices
	for line in ips:
		device['ip']=line.strip()
		print("\n\nConnecting Device ",line)
		try:
			net_connect = ConnectHandler(**device)	
		except: 
			print("Something is wrong while connecting device "+device['ip'])
			continue
		net_connect.enable()
		time.sleep(1)
		print ("Reading the Version information ")
		output = net_connect.send_command('show version')
		time.sleep(3)

#finding hostname in output using regular expressions
		regex_hostname = re.compile(r'(\S+)\suptime')
		hostname = regex_hostname.findall(output)
		print(hostname[0])  

#finding uptime in output using regular expressions
		regex_uptime = re.compile(r'\S+\suptime\sis\s(.+)')
		uptime = regex_uptime.findall(output)
		print(uptime[0])  

#finding version in output using regular expressions
		regex_version = re.compile(r'Cisco\sIOS\sSoftware.+Version\s([^,]+)')
		version = regex_version.findall(output)
		print(version[0])

#finding serial in output using regular expressions
		regex_serial = re.compile(r'Processor\sboard\sID\s(\S+)')
		serial = regex_serial.findall(output)
		print(serial[0])

#finding ios image in output using regular expressions
#		regex_ios = re.compile(r'System\simage\s\file\sis\s"([^.*"])')
#		ios = regex_ios.findall(output)
#		print(ios)

#finding model in output using regular expressions
		regex_model = re.compile(r'[Cc]isco\s(\S+).*memory.')
		model = regex_model.findall(output)
		print(model[0])
  
		print(device['ip'])    # print current ip address of router on screen
  
#append results to table [hostname,uptime,version,serial,ios,model]
		devices.append([device['ip'],hostname[0],uptime[0],version[0],serial[0],model[0]])
  
#print all results (for all routers) on screen    
	for i in devices:
		print(i)

if __name__ == "__main__":
	version()


