######################################################################################
# Instituto Tecnológico de Colima - División de Estudios de Posgrado e Investigación #
# Maestría en Sistemas Computacionales - Materia: Tecnologías de Internet            #
#                                                                                    #
# Código Fuente para Servidor UDP, con interfas tkinter el cual lee datos            #
# del puerto serial (temperatura) si la temperatura exede de los rangos establesidos #
# el programa emitira una alerta a los clientes conectados a este                    #
#                                                                                    #
# Realizado por:                                                                     #
# Osvaldo Vladimir Rodríguez Leal                                                    #
# José Alfredo Cortés Quiroz                                                         #
# Villa de Álvarez, Col 21/10/19                                                     #
######################################################################################

from tkinter import *
from tkinter import scrolledtext
import serial, time
import threading
import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
arduino = serial.Serial('/dev/ttyUSB0', 9600)
mensage = '!Alerta temperatura elevada!'
multicast_addr = '224.0.0.1'
port = 6000

window = Tk() 
window.title("..::Aletas de Temperatura UDP::..") 
window.geometry('430x430')  
area_conversation = scrolledtext.ScrolledText(window,width=50,height=20)
area_conversation.grid(column=1, row=0)

def read_serial():
    while(True):
        rawString = arduino.readline()
        cadena = rawString.decode("utf-8")        
        print(cadena)
        if (float(cadena) >= 25.00 and float(cadena)<= 30.00):
            area_conversation.insert(INSERT,cadena)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
            sock.sendto((str.encode(mensage)), (multicast_addr, port))

tread1 = threading.Thread(target = read_serial)
tread1.start()

window.mainloop()
