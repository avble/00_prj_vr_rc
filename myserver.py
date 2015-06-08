import thread
import threading 
import socket
import cmd


host = ''
port = 1234 
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)


peers = []

def peer_get_a_peer(usr_id):
	for peer in peers:
		if peer[1] == user_id:
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
				client.send("OK")
			elif cmd == 'GET':
				peer = peer_get_a_peer(user_id)		
				client.send("OK")
				print peer


class CMDInterpreter(cmd.Cmd):
    def do_list_peer(self, line):
	for peer in peers:
		print peer
    
    
    def do_EOF(self, line):
        return True

if __name__ == "__main__":
	thread.start_new_thread( server_thread , ("Thread-1", ) )	
	CMDInterpreter().cmdloop()


