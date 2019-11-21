######################################################################################
# Instituto Tecnológico de Colima - División de Estudios de Posgrado e Investigación #
# Maestría en Sistemas Computacionales - Materia: Tecnologías de Internet            #
#                                                                                    #
# Código Fuente para Cliente (receptor) UDP, con interfas tkinter el cual obtiene    #
# alertas si la temperatura exede de los rangos establesidos en el servidor (emisor) #
#                                                                                    #
# Realizado por:                                                                     #
# Osvaldo Vladimir Rodríguez Leal                                                    #
# José Alfredo Cortés Quiroz                                                         #
# Villa de Álvarez, Col 21/10/19                                                     #
######################################################################################

from tkinter import *
from tkinter import scrolledtext
import threading
import socket
import struct

multicast_addr = '224.0.0.1'
bind_addr = '0.0.0.0'
port = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((bind_addr, port))

window = Tk() 
window.title("..::Aletas de Temperatura UDP::..") 
window.geometry('430x430')  
area_conversation = scrolledtext.ScrolledText(window,width=50,height=20)
area_conversation.grid(column=1, row=0)

def get_alerts():
    while True:
        message, address = sock.recvfrom(255)
        area_conversation.insert(INSERT,message)
        area_conversation.insert(INSERT,'\n')
        print (message)

tread1 = threading.Thread(target = get_alerts)
tread1.start()
window.mainloop()
