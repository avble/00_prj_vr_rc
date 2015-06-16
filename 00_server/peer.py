import xml.etree.ElementTree as ET
import os, sys 
import os.path
import glob
import device 

#def _device_get_device_id(dev_des):
#	root = ET.fromstring(dev_des)
#	if root == None:
#		return None 
#	# get devicename from xml string 
#	device_id = None
#	for e in root:
#		if e.tag == 'device':
#			for e_device in e: 
#				if e_device.tag == 'uniqueId':
#					device_id=e_device.text
#	return device_id
#
#
#def _device_get_networkid_from_file(device_file):
#	root = ET.parse(device_file).getroot()
#	if root == None:
#		return None;
#	network_id= None
#	for e in root:
#		if e.tag == 'device':
#			for e_device in e: 
#				if e_device.tag == 'home':
#					for home in e_device: 
#						if home.tag == 'networkID':
#							network_id = home.text
#	return network_id
#
#
def _peer_get_deviceid_from_file(peer_file):
	root = ET.parse(peer_file).getroot()
	if root == None:
		return None;
	device_id= None
	for e in root:
		if e.tag == 'device':
			for e_device in e: 
				if e_device.tag == 'uniqueId':
					device_id = e_device.text
	return device_id 




# description: 
# return the registered xml 

def peer_get_peer_from_file(peer_file):
        if  _peer_get_deviceid_from_file(peer_file) != None:
                file = open(peer_file, 'r')
                registered_xml = ''
                while 1:
                        line = file.readline()
                        if not line:
                                break
                        registered_xml += line
                file.close()
                return registered_xml
        else:
                return None



def peer_reset(device_id):
	path = "./database/peers/" + device_id + ".peer.xml"
	if os.path.isfile(path):
		os.remove(path)
		return 0
	return -1 


# return 
# -1: error 
#  0: successful 
def peer_register(xml_registerPeer):
	# save device information as xml 
	device_id = device._device_get_device_id(xml_registerPeer)
	if device_id == None:
		return -1;
	file = open("./database/peers/" + device_id + ".peer.xml", 'w')
	if file == None:
		return -1
	file.write(xml_registerPeer)
	file.close()
	return 0


def peer_getDevice(device_id):
        path = "./database/peers/" + device_id + ".peer.xml"
        peer = peer_get_peer_from_file(path)
        if peer != None:
                return peer 
        else:
                return "No device exist", 401


#def peer_get_peers_from_networkid(networkid):
#	device_id = '' 
#	devices = glob.glob('./database/peers/*')	
#	top = ET.Element('DeviceList')
#
#	for device in devices:
#		if _device_get_networkid_from_file(device) != None:
#			device_id = _device_get_deviceid_from_file(device)
#			child = ET.SubElement(top, "Device")
#			child.text = device_id
#
#	return ET.tostring(top)




#def device_get(device_id):
