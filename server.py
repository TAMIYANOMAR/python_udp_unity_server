import socket
import json
import random

recieve_sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
send_sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)

recieve_port = 5000
send_port = 5001

server_host = '0.0.0.0'

recieve_addr = (server_host, recieve_port)
send_addr = (server_host, send_port)

print("server started on port: " + str(recieve_port) + " and " + str(send_port))

# Bind to the port
recieve_sock.bind(recieve_addr)
send_sock.bind(send_addr)

client_addr_1 = None
player_1_ready = False
client_addr_2 = None
player_2_ready = False

player_1_position = [0,0]
player_1_hp = 100
player_2_position = [0,0]
player_2_hp = 100

start = False

while True:

    # player_2_position[0] += random.randrange(-1,1)/10
    # player_2_position[1] += random.randrange(-1,1)/10

    json_data = { 
        "player_1_position_x": player_1_position[0],
        "player_1_position_y": player_1_position[1], 
        "player_1_hp": player_1_hp, 
        "player_2_position_x": player_2_position[0],
        "player_2_position_y": player_2_position[1], 
        "player_2_hp": player_2_hp 
    }

    print("recieving data")

    data, addr = recieve_sock.recvfrom(1024)

    if(start == False):

        if(client_addr_1 == None):
            print("client 1 connected")
            client_addr_1 = (addr[0],5002)
            print(client_addr_1)
            send_sock.sendto("1".encode(), addr)
            print("sent 1 to client 1")
            continue
        elif(client_addr_2 == None and addr[0] != client_addr_1[0]):
            print("client 2 connected")
            client_addr_2 = (addr[0],5002)
            send_sock.sendto("2".encode(), addr)
            print("sent 2 to client 2")
            continue
        
        if(addr[0] != client_addr_1[0] and addr[0] != client_addr_2[0]):
            send_sock.sendto("Sever connection is full".encode(), addr)
            continue
        elif(addr[0] == client_addr_1[0]):
            if(data.decode() == "ready"):
                player_1_ready = True
                print("player 1 ready")
        elif(addr[0] == client_addr_2[0]):
            if(data.decode() == "ready"):
                player_2_ready = True
                print("player 2 ready")

        if(player_1_ready == True and player_2_ready == True):
            send_sock.sendto("start".encode(), client_addr_1)
            print("sent start to client 1")
            send_sock.sendto("start".encode(), client_addr_2)
            print("sent start to client 2")
            player_1_ready = False
            player_2_ready = False 
            start = True
            continue 
    
    if(start):
        if(addr[0] == client_addr_1[0]):
            print("sending data to client 1")
            s = json.dumps(json_data,ensure_ascii=False)
            send_sock.sendto(s.encode(), client_addr_1)
            data_json = json.loads(data)
            print(data_json)
            player_1_position[0] = data_json["player_1_position_x"]
            player_1_position[1] = data_json["player_1_position_y"]
            player_1_hp = data_json["player_1_hp"]
        
        elif(addr[0] == client_addr_2[0]):
            print("sending data to client 2")
            s = json.dumps(json_data,ensure_ascii=False)
            send_sock.sendto(s.encode(), client_addr_2)
            data_json = json.loads(data)
            player_2_position = data_json["player_2_position_x"]
            player_2_position = data_json["player_2_position_y"]
            player_2_hp = data_json["player_2_hp"]