import pprint
import thread
import threading 
import socket
import cmd


host = ''
port = 12345
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)


peers = []

def peer_get_a_peer(usr_id):
	for peer in peers:
		if peer[1] == usr_id:
			return peer
	return None


def peer_add_a_peer(_peer):
	for peer in peers:
		if peer[1] == _peer[1]:
			peer[2] = _peer[2] 
			return None
	
	peers.append(_peer)
	


def server_thread (thread_name):
	while 1:
		client, address = s.accept()
		data = client.recv(size)
		print data	
		if data:
			data_list = data.split('_')
			cmd = data_list[0]
			user_id = data_list[2]
			sdp = None;
			if len(data_list) > 2:
				sdp = data_list[3]
			item = [cmd, user_id, sdp]
			if cmd == 'PUT':	
				peer_add_a_peer(item)
				client.send("ACK: OK")
			elif cmd == 'GET':
				peer = peer_get_a_peer(user_id)		
				dsp_all = "ACK: OK"
				dsp_all += '\n'
				if peer != None:
					dsp_all += peer[2]
					dsp_all += '\n'
				client.send(dsp_all);
				print "[Debug] peer: ", dsp_all 

			elif cmd == 'GETALL':
				dsp_all = "ACK: OK"
				dsp_all +=  '\n'
				for peer in peers:
					dsp_all += "USER=" + peer[1]
					dsp_all +=  '\n'
					dsp_all += peer[2]
					dsp_all +=  '\n'
				client.send(dsp_all)
				print "Debug: \n",  dsp_all


class CMDInterpreter(cmd.Cmd):
    def do_list_peer(self, line):
	for peer in peers:
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(peer[2])
    
    
    def do_EOF(self, line):
        return True

if __name__ == "__main__":
	thread.start_new_thread( server_thread , ("Thread-1", ) )	
	CMDInterpreter().cmdloop()


