import xml.etree.ElementTree as ET
import os, sys 
import os.path
import glob

def _device_get_device_id(dev_des):
	root = ET.fromstring(dev_des)
	if root == None:
		return None 
	# get devicename from xml string 
	device_id = None
	for e in root:
		if e.tag == 'device':
			for e_device in e: 
				if e_device.tag == 'uniqueId':
					device_id=e_device.text
	return device_id


def _device_get_networkid_from_file(device_file):
	root = ET.parse(device_file).getroot()
	if root == None:
		return None;
	network_id= None
	for e in root:
		if e.tag == 'device':
			for e_device in e: 
				if e_device.tag == 'home':
					for home in e_device: 
						if home.tag == 'networkID':
							network_id = home.text
	return network_id


def _device_get_deviceid_from_file(device_file):
	root = ET.parse(device_file).getroot()
	if root == None:
		return None;
	device_id= None
	for e in root:
		if e.tag == 'device':
			for e_device in e: 
				if e_device.tag == 'uniqueId':
					device_id = e_device.text
	return device_id 



def device_reset(device_id):
	path = "./database/devices/" + device_id + ".xml"
	if os.path.isfile(path):
		os.remove(path)
		return 0
	return -1 


# return 
# -1: error 
#  0: successful 
def device_register(device):
	# save device information as xml 
	device_id = _device_get_device_id(device)
	if device_id == None:
		return -1;
	file = open("./database/devices/" + device_id + ".xml", 'w')
	if file == None:
		return -1
	file.write(device)
	file.close()
	return 0

def device_get_device_from_networkid(networkid):
	device_id = '' 
	devices = glob.glob('./database/devices/*')	
	top = ET.Element('DeviceList')

	for device in devices:
		if _device_get_networkid_from_file(device) != None:
			device_id = _device_get_deviceid_from_file(device)
			child = ET.SubElement(top, "Device")
			child.text = device_id

	return ET.tostring(top)




#def device_get(device_id):
