# Reference from ---> Python library to send command to EPSON VT6 via TCP/IP
# by Judhi Prasetyo April 2023 
# https://github.com/judhi/RC7_Python

import socket
from time import sleep

class EpsonRobotController:
    def __init__(self, ip_address="127.0.0.1", port=2001):
        self.ip_address = ip_address
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip_address, self.port))

    def go(self, x=0, y=450, robot_z=850, robot_u=0):
        coordinates = f"GO {x} {y} {robot_z} {robot_u}\r\n"
        print(f"Going to position {x}, {y}, {robot_z}, {robot_u}")
        self.client_socket.send(coordinates.encode())
        confirmation = self.client_socket.recv(1023) # waiting for confirmation from robot
        print("result:", confirmation)
        sleep(1)

    def jump(self, x=0, y=450, robot_z=850, robot_u=0):
        coordinates = f"JUMP {x} {y} {robot_z} {robot_u}\r\n"
        print(f"Jumping to position {x}, {y}, {robot_z}, {robot_u}")
        self.client_socket.send(coordinates.encode())
        confirmation = self.client_socket.recv(1023) # waiting for confirmation from robot
        print("result:", confirmation)
        sleep(1)
        
    def move(self, x=0, y=450, robot_z=850, robot_u=0):
        coordinates = f"MOVE {x} {y} {robot_z} {robot_u}\r\n"
        print(f"Moving to position {x}, {y}, {robot_z}, {robot_u}")
        self.client_socket.send(coordinates.encode())
        confirmation = self.client_socket.recv(1023) # waiting for confirmation from robot
        print("result:", confirmation)
        sleep(1)
        
    def grip(self, gripper_state):
        endeffector_state = f"{gripper_state} \r\n"
        print(f"Gripper {gripper_state} ")
        self.client_socket.send(endeffector_state.encode())
        confirmation = self.client_socket.recv(1023) # waiting for confirmation from robot
        print("result:", confirmation)
        sleep(1)
        
    def close_connection(self):
        self.client_socket.close()