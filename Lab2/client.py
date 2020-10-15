import socket
import threading 
import pickle
import json
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(
    ("127.0.0.1",1234)
)

def send_server():
        while True:
            data = client.recv(2048) #Оримумо "You are connected"
            #2048 - кількість даних які ми хочемо отримати за один пакет
            print(data.decode("utf-8"))#Розкодовуємо рядок 
   
if __name__ == "__main__":
    send_server()
