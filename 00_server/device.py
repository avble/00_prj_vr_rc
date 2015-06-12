import xml.etree.ElementTree as ET

def _device_get_device_id(dev_des):
	#print "Debug  :", device
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


def device_reset(device_id):
	# just delete file 
	return 0


#def device_get(device_id):
