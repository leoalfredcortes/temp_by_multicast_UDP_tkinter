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

from tkinter import *   #libreria grafica Tkinter 
import tk_tools         #libreria grafica para el acelerometro
import serial, time     #libreria para el puerto serial
import threading        #libreria para manejar ilos
import socket           #libreria para manejar la comunicacion por sockets
import struct           #libreria para menajrar estructuras

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
arduino = serial.Serial('/dev/ttyUSB0', 9600)
mensage = '!Alerta temperatura elevada!'
multicast_addr = '224.0.0.1'
port = 6000
temp1 = ""
temp2 = ""

window = Tk() 
window.title("::Monitor UDP::") 
window.geometry('230x260') 

tk_title = Label(window,text="Temperature Monitor")
tk_title.grid(column=1,row=0)

gauge = tk_tools.Gauge(window, max_value=50.0,label='Temperature', unit='°C')
gauge.grid(column=1, row=1)

tk_tex_intruction = Label(window,text="Rango para Alertas")
tk_tex_intruction.grid(column=1,row=3)

tk_label= Label(window,text="De:")
tk_label.grid(column=1,row=4)

txt_in = Entry(window,width=15)
txt_in.grid(column=1, row=5)

tk_label2= Label(window,text="A:")
tk_label2.grid(column=1,row=6)

txt_in2 = Entry(window,width=15)
txt_in2.grid(column=1, row=7)

def read_serial():
    while(True):
        rawString = arduino.readline()
        gauge.set_value(float(rawString))
        cadena = rawString.decode("utf-8")  
        temp1 = float(txt_in.get())
        temp2 = float(txt_in2.get())      
        print(cadena)
        if (float(cadena) >= temp1 and float(cadena)<= temp2):
            sock.sendto((str.encode(cadena + "°C" +mensage )), (multicast_addr, port))

def iniciar():    
    tread1 = threading.Thread(target = read_serial)
    tread1.start()

btn = Button(window, text="Star Alerts", bg="blue", fg="white", command=iniciar)
btn.grid(column=1, row=8)

window.mainloop()
