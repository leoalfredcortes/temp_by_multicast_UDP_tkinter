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
window.title("..::Receptor Aletas de Temperatura UDP::..") 
window.geometry('425x450')  
area_conversation = scrolledtext.ScrolledText(window,width=50,height=20)
area_conversation.grid(column=1, row=0)
falg_start = 0

def get_alerts():
    falg_start = 1
    while(falg_start==1):
        message, address = sock.recvfrom(255)
        area_conversation.insert(INSERT,message)
        area_conversation.insert(INSERT,'\n')
        
def clean_text():
    area_conversation.delete('1.0', END)    
    
def ini_prog():
    area_conversation.insert(INSERT,"Iniciando sistema de Alertas...")
    tread1 = threading.Thread(target = get_alerts)
    tread1.start()    
    
btn = Button(window, text="Start", bg="blue", fg="white", command=ini_prog)
btn.grid(column=1, row=2)

btn = Button(window, text="Clear", bg="blue", fg="white", command=clean_text)
btn.grid(column=1, row=3)

window.mainloop()
