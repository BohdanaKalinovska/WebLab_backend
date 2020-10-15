import socket
import threading
from datetime import datetime
import time
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Даємо серверу адрес за яким до нас будуть приєднуватися
server.bind(
    ("127.0.0.1", 1234) #lockalhost (адрес, порт)
        )

#Дає серверу поняти що він може приняти вхідні підключення, 
server.listen(15) #15 - це кількість підключень які будуть чекати 
print("Server is listening")
users = [] #Зберігає user_socket

#Надсилає дані користувачам 
def vuvid(user_data):
    for i in range (0,len(users)):
        ur_sk = users[i]
        x = json.dumps(user_data) 
        ur_sk.send(x.encode("utf-8"))
        i +=1

#Таймер
def count_down(user_data):
    global my_timer
    my_timer = 15 #За завданням
    for x in range(my_timer):
        my_timer -= 1
        print(x)
        time.sleep(1)
    print("timer_back:",datetime.now())  
    vuvid(user_data)
    socket.close()

def start_server():
    user_data = [] #Зберігає clients
    while True:
        if not user_data:
            user_socket, address = server.accept() # приймає підключення
            print(f"ID address: User_{address}")
            time_first_connect = datetime.strftime(datetime.now(), '%H:%M:%S')
            time_n = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
            
            clients = { 
                "Start_timer": time_first_connect,
                "id:": address[0],
                "start:":time_n
            }
            user_data.append(clients)   
            #між сокетами передаються байти encode - кодує в байти
            user_socket.send("You are connected".encode("utf-8")) 
            #Щоб відправляти всім клієнтам дані
            users.append(user_socket)
            countdown_thread = threading.Thread(target = count_down, args = (user_data,))
            countdown_thread.start() 
        
        
        while my_timer > 0:
            user_socket, address = server.accept()
            print(f"ID address: User_{address}")
            time_now = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
            print(f"{time_now}")
            clients = { 
                "id:": address[0],
                "start:":time_now
                }
        
            #Для того щоб я могла відправляти повідомлення усім клієнтам які підключені до мого сервера
            user_data.append(clients)
            user_socket.send("You are connected".encode("utf-8"))
            users.append(user_socket)
    
if __name__=="__main__":
    start_server()
